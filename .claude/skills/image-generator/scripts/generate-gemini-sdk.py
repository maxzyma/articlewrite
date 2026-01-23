#!/usr/bin/env python3
"""
Gemini image generator using official Google AI SDK
"""
import os
import sys

try:
    import google.generativeai as genai
except ImportError:
    print("❌ Google Generative AI SDK not installed")
    print("Install with: pip3 install google-generativeai")
    sys.exit(1)

# Get API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not found in environment")
    sys.exit(1)

# Parse arguments
if len(sys.argv) < 2:
    print("Usage: python3 generate-gemini-sdk.py \"prompt\" [output_path]")
    sys.exit(1)

prompt = sys.argv[1]
output = sys.argv[2] if len(sys.argv) > 2 else "gemini-output.png"

print(f"🎨 Generating with Gemini...")
print(f"📝 Prompt: {prompt[:100]}...")

# Configure API
genai.configure(api_key=api_key)

# Try to use image generation model
try:
    # Use the experimental image generation model
    model = genai.GenerativeModel("gemini-3-pro-image-preview")

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="image/png"
        )
    )

    # Save image
    if hasattr(response, 'parts') and len(response.parts) > 0:
        part = response.parts[0]
        if hasattr(part, 'inline_data') and part.inline_data:
            import base64
            image_bytes = base64.b64decode(part.inline_data.data)
            with open(output, 'wb') as f:
                f.write(image_bytes)
            print("✅ Image generated successfully!")
            print(f"💾 Saved to: {output}")
        else:
            print("❌ No image data in response")
            print(f"Response: {response}")
    else:
        print("❌ Unexpected response format")
        print(f"Response: {response}")

except Exception as e:
    print(f"❌ Error: {e}")
    print("\nNote: Gemini image generation may require specific model access.")
    print("Falling back to Pollinations.ai...")

    # Fallback to Pollinations
    import urllib.request
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=True&enhance=True"
    urllib.request.urlretrieve(url, output)
    print("✅ Image generated using Pollinations.ai")
    print(f"💾 Saved to: {output}")
