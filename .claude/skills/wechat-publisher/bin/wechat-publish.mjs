#!/usr/bin/env node

/**
 * WeChat Official Account publisher powered by @wenyan-md/core.
 *
 * Usage:
 *   node .claude/skills/wechat-publisher/bin/wechat-publish.mjs render  <markdown-file> [--theme <id>] [--hl-theme <id>] [--out <html-file>]
 *   node .claude/skills/wechat-publisher/bin/wechat-publish.mjs publish <markdown-file> [--theme <id>] [--hl-theme <id>] [--dry-run] [--media-id <id>]
 *   node .claude/skills/wechat-publisher/bin/wechat-publish.mjs themes
 *
 * Options:
 *   --media-id <id>  Update an existing draft instead of creating a new one
 *
 * Environment:
 *   WECHAT_APP_ID      - WeChat AppID
 *   WECHAT_APP_SECRET  - WeChat AppSecret
 */

import { readFile, writeFile } from "node:fs/promises"
import { resolve, dirname } from "node:path"

const DRAFT_UPDATE_URL = "https://api.weixin.qq.com/cgi-bin/draft/update"

// Available themes (from wenyan-core built-in registry)
const THEMES = [
  { id: "default",     name: "Default",     desc: "简洁经典" },
  { id: "orangeheart", name: "OrangeHeart", desc: "橙色暖调" },
  { id: "rainbow",     name: "Rainbow",     desc: "彩色活泼" },
  { id: "lapis",       name: "Lapis",       desc: "冷蓝简约" },
  { id: "pie",         name: "Pie",         desc: "现代锐利 (sspai 风格)" },
  { id: "maize",       name: "Maize",       desc: "柔和米黄" },
  { id: "purple",      name: "Purple",      desc: "紫色点缀极简" },
  { id: "phycat",      name: "Phycat",      desc: "薄荷绿" },
]

const HL_THEMES = [
  "atom-one-dark", "atom-one-light", "dracula", "github",
  "github-dark", "monokai", "solarized-dark", "solarized-light", "xcode",
]

function parseArgs(args) {
  const parsed = { command: args[0], file: args[1] }
  for (let i = 2; i < args.length; i++) {
    if (args[i] === "--theme" && args[i + 1]) {
      parsed.theme = args[++i]
    } else if (args[i] === "--hl-theme" && args[i + 1]) {
      parsed.hlTheme = args[++i]
    } else if (args[i] === "--out" && args[i + 1]) {
      parsed.out = args[++i]
    } else if (args[i] === "--dry-run") {
      parsed.dryRun = true
    } else if (args[i] === "--media-id" && args[i + 1]) {
      parsed.mediaId = args[++i]
    }
  }
  return parsed
}

function stripAnchorLinks(html) {
  // WeChat rejects <a href="#xxx"> anchor links (error 45166).
  // Replace them with plain <span> preserving the text content.
  return html.replace(/<a\s+href="#[^"]*"([^>]*)>(.*?)<\/a>/gi, (_, attrs, text) => {
    const styleMatch = attrs.match(/style="[^"]*"/)
    const style = styleMatch ? ` ${styleMatch[0]}` : ""
    return `<span${style}>${text}</span>`
  })
}

async function renderMarkdown(filePath, themeId = "default", hlThemeId = "github") {
  const { renderStyledContent } = await import("@wenyan-md/core/wrapper")
  const markdown = await readFile(resolve(filePath), "utf-8")
  const result = await renderStyledContent(markdown, {
    themeId,
    hlThemeId,
    isWechat: true,
  })
  return { ...result, content: stripAnchorLinks(result.content) }
}

