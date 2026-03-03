# Image Generation Services

## Gemini 3 Pro Image Preview (Recommended)

**API Endpoint**:
```
https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/global/publishers/google/models/gemini-3-pro-image-preview:generateContent
```

**Reference**: https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/gemini-3-pro-image-preview

### Setup

#### Option 1: gcloud CLI (Recommended)
```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

#### Option 2: Access Token
```bash
export GOOGLE_PROJECT_ID=your-project-id
export GOOGLE_ACCESS_TOKEN=ya29.xxx...
```

#### Option 3: Service Account
```bash
export GOOGLE_PROJECT_ID=your-project-id
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

**Strengths**: Excellent quality, fast generation, great prompt understanding, complex multi-element scenes.

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
| Cost | GCP billing | $0.04-0.08 |

**Default**: Use Gemini. Switch to DALL-E when text rendering or maximum quality matters.

---

## Troubleshooting

### Gemini

**"GOOGLE_PROJECT_ID not set"**: `export GOOGLE_PROJECT_ID=your-project-id`

**"No access token"**: `gcloud auth application-default login`

**HTTP 403/404**: Ensure Vertex AI API is enabled and billing is active.

### DALL-E

**"OPENAI_API_KEY not found"**: `export OPENAI_API_KEY="sk-..."`

**Size errors**: DALL-E only supports 1024x1024, 1792x1024, 1024x1792.
