# Image Generation Services

## Gemini (Recommended)

**API Key**: https://aistudio.google.com/apikey

```bash
export GEMINI_API_KEY="AIza..."
```

**Endpoint**: `generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent`

**Strengths**: Excellent quality, fast generation, great prompt understanding, complex multi-element scenes, free tier available.

---

## OpenAI DALL-E 3

**API Key**: https://platform.openai.com/api-keys

```bash
export OPENAI_API_KEY="sk-..."
```

**Supported Sizes**: 1024x1024, 1792x1024, 1024x1792

**Pricing**: Standard $0.04, HD $0.08 per image.

**Strengths**: Highest quality, excellent text rendering, best for professional and marketing use.

---

## Choosing Between Services

| Criteria | Gemini | DALL-E |
|----------|--------|--------|
| Overall quality | Excellent | Highest |
| Text rendering | Good | Best |
| Speed | Fast | Moderate |
| Complex scenes | Excellent | Good |
| Cost | Free tier | $0.04-0.08 |
| Setup | 1 API Key | 1 API Key |

**Default**: Use Gemini. Switch to DALL-E when text rendering or maximum quality matters.

---

## Troubleshooting

### Gemini

**"GEMINI_API_KEY not set"**: Get key at https://aistudio.google.com/apikey

**HTTP 429**: Rate limit exceeded. Wait and retry.

**HTTP 400**: Check prompt for policy violations.

### DALL-E

**"OPENAI_API_KEY not found"**: `export OPENAI_API_KEY="sk-..."`

**Size errors**: DALL-E only supports 1024x1024, 1792x1024, 1024x1792.
