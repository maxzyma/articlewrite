---
name: article-writing
description: End-to-end workflow for writing and illustrating technical blog posts. Covers article structuring, industry research/deduplication, evidence-backed argument integration, infographic generation (PIL + AntV Chart MCP), and publication preparation. Use when user wants to write a tech article, expand notes into a blog post, add images to an article, or mentions "写文章", "扩写博文", "添加配图", "技术文章".
---

# Tech Article Workflow

End-to-end technical article creation: draft → validate → enrich → illustrate → publish.

## Workflow Stages

### Stage 1: Draft & Structure

1. Analyze user's input (notes, outline, framework)
2. Propose article structure with sections and key arguments
3. Write first draft with clear section hierarchy
4. Add YAML front-matter:

```yaml
---
title: Article Title
author: Magoo
description: One-sentence summary for social sharing
cover: ./images/cover-name.png
---
```

### Stage 2: Industry Validation

Before deepening content, check for duplicate viewpoints:

1. Web search for key terms and claims in the article
2. Identify what's already industry consensus vs. original contribution
3. Report findings to user with specific risks:
   - "This claim is well-established — cite rather than claim originality"
   - "This framing is novel — emphasize differentiation"
4. Integrate industry references and prior art citations into the article

### Stage 3: Argument Enrichment

For each core argument, strengthen with evidence:

1. Use subagent for parallel research (web search + academic sources)
2. Find quantitative data (benchmarks, surveys, industry reports)
3. Find authoritative quotes (key figures, official publications)
4. Weave evidence naturally into narrative — avoid "report style" listing
5. Add reference list at article end

### Stage 4: Illustration

Generate images that enhance comprehension. See [references/image-generation.md](references/image-generation.md) for detailed patterns.

**Tool selection decision tree:**

```
What type of visual?
├─ Custom infographic (evolution chain, comparison cards, flow diagram)
│  → PIL Python script (full layout control, Chinese font support)
│
├─ Data-driven chart (radar, area, column, bar, scatter)
│  → AntV Chart MCP (mcp-server-chart, texture:"rough" for hand-drawn)
│
├─ AI-generated art/photo (covers, abstract visuals)
│  → image-generator skill (Gemini recommended, DALL-E for text)
│
└─ Architecture/flow diagram (simple boxes and arrows)
   → AntV flow_diagram or PIL (avoid AntV mind_map — excessive whitespace)
```

**Image insertion pattern:**

1. Create `images/` subdirectory in article folder
2. Use relative paths: `![alt text](images/fig-name.png)`
3. Place images at contextually relevant positions (after the concept they illustrate)
4. Clean up generation scripts after use

### Stage 5: Review & Publish

1. Check introduction foreshadows all core arguments
2. Verify all images render correctly (read PNG to visually confirm)
3. Update front-matter (title, description, cover)
4. Auto-commit and push per CLAUDE.md rules

## Quality Principles

- **Conclusion-first**: TL;DR and core claims at the top, evidence below
- **Cite don't claim**: Acknowledge existing consensus, highlight original contribution
- **Show don't tell**: Prefer infographics over text for comparisons and timelines
- **Evidence density**: Every major claim should have a data point or authoritative reference
- **Image restraint**: 3-5 images per article; each must add comprehension value, not decoration
