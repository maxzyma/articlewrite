#!/usr/bin/env python3
"""
Direct Gemini image generator without proxy issues
"""
import os
import sys
import base64
import subprocess

# Get API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not found in environment")
    sys.exit(1)

# Parse arguments
if len(sys.argv) < 2:
    print("Usage: python3 generate-gemini-direct.py \"prompt\" [output_path]")
    sys.exit(1)

prompt = sys.argv[1]
output = sys.argv[2] if len(sys.argv) > 2 else "gemini-output.png"

print(f"🎨 Generating with Gemini 3 Pro Image Preview...")
print(f"📝 Prompt: {prompt[:100]}...")

# Use curl to avoid Python proxy issues
import urllib.parse
encoded_prompt = urllib.parse.quote(prompt)

curl_command = [
    "curl", "-X", "POST",
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateImage?key={api_key}",
    "-H", "Content-Type: application/json",
    "-d", f'{{"contents":[{{"parts":[{{"text":"{prompt}"}}]}}],"generationConfig":{{"responseMimeType":"image/png"}}}}',
    "--max-time", "120",
    "--silent"
]

try:
    result = subprocess.run(curl_command, capture_output=True, text=True, check=False)

    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        sys.exit(1)

    # Parse JSON response
    import json
    response_data = json.loads(result.stdout)

    # Extract base64 image data
    image_b64 = response_data['candidates'][0]['content']['parts'][0]['inlineData']['data']
    image_bytes = base64.b64decode(image_b64)

    # Save image
    with open(output, 'wb') as f:
        f.write(image_bytes)

    print("✅ Image generated successfully!")
    print(f"💾 Saved to: {output}")

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
