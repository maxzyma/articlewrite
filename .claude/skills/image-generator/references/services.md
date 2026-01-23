# Image Generation Services

Complete guide for each supported image generation service.

## Gemini 2.0 Flash Exp Image Generation (Recommended - First Choice)

**API Key Required**: Yes - `GEMINI_API_KEY`

**Getting API Key**:
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create account or sign in
3. Click "Create API Key"
4. Set environment variable:
   ```bash
   export GEMINI_API_KEY="AI..."
   ```

**Features**:
- ✅ Excellent image quality
- ✅ Google's latest 2.0 Flash model
- ✅ Fast generation speed
- ✅ Great prompt understanding
- ✅ Multiple aspect ratios supported

**Best for**:
- All image generation needs (recommended as first choice)
- Professional projects
- High-quality covers
- Complex scenes

**Pricing** (as of 2025):
- Very competitive pricing
- Free tier available for testing
- Pay-per-use after free tier

**Usage**:
```bash
python3 scripts/generate.py "your prompt" --service gemini
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
python3 scripts/generate.py "your prompt" --service pollinations
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
python3 scripts/generate.py "your prompt" --service openai
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
python3 scripts/generate.py "your prompt" --service stability
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

**Use Gemini when**:
- You want the best overall experience (recommended first choice)
- Quality and speed are both important
- You need reliable results
- Professional or personal projects

**Use Pollinations.ai when**:
- You want to test ideas quickly
- You don't have API keys
- Cost is a concern
- Quality requirements are moderate

**Use DALL-E when**:
- You need highest quality
- Text rendering is important
- Budget allows ($0.04-0.08/image)
- Professional use

**Use Stability AI when**:
- You want artistic styles
- Need batch generation
- Want fine-tuned control
- Cost-sensitive (cheaper than DALL-E)
