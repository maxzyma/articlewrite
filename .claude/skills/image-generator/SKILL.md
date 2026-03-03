---
name: image-generator
description: Generate high-quality AI images using Gemini 3 Pro Image Preview (Vertex AI, recommended) or OpenAI DALL-E 3. Supports custom prompts, multiple aspect ratios (16:9, 1:1, 4:3, 9:16), and automatic local saving. Use when user requests image generation, creating covers, visual content for articles/presentations, or any task requiring AI-generated visuals.
---

# Image Generator

Quality-focused AI image generation: Gemini + DALL-E.

## Quick Start

### Gemini 3 Pro Image Preview (Recommended)

```bash
export GOOGLE_PROJECT_ID=your-project-id
gcloud auth application-default login

./.claude/skills/image-generator/bin/generate "your prompt" --service gemini
```

### OpenAI DALL-E 3

```bash
export OPENAI_API_KEY=sk-...
./.claude/skills/image-generator/bin/generate "your prompt" --service openai
```

## Services

| Service | Quality | Cost | Best For |
|---------|---------|------|----------|
| **Gemini 3 Pro** | Excellent | Google Cloud billing | General use, complex scenes, first choice |
| **DALL-E 3** | Highest | $0.04-0.08/image | Text rendering, professional materials |

## Aspect Ratios

| Ratio | Resolution | Use Case |
|-------|-----------|----------|
| 16:9 | 1920x1080 | Article covers, presentations |
| 1:1 | 1024x1024 | Social media, avatars |
| 4:3 | 1536x1152 | Traditional displays |
| 9:16 | 1080x1920 | Phone wallpapers, Stories |

## Examples

### Article Cover (16:9)
```bash
./.claude/skills/image-generator/bin/generate \
  "Abstract three-layer evolution diagram, modern tech style, gradient blue and purple" \
  --service gemini \
  --width 1920 --height 1080 \
  --output ./article-cover.png
```

### DALL-E for Text-Heavy Images
```bash
./.claude/skills/image-generator/bin/generate \
  "Cyberpunk city at night, neon lights, detailed" \
  --service openai \
  --output ./cyberpunk.png
```

## Prompt Writing

**Structure**: Subject + Style + Details + Quality Modifiers

For detailed guidance, see `references/prompts.md`.
