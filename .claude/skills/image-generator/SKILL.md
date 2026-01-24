---
name: image-generator
description: Generate AI images using multiple services (Gemini 3 Pro Image Preview via Vertex AI as first choice, also supports Pollinations.ai, OpenAI DALL-E, Stability AI). Supports custom prompts, multiple aspect ratios (16:9, 1:1, 4:3, 9:16), and automatic local saving. Use when user requests image generation, creating covers, visual content for articles/presentations, social media images, or any task requiring AI-generated visuals. Gemini 3 Pro Image Preview via Vertex AI is recommended as the first choice.
---

# Image Generator

Generate AI images using multiple services with custom prompts and aspect ratios.

## Quick Start

### Gemini 3 Pro Image Preview (Recommended - First Choice)

```bash
# Set up Google Cloud project and authentication
export GOOGLE_PROJECT_ID=your-project-id
gcloud auth application-default login

# Generate image (recommended)
./.claude/skills/image-generator/bin/generate "your prompt" --service gemini
```

### Pollinations.ai (Free, No API Key)

```bash
./.claude/skills/image-generator/bin/generate "your prompt" --service pollinations
```

### OpenAI DALL-E 3

```bash
export OPENAI_API_KEY=sk-...
./.claude/skills/image-generator/bin/generate "your prompt" --service openai
```

## Supported Services

### Gemini 3 Pro Image Preview (Recommended - First Choice)

**Authentication**: Requires Google Cloud credentials

**Setup**:
1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
2. Set project ID:
   ```bash
   export GOOGLE_PROJECT_ID=your-project-id
   # Or: gcloud config set project YOUR_PROJECT_ID
   ```
3. Authenticate:
   ```bash
   gcloud auth application-default login
   ```

**Alternative authentication**:
- Access token: `export GOOGLE_ACCESS_TOKEN=ya29.xxx...`
- Service account: `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json`

**API**: Uses Vertex AI endpoint based on official documentation
- Reference: https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/gemini-3-pro-image-preview

### Pollinations.ai (FREE)
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
  -s, --service         Service: gemini, pollinations, openai, stability (default: gemini)
  -o, --output          Output path (default: ./generated_image.png)
  --width               Image width (default: 1920)
  --height              Image height (default: 1080)
```

## Examples

### Article Cover (16:9)
```bash
./.claude/skills/image-generator/bin/generate \
  "Abstract three-layer evolution diagram, modern tech style, gradient blue and purple" \
  --service gemini \
  --width 1920 --height 1080 \
  --output ./article-cover.png
```

### Social Media (1:1)
```bash
./.claude/skills/image-generator/bin/generate \
  "Professional portrait, modern office background" \
  --service pollinations \
  --width 1024 --height 1024 \
  --output ./avatar.png
```

### Using OpenAI DALL-E
```bash
./.claude/skills/image-generator/bin/generate \
  "Cyberpunk city at night, neon lights, detailed" \
  --service openai \
  --output ./cyberpunk.png
```

## Environment Variables

### For Gemini (Vertex AI)
```bash
# Required
export GOOGLE_PROJECT_ID=your-project-id

# Authentication (choose one)
export GOOGLE_ACCESS_TOKEN=ya29.xxx...           # Direct token
export GOOGLE_APPLICATION_CREDENTIALS=/path/key.json  # Service account
# Or use: gcloud auth application-default login
```

### For Other Services
```bash
export OPENAI_API_KEY="sk-..."
export STABILITY_API_KEY="sk-..."
```

## Setup Guide

### Google Cloud Setup (for Gemini)

1. **Create a Google Cloud project**:
   - Visit: https://console.cloud.google.com/
   - Click "New Project"

2. **Enable Vertex AI API**:
   - Go to: https://console.cloud.google.com/apis/library/aiplatform.googleapis.com
   - Select your project and enable

3. **Authenticate**:
   ```bash
   # Install gcloud
   curl https://sdk.cloud.google.com | bash
   exec $SHELL

   # Login
   gcloud auth login
   gcloud auth application-default login

   # Set project
   gcloud config set project YOUR_PROJECT_ID
   ```

### Get API Keys
- Gemini: Via Google Cloud Console (no separate key needed)
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
