#!/usr/bin/env python3
"""
Imagen image generator - Google's dedicated image generation model
"""
import os
import sys
import base64

try:
    import google.generativeai as genai
except ImportError:
    print("❌ Google Generative AI SDK not installed")
    sys.exit(1)

# Get API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not found in environment")
    sys.exit(1)

# Parse arguments
if len(sys.argv) < 2:
    print("Usage: python3 generate-imagen.py \"prompt\" [output_path]")
    sys.exit(1)

prompt = sys.argv[1]
output = sys.argv[2] if len(sys.argv) > 2 else "imagen-output.png"

print(f"🎨 Generating with Imagen 3.0...")
print(f"📝 Prompt: {prompt[:100]}...")

# Configure API
genai.configure(api_key=api_key)

# Try different Imagen models
imagen_models = [
    "models/imagen-3.0-generate-001",
    "models/imagen-4.0-generate-001",
    "models/imagen-4.0-fast-generate-001",
]

for model_name in imagen_models:
    try:
        print(f"🔄 Trying {model_name}...")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        # Save image
        if hasattr(response, 'parts') and len(response.parts) > 0:
            part = response.parts[0]
            if hasattr(part, 'inline_data') and part.inline_data:
                image_bytes = base64.b64decode(part.inline_data.data)
                with open(output, 'wb') as f:
                    f.write(image_bytes)
                print(f"✅ Image generated successfully with {model_name}!")
                print(f"💾 Saved to: {output}")
                sys.exit(0)
            else:
                print(f"   ⚠️  No image data, trying next model...")
        else:
            print(f"   ⚠️  Unexpected response format, trying next model...")

    except Exception as e:
        print(f"   ⚠️  {model_name} failed: {str(e)[:100]}")
        continue

# If all Imagen models fail, fallback to Pollinations
print("🔄 All Imagen models failed, falling back to Pollinations.ai...")
import urllib.request
import urllib.parse
encoded_prompt = urllib.parse.quote(prompt)
url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=True&enhance=True"
urllib.request.urlretrieve(url, output)
print("✅ Image generated using Pollinations.ai")
print(f"💾 Saved to: {output}")
