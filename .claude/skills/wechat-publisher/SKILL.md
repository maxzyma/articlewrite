---
name: wechat-publisher
description: Publish Markdown articles to WeChat Official Account (微信公众号) drafts. Converts Markdown to beautifully styled HTML with theme support, uploads images, and publishes to drafts via WeChat API. Use when user wants to publish an article to WeChat, or mentions "公众号", "微信发布", "wechat publish".
---

# WeChat Publisher Skill (微信公众号发布)

Publish Markdown articles to WeChat Official Account drafts with beautiful themes.

Powered by [`@wenyan-md/core`](https://github.com/caol64/wenyan-core) — Markdown → 带主题内联样式 HTML → 微信草稿箱。

## Prerequisites

- `WECHAT_APP_ID` and `WECHAT_APP_SECRET` environment variables (configured in coworkspace `open` script)
- `@wenyan-md/core` + peer deps installed (`package.json` already configured)
- WeChat Official Account with API access and **IP whitelist** configured on [微信开发者平台](https://developers.weixin.qq.com/platform)

## Workflow

### Step 1: Identify the Article

1. If a specific file is mentioned, use that file
2. If no file specified, ask which Markdown file to publish
3. Read the file and check for YAML front-matter

**Front-matter is critical** — without it, title defaults to "Untitled" and no cover image is set:

```yaml
---
title: 文章标题
cover: ./cover.jpg
author: Mazy
description: 文章摘要（显示在公众号消息列表）
source_url: https://original-url.com
---
```

**Front-matter checklist (MUST verify before publishing):**
- [ ] `title` — 缺失则标题显示 "Untitled"
- [ ] `cover` — 缺失则取正文第一张图；若正文也无图则发布失败
- [ ] `author` — 可选，缺失则显示公众号默认名称

If `title` or `cover` is missing, **proactively提醒用户补充**，不要直接发布。

**WeChat 正文清理规则（MUST，发布前自动执行）：**

微信文章标题由 front-matter `title` 字段控制，正文不应重复。发布时必须创建临时副本并执行以下清理：

1. **删除 H1 标题**（`# xxx`）— 微信标题已由 front-matter 控制，正文中的 H1 会导致重复
2. **清空 `description` 字段**（设为 `description:`）— wenyan-md 会将 description 渲染为正文顶部引用块，与微信消息列表摘要重复
3. **保留 TL;DR / 正文引用块** — 这些是文章内容的一部分，不应删除
4. **修正图片路径** — 临时副本中的相对路径需改为绝对路径

> 原始 Markdown 文件不修改，所有清理操作在 `/tmp/claude/wechat-publish.md` 临时副本上执行。

### Step 2: Cover Image

封面图质量直接决定文章在列表页的点击率。

**封面图规格：**
- 推荐比例 **2.35:1**（900×383 或 1800×766）
- 内容在小卡片上必须一眼可辨，**避免用文章内的密集信息图作封面**
- 信息层级：大标题 + 核心视觉元素（3 个以内），底部可加副标题

**生成封面图（推荐使用 image-generator skill）：**

```bash
export GEMINI_API_KEY=$GEMINI_API_KEY
./.claude/skills/image-generator/bin/generate \
  "描述封面内容的 prompt" \
  --service gemini \
  --width 1800 --height 766 \
  --output ./path/to/cover.png
```

> **注意**：image-generator 的 `--output` 相对路径基于 skill 目录，建议用绝对路径或确认输出位置后手动移动。

生成后更新 front-matter 的 `cover` 字段指向该文件（相对于 Markdown 文件的路径）。

### Step 3: Choose Theme

```bash
node scripts/wechat-publish.mjs themes
```

| ID | Name | Style | Recommended For |
|---|---|---|---|
| `default` | Default | 简洁经典 | 通用 |
| `orangeheart` | OrangeHeart | 橙色暖调 | 生活/产品 |
| `rainbow` | Rainbow | 彩色活泼 | 创意/设计 |
| `lapis` | Lapis | 冷蓝简约 | **技术文章首选** |
| `pie` | Pie | 现代锐利 (sspai 风格) | 科技评测 |
| `maize` | Maize | 柔和米黄 | 教程/笔记 |
| `purple` | Purple | 紫色点缀极简 | 思考/观点 |
| `phycat` | Phycat | 薄荷绿 | 科普/学术 |

Code highlight themes: `atom-one-dark`, `atom-one-light`, `dracula`, `github` (default), `github-dark`, `monokai`, `solarized-dark`, `solarized-light`, `xcode`

If user has a preferred theme from previous sessions, use that directly.

### Step 4: Preview

Render and preview in mobile viewport (simulating WeChat reading experience):

```bash
mkdir -p /tmp/claude
node scripts/wechat-publish.mjs render <markdown-file> \
  --theme <theme-id> \
  --hl-theme <hl-theme-id> \
  --out /tmp/claude/wechat-preview.html
```

**Use chrome-devtools MCP for mobile preview:**

```
1. navigate_page → file:///tmp/claude/wechat-preview.html
2. emulate viewport → { width: 375, height: 812, deviceScaleFactor: 3, isMobile: true, hasTouch: true }
3. take_screenshot (viewport, not fullPage) → show to user
4. If user wants to see more, scroll with evaluate_script:
   () => { window.scrollTo(0, 2000); return 'scrolled'; }
   then take another screenshot
```

> **经验**：fullPage 截图对长文会生成超大图（87000+ px），不利于查看。改用分段 viewport 截图更实用。

Let user confirm styling. If adjustments needed, re-render with different theme.

### Step 5: Publish or Update

**New draft (首次发布):**

```bash
node scripts/wechat-publish.mjs publish <markdown-file> \
  --theme <theme-id> \
  --hl-theme <hl-theme-id>
```

**Update existing draft (修改已有草稿):**

```bash
node scripts/wechat-publish.mjs publish <markdown-file> \
  --theme <theme-id> \
  --hl-theme <hl-theme-id> \
  --media-id <draft-media-id>
```

> **`--media-id` 工作原理**：创建临时草稿（复用 wenyan-core 的完整图片上传 + 缓存逻辑）→ 读取临时草稿内容（含微信 CDN 图片 URL）→ 更新目标草稿 → 自动删除临时草稿。对用户来说是原地更新，无需手动清理。

**记住 media_id**：每次发布成功后会返回 `media_id`，后续更新需要用到。建议将 media_id 记录在文章的 front-matter 中：

```yaml
---
title: 文章标题
wechat_media_id: Kp3yNKpaOwwGup4XjiOi2xxx
---
```

Optional dry run first: add `--dry-run` to verify metadata without actual API call.

**Important**: env vars must be exported in current shell session:
```bash
export WECHAT_APP_ID=$WECHAT_APP_ID
export WECHAT_APP_SECRET=$WECHAT_APP_SECRET
```

Report to user:
- Draft `media_id` on success
- Remind: go to [mp.weixin.qq.com](https://mp.weixin.qq.com) → 草稿箱 to preview and send

### Step 6: Post-publish

- **Record `media_id` in front-matter** (`wechat_media_id: xxx`) for future updates — this is mandatory, not optional
- If re-published due to `40007` (old draft deleted), **update front-matter with the new `media_id`** — stale IDs cause repeated failures
- Git commit the front-matter changes

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `invalid ip ... not in whitelist` | Machine IP not whitelisted | `curl -s ifconfig.me` → add IP at [developers.weixin.qq.com/platform](https://developers.weixin.qq.com/platform) → 基础信息 → IP 白名单 |
| `invalid credential` | Wrong AppID/AppSecret | Verify in coworkspace `open` script |
| `access_token expired` | Token cache stale | `rm -f ~/.config/wenyan-md/token.json` and retry |
| `require subscribe` | Account type limitation | Some APIs require verified service account (认证服务号) |
| `45166: invalid content` | **HTML 中含有 `<a href="#xxx">` 锚点链接** | 脚本已自动处理：`stripAnchorLinks()` 将 `#` 锚点转为 `<span>`。如仍报此错，检查是否有其他微信不支持的 HTML 元素 |
| `40007: invalid media_id` | 目标草稿已被删除或 media_id 错误 | 草稿被手动删除后 media_id 失效，需重新用 `publish`（不带 `--media-id`）新建草稿，**并更新 front-matter 中的 `wechat_media_id`** |
| No cover image | No `cover` in front-matter and no images in content | Add `cover:` field or include at least one image |
| Title shows "Untitled" | Missing `title` in front-matter | Add front-matter with `title:` field |

**AppSecret management**: Since Dec 2025, WeChat moved「开发接口管理」to [微信开发者平台](https://developers.weixin.qq.com/platform). AppSecret reset/freeze is now at: 我的业务与服务 → 公众号 → 基础信息 → 开发密钥.

## Architecture

```
scripts/wechat-publish.mjs          CLI entry point
  ├── @wenyan-md/core/wrapper       renderStyledContent() — Markdown → styled HTML
  │     ├── marked + highlight.js   Markdown parsing + code highlighting
  │     ├── css-tree                CSS AST → inline styles (微信不支持 <style> 和 class)
  │     ├── MathJax                 TeX formulas → SVG
  │     └── JSDOM                   Node.js DOM simulation
  └── @wenyan-md/core/publish       publishToWechatDraft() — images + draft API
        ├── Access Token            cached at ~/.config/wenyan-md/token.json (7200s TTL)
        ├── Image upload            MD5 dedup cache at ~/.config/wenyan-md/upload-cache.json
        └── WeChat Draft API        POST /cgi-bin/draft/add
```

## Tips

- Images (local paths + URLs) are automatically uploaded to WeChat CDN (`mmbiz.qpic.cn`)
- Already-uploaded images are skipped (URL prefix check)
- Image uploads are cached by MD5 hash — same image won't re-upload
- Cover path is **relative to the Markdown file**, not the project root
- WeChat article content limit ~20000 chars; very long articles may need splitting
- The rendering engine converts all CSS to inline styles (微信 requirement): no `<style>`, no `class`, no CSS variables, no pseudo-elements — all handled automatically
- `--media-id` 更新时，author/source_url 等字段优先取 front-matter 原始值（脚本已修复），不依赖临时草稿读回的值
- 更新草稿后，mp.weixin.qq.com 草稿箱可能有**浏览器缓存**，可通过 `draft/get` API 验证实际内容
- front-matter 中的 `wechat_media_id` 是后续更新的唯一凭据，**发布/重发后必须同步更新**
