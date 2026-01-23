#!/usr/bin/env python3
"""
Gemini image generator using correct model name
"""
import os
import sys
import json
import base64

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
    print("Usage: python3 generate-gemini-v2.py \"prompt\" [output_path]")
    sys.exit(1)

prompt = sys.argv[1]
output = sys.argv[2] if len(sys.argv) > 2 else "gemini-output.png"

print(f"🎨 Generating with Gemini 2.0 Flash Exp Image Generation...")
print(f"📝 Prompt: {prompt[:100]}...")

# Configure API
genai.configure(api_key=api_key)

# Use the correct model
try:
    # Try gemini-2.0-flash-exp-image-generation first
    model = genai.GenerativeModel("models/gemini-2.0-flash-exp-image-generation")

    response = model.generate_content(prompt)

    # Save image
    if hasattr(response, 'parts') and len(response.parts) > 0:
        part = response.parts[0]
        if hasattr(part, 'inline_data') and part.inline_data:
            image_bytes = base64.b64decode(part.inline_data.data)
            with open(output, 'wb') as f:
                f.write(image_bytes)
            print("✅ Image generated successfully with Gemini!")
            print(f"💾 Saved to: {output}")
        else:
            print(f"❌ No image data in response")
            print(f"Response parts: {response.parts}")
    else:
        print(f"❌ Unexpected response format")
        print(f"Response: {response}")

except Exception as e:
    print(f"❌ Error with Gemini: {e}")

    # Try Imagen model as fallback
    try:
        print("🔄 Trying Imagen model...")
        model = genai.GenerativeModel("models/imagen-3.0-generate-001")

        response = model.generate_content(prompt)

        if hasattr(response, 'parts') and len(response.parts) > 0:
            part = response.parts[0]
            if hasattr(part, 'inline_data') and part.inline_data:
                image_bytes = base64.b64decode(part.inline_data.data)
                with open(output, 'wb') as f:
                    f.write(image_bytes)
                print("✅ Image generated successfully with Imagen!")
                print(f"💾 Saved to: {output}")
                sys.exit(0)
    except Exception as e2:
        print(f"❌ Imagen also failed: {e2}")

    # Final fallback to Pollinations
    print("🔄 Falling back to Pollinations.ai...")
    import urllib.request
    import urllib.parse
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=True&enhance=True"
    urllib.request.urlretrieve(url, output)
    print("✅ Image generated using Pollinations.ai")
    print(f"💾 Saved to: {output}")
