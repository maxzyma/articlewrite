#!/usr/bin/env node

/**
 * Scan all article front-matter and generate a publish status overview.
 *
 * Usage: node scripts/publish-status.mjs
 */

import { readdir, readFile } from 'node:fs/promises'
import { join } from 'node:path'

const ROOT = new URL('..', import.meta.url).pathname

async function extractFrontMatter(filePath) {
  const content = await readFile(filePath, 'utf-8')
  const match = content.match(/^---\n([\s\S]*?)\n---/)
  if (!match) return null

  const lines = match[1].split('\n')
  const fm = {}
  let currentKey = null
  let currentObj = null

  for (const line of lines) {
    const kvMatch = line.match(/^(\w+):\s*(.*)$/)
    if (kvMatch) {
      const [, key, value] = kvMatch
      if (value === '' || value === '{}') {
        fm[key] = {}
        currentKey = key
        currentObj = fm[key]
      } else {
        fm[key] = value
        currentKey = null
        currentObj = null
      }
      continue
    }

    const nestedMatch = line.match(/^\s+(\w+):\s*(.+)$/)
    if (nestedMatch && currentObj) {
      currentObj[nestedMatch[1]] = nestedMatch[2]
    }
  }
  return fm
}

const SKIP_DIRS = new Set(['node_modules', 'scripts', 'skills', '.claude', '.git'])

async function tryReadArticle(dirPath, slug) {
  const files = await readdir(dirPath)
  const mdFile = files.find(f => f.endsWith('.md'))
  if (!mdFile) return null

  const fm = await extractFrontMatter(join(dirPath, mdFile))
  if (!fm?.title) return null

  return {
    slug,
    title: fm.title,
    author: fm.author || 'Mazy',
    created: fm.created || '?',
    published: typeof fm.published === 'object' ? fm.published : {},
  }
}

async function scanArticles() {
  const articles = []
  const years = await readdir(ROOT, { withFileTypes: true })

  for (const entry of years) {
    if (!entry.isDirectory() || SKIP_DIRS.has(entry.name)) continue

    // YYYY/ directory — scan months
    if (/^\d{4}$/.test(entry.name)) {
      const yearPath = join(ROOT, entry.name)
      const months = await readdir(yearPath, { withFileTypes: true })
      for (const month of months) {
        if (!month.isDirectory()) continue
        const monthPath = join(yearPath, month.name)
        const slugs = await readdir(monthPath, { withFileTypes: true })
        for (const slug of slugs) {
          if (!slug.isDirectory()) continue
          const article = await tryReadArticle(join(monthPath, slug.name), slug.name)
          if (article) articles.push(article)
        }
      }
      continue
    }

    // Legacy: flat article directory at root
    const article = await tryReadArticle(join(ROOT, entry.name), entry.name)
    if (article) articles.push(article)
  }

  return articles.sort((a, b) => (b.created || '').localeCompare(a.created || ''))
}

function formatTable(articles) {
  const channels = new Set()
  for (const a of articles) {
    for (const ch of Object.keys(a.published)) channels.add(ch)
  }
  const chList = [...channels].sort()

  const header = `| # | 文章 | 创建日期 | ${chList.map(c => c).join(' | ')} |`
  const sep = `|---|------|---------|${chList.map(() => '---').join('|')}|`

  const rows = articles.map((a, i) => {
    const chCols = chList.map(c => a.published[c] || '-')
    return `| ${i + 1} | ${a.title} | ${a.created} | ${chCols.join(' | ')} |`
  })

  return [header, sep, ...rows].join('\n')
}

function formatStats(articles) {
  const total = articles.length
  const unpublished = articles.filter(a => Object.keys(a.published).length === 0).length
  const published = total - unpublished
  return `\n总计: ${total} 篇 | 已发布: ${published} 篇 | 未发布: ${unpublished} 篇`
}

const articles = await scanArticles()
console.log('\n# 文章发布状态总览\n')
console.log(formatTable(articles))
console.log(formatStats(articles))
