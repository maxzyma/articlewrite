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
