# 文章目录结构规则

## 每篇文章一个独立目录

```
articlewrite/
├── <article-slug>/
│   ├── <article-slug>.md      # 文章正文
│   ├── cover.png              # 封面（如有）
│   └── images/                # 配图（如有）
│       ├── fig1-xxx.png
│       └── fig2-xxx.png
```

## 约束

- **禁止**按主题分类建父目录（如 `ai-research/`）——所有文章平铺在根目录
- **禁止**在根目录直接放 .md 文件——必须归入文章目录
- 图片必须放在各自文章目录内，不共享 `images/`
- 封面迭代只保留最终版，废弃版本不提交
- 新增文章：`mkdir <slug> && 写 <slug>/<slug>.md`
- **作者名固定为 `Mazy`** —— front-matter 中 `author: Mazy`，不使用其他名称
- 文章量超 40 篇时引入 `YYYY/MM/` 年月分层

## Front-matter 格式（必须）

```yaml
---
title: 文章标题
author: Mazy
description: 一句话摘要
cover: ./cover.png          # 可选
created: YYYY-MM-DD
published:                  # source of truth
  wechat: YYYY-MM-DD       # 按渠道记录发布日期
  juejin: YYYY-MM-DD
---
```

- 未发布的渠道不写或写 `published: {}`
- 发布后在 front-matter 中补充渠道和日期
- 总览用 `node scripts/publish-status.mjs` 聚合生成
