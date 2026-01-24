# Image Generation Services

Complete guide for each supported image generation service.

## Gemini 3 Pro Image Preview (Recommended - First Choice)

**Based on**: https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/gemini-3-pro-image-preview

**API Endpoint**:
```
https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/global/publishers/google/models/gemini-3-pro-image-preview:generateContent
```

**Authentication**: Requires Google Cloud credentials

### Setup Options

#### Option 1: Using gcloud CLI (Recommended)
```bash
# 1. Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec $SHELL

# 2. Login and set up credentials
gcloud auth login
gcloud auth application-default login

# 3. Set your project
gcloud config set project YOUR_PROJECT_ID
# Or: export GOOGLE_PROJECT_ID=your-project-id
```

#### Option 2: Using Access Token Directly
```bash
export GOOGLE_PROJECT_ID=your-project-id
export GOOGLE_ACCESS_TOKEN=ya29.xxx...
```

#### Option 3: Using Service Account
```bash
export GOOGLE_PROJECT_ID=your-project-id
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

**Request Format**:
```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  -H "Content-Type: application/json" \
  "https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/global/publishers/google/models/gemini-3-pro-image-preview:generateContent" \
  -d '{
    "contents": {
      "role": "user",
      "parts": {"text": "your prompt here"}
    },
    "generation_config": {
      "response_modalities": ["TEXT", "IMAGE"]
    }
  }'
```

**Features**:
- ✅ Excellent image quality (Google's latest model)
- ✅ Native text and image generation
- ✅ Fast generation speed
- ✅ Great prompt understanding

**Best for**:
- All image generation needs (recommended first choice)
- Professional projects requiring high quality
- Complex scenes with multiple elements

**Usage**:
```bash
./.claude/skills/image-generator/bin/generate "your prompt" --service gemini
```

---

## Pollinations.ai (FREE)

**API Key Required**: No - completely free!

**Features**:
- ✅ No registration or API key needed
- ✅ High quality images (FLUX model)
- ✅ Fast generation
- ✅ No rate limits
- ✅ Multiple aspect ratios supported

**Best for**:
- Quick prototyping
- Testing prompts
- Personal projects
- Learning image generation

**Limitations**:
- Queue-based generation (may take 10-30 seconds)
- Community service (no SLA)

**Usage**:
```bash
./.claude/skills/image-generator/bin/generate "your prompt" --service pollinations
```

---

## OpenAI DALL-E 3

**API Key Required**: Yes - `OPENAI_API_KEY`

**Getting API Key**:
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create account or sign in
3. Click "Create new secret key"
4. Set environment variable:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

**Features**:
- ✅ Best quality images
- ✅ Excellent text rendering
- ✅ Detailed understanding
- ✅ 1024x1024, 1792x1024, 1024x1792 sizes

**Best for**:
- Professional projects
- Marketing materials
- High-quality covers
- Text-heavy images

**Pricing** (as of 2025):
- Standard: $0.040 per image
- HD: $0.080 per image

**Usage**:
```bash
./.claude/skills/image-generator/bin/generate "your prompt" --service openai
```

---

## Stability AI (Stable Diffusion)

**API Key Required**: Yes - `STABILITY_API_KEY`

**Getting API Key**:
1. Visit [Stability AI Platform](https://platform.stability.ai/account/keys)
2. Create account or sign in
3. Generate API key
4. Set environment variable:
   ```bash
   export STABILITY_API_KEY="sk-..."
   ```

**Features**:
- ✅ Multiple SDXL models
- ✅ Fast generation
- ✅ Customizable (CFG, steps)
- ✅ Good for artistic styles

**Best for**:
- Artistic images
- Style variations
- Batch generation
- Cost optimization

**Pricing** (as of 2025):
- $0.01-0.04 per image (depending on model)

**Usage**:
```bash
./.claude/skills/image-generator/bin/generate "your prompt" --service stability
```

---

## Common Aspect Ratios

| Ratio | Resolution | Use Case |
|-------|-----------|----------|
| 16:9 | 1920x1080 | Video covers, presentations |
| 1:1 | 1024x1024 | Social media, avatars |
| 4:3 | 1536x1152 | Traditional displays |
| 9:16 | 1080x1920 | Phone wallpapers, Stories |
| 21:9 | 2016x864 | Ultrawide displays |

---

## Choosing a Service

### Use Gemini (Vertex AI) when:
- You want the best overall quality (recommended first choice)
- You have Google Cloud access set up
- Quality and speed are both important
- You need reliable, production-ready results

### Use Pollinations.ai when:
- You want to test ideas quickly
- You don't have API keys set up
- Cost is a concern
- Quality requirements are moderate

### Use DALL-E when:
- You need highest quality
- Text rendering is important
- Budget allows ($0.04-0.08/image)
- Professional use

### Use Stability AI when:
- You want artistic styles
- Need batch generation
- Want fine-tuned control
- Cost-sensitive (cheaper than DALL-E)

---

## Troubleshooting

### Gemini/Vertex AI Issues

**"GOOGLE_PROJECT_ID not set"**:
```bash
export GOOGLE_PROJECT_ID=your-project-id
# Or: gcloud config set project YOUR_PROJECT_ID
```

**"No access token available"**:
```bash
# Install and login with gcloud
gcloud auth application-default login

# Or set token directly
export GOOGLE_ACCESS_TOKEN=ya29.xxx...
```

**HTTP 404 or 403 errors**:
- Ensure Vertex AI API is enabled in your Google Cloud project
- Check that your project has billing enabled
- Verify you have access to the model

### Pollinations Issues

**Slow generation**:
- Try again later during off-peak hours
- Reduce image size for faster results

### General Issues

**Proxy errors**:
- The scripts use urllib directly which should work with most proxy configurations
- If issues persist, check your system proxy settings