async function updateWechatDraft(mediaId, articleOptions, publishOptions) {
  // Reuse wenyan-core for token + image upload, then call draft/update API
  const { publishToWechatDraft } = await import("@wenyan-md/core/publish")

  // Step 1: Use publishToWechatDraft to handle image uploads (creates a temp draft)
  console.log("Uploading images and preparing content...")
  const tempDraft = await publishToWechatDraft(articleOptions, publishOptions)
  const tempMediaId = tempDraft.media_id

  // Step 2: Get access token for update + cleanup
  const appId = publishOptions.appId ?? process.env.WECHAT_APP_ID
  const appSecret = publishOptions.appSecret ?? process.env.WECHAT_APP_SECRET
  const tokenRes = await fetch(
    `https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${appId}&secret=${appSecret}`
  )
  const tokenData = await tokenRes.json()
  if (tokenData.errcode) {
    throw new Error(`Token error: ${tokenData.errcode} ${tokenData.errmsg}`)
  }
  const accessToken = tokenData.access_token

  // Helper: always clean up temp draft
  async function cleanupTempDraft() {
    try {
      await fetch(
        `https://api.weixin.qq.com/cgi-bin/draft/delete?access_token=${accessToken}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ media_id: tempMediaId }),
        }
      )
    } catch {
      // Best-effort cleanup, don't fail on this
    }
  }

  try {
    // Step 3: Get the temp draft's content (with WeChat CDN image URLs)
    const getRes = await fetch(
      `https://api.weixin.qq.com/cgi-bin/draft/get?access_token=${accessToken}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ media_id: tempMediaId }),
      }
    )
    const draftData = await getRes.json()
    if (draftData.errcode) {
      throw new Error(`Get draft error: ${draftData.errcode} ${draftData.errmsg}`)
    }
    const article = draftData.news_item[0]

    // Step 4: Update the target draft with the new content
    console.log(`Updating draft: ${mediaId}`)
    const updateRes = await fetch(
      `${DRAFT_UPDATE_URL}?access_token=${accessToken}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          media_id: mediaId,
          index: 0,
          articles: {
            title: article.title,
            content: article.content,
            thumb_media_id: article.thumb_media_id,
            author: articleOptions.author || article.author || "",
            content_source_url: articleOptions.source_url || article.content_source_url || "",
          },
        }),
      }
    )
    const updateData = await updateRes.json()
    if (updateData.errcode && updateData.errcode !== 0) {
      throw new Error(`Update error: ${updateData.errcode} ${updateData.errmsg}`)
    }

    return { media_id: mediaId }
  } finally {
    // Always clean up temp draft, even if update fails
    console.log("Cleaning up temp draft...")
    await cleanupTempDraft()
  }
}

async function listThemes() {
  console.log("\n📋 Available article themes:\n")
  for (const t of THEMES) {
    console.log(`  ${t.id.padEnd(14)} ${t.name.padEnd(14)} ${t.desc}`)
  }
  console.log("\n📋 Available code highlight themes:\n")
  for (const h of HL_THEMES) {
    console.log(`  ${h}`)
  }
  console.log()
}

async function handleRender(opts) {
  if (!opts.file) {
    console.error("Error: markdown file path required")
    process.exit(1)
  }

  const theme = opts.theme || "default"
  const hlTheme = opts.hlTheme || "github"

  console.log(`Rendering: ${opts.file}`)
  console.log(`Theme: ${theme} | Highlight: ${hlTheme}`)

  const result = await renderMarkdown(opts.file, theme, hlTheme)

  console.log(`Title: ${result.title || "(untitled)"}`)
  console.log(`Cover: ${result.cover || "(none)"}`)

  if (opts.out) {
    const outPath = resolve(opts.out)
    const htmlWrapper = `<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${result.title || "Preview"}</title>
<style>body{max-width:680px;margin:0 auto;padding:20px;background:#f5f5f5}
#content{background:#fff;padding:20px;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.1)}</style>
</head><body>
<div id="content">${result.content}</div>
</body></html>`
    await writeFile(outPath, htmlWrapper, "utf-8")
    console.log(`Preview saved: ${outPath}`)
  } else {
    console.log("---HTML_START---")
    console.log(result.content)
    console.log("---HTML_END---")
  }

  return result
}

async function handlePublish(opts) {
  if (!opts.file) {
    console.error("Error: markdown file path required")
    process.exit(1)
  }

  const appId = process.env.WECHAT_APP_ID
  const appSecret = process.env.WECHAT_APP_SECRET

  if (!appId || !appSecret || appSecret === "YOUR_APP_SECRET_HERE") {
    console.error("Error: WECHAT_APP_ID and WECHAT_APP_SECRET must be set")
    console.error("Configure them in the coworkspace open script")
    process.exit(1)
  }

  const theme = opts.theme || "default"
  const hlTheme = opts.hlTheme || "github"

  console.log(`Rendering: ${opts.file}`)
  console.log(`Theme: ${theme} | Highlight: ${hlTheme}`)

  const result = await renderMarkdown(opts.file, theme, hlTheme)

  console.log(`Title: ${result.title || "(untitled)"}`)

  if (opts.dryRun) {
    console.log("\n[DRY RUN] Would publish with:")
    console.log(`  Title: ${result.title}`)
    console.log(`  Cover: ${result.cover || "(first image in content)"}`)
    console.log(`  Author: ${result.author || "(default)"}`)
    console.log(`  Content length: ${result.content.length} chars`)
    console.log(`  Mode: ${opts.mediaId ? `update (${opts.mediaId})` : "new draft"}`)
    return
  }

  const articleOptions = {
    title: result.title || "Untitled",
    content: result.content,
    cover: result.cover,
    author: result.author,
    source_url: result.source_url,
  }
  const publishOpts = {
    appId,
    appSecret,
    relativePath: dirname(resolve(opts.file)),
  }

  if (opts.mediaId) {
    console.log(`Updating existing draft: ${opts.mediaId}`)
    const updateResult = await updateWechatDraft(opts.mediaId, articleOptions, publishOpts)
    console.log("\nDraft updated successfully!")
    console.log(`media_id: ${updateResult.media_id}`)
    return updateResult
  }

  console.log("Publishing new draft...")

  const { publishToWechatDraft } = await import("@wenyan-md/core/publish")
  const publishResult = await publishToWechatDraft(articleOptions, publishOpts)

  console.log("\nPublished successfully!")
  console.log(`Draft media_id: ${publishResult.media_id}`)
  return publishResult
}

// Main
const args = process.argv.slice(2)
const opts = parseArgs(args)

try {
  switch (opts.command) {
    case "themes":
      await listThemes()
      break
    case "render":
      await handleRender(opts)
      break
    case "publish":
      await handlePublish(opts)
      break
    default:
      console.log("Usage:")
      console.log("  node .claude/skills/wechat-publisher/bin/wechat-publish.mjs themes")
      console.log("  node .claude/skills/wechat-publisher/bin/wechat-publish.mjs render  <file.md> [--theme <id>] [--hl-theme <id>] [--out <preview.html>]")
      console.log("  node .claude/skills/wechat-publisher/bin/wechat-publish.mjs publish <file.md> [--theme <id>] [--hl-theme <id>] [--dry-run] [--media-id <id>]")
      process.exit(1)
  }
} catch (error) {
  console.error(`Error: ${error.message}`)
  process.exit(1)
}
