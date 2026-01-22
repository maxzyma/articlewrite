---
name: image-generator
description: Generate AI images using multiple services (Pollinations.ai, OpenAI DALL-E, Stability AI). Supports custom prompts, multiple aspect ratios (16:9, 1:1, 4:3, 9:16), and automatic local saving. Use when user requests image generation, creating covers, visual content for articles/presentations, social media images, or any task requiring AI-generated visuals. Pollinations.ai is free and requires no API key.
---

# Image Generator

Generate AI images using multiple services with custom prompts and aspect ratios.

## Quick Start

Generate images using the `scripts/generate.py` script:

```bash
# Free service (no API key needed)
python3 scripts/generate.py "A cute cat playing in sunlight" --service pollinations

# Specify output path
python3 scripts/generate.py "Futuristic city" --service pollinations --output ./cover.png

# Custom size (16:9 for covers)
python3 scripts/generate.py "Abstract tech art" --service pollinations --width 1920 --height 1080
```

## Supported Services

### Pollinations.ai (FREE - Recommended)
- No API key required
- High quality (FLUX model)
- Fast generation
- **Use for**: Quick testing, personal projects, cost-free generation

### OpenAI DALL-E 3
- Requires `OPENAI_API_KEY` environment variable
- Best quality and text rendering
- $0.04-0.08 per image
- **Use for**: Professional projects, marketing materials

### Stability AI
- Requires `STABILITY_API_KEY` environment variable
- Artistic styles, fast generation
- $0.01-0.04 per image
- **Use for**: Artistic images, cost optimization

## Common Aspect Ratios

| Ratio | Resolution | Use Case |
|-------|-----------|----------|
| 16:9 | 1920x1080 | Article covers, presentations |
| 1:1 | 1024x1024 | Social media, avatars |
| 4:3 | 1536x1152 | Traditional displays |
| 9:16 | 1080x1920 | Phone wallpapers, Stories |

## Command-Line Options

```
positional arguments:
  prompt                 Image generation prompt

optional arguments:
  -h, --help            Show help message
  -s, --service         Service: pollinations, openai, stability (default: pollinations)
  -o, --output          Output path (default: ./generated_image.png)
  --width               Image width (default: 1920)
  --height              Image height (default: 1080)
```

## Examples

### Article Cover (16:9)
```bash
python3 scripts/generate.py \
  "Abstract three-layer evolution diagram, modern tech style, gradient blue and purple" \
  --service pollinations \
  --width 1920 --height 1080 \
  --output ./article-cover.png
```

### Social Media (1:1)
```bash
python3 scripts/generate.py \
  "Professional portrait, modern office background" \
  --service pollinations \
  --width 1024 --height 1024 \
  --output ./avatar.png
```

### Using OpenAI DALL-E
```bash
python3 scripts/generate.py \
  "Cyberpunk city at night, neon lights, detailed" \
  --service openai \
  --output ./cyberpunk.png
```

## Environment Variables (Optional)

For paid services, set API keys in your shell or project `.env`:

```bash
# OpenAI DALL-E
export OPENAI_API_KEY="sk-..."

# Stability AI
export STABILITY_API_KEY="sk-..."
```

Get API keys:
- OpenAI: https://platform.openai.com/api-keys
- Stability AI: https://platform.stability.ai/account/keys

## Prompt Writing Tips

**Good prompt structure**: Subject + Style + Details + Quality

Example:
```
"Majestic mountain landscape at sunset, photography style, dramatic lighting, 8K ultra detailed"
```

For detailed prompt writing guidance and examples, see `references/prompts.md`.

For complete service documentation, pricing, and configuration, see `references/services.md`.
