#!/usr/bin/env python3
"""
Gemini 3 Pro Image Generator using Vertex AI API with OAuth access token
or API key authentication

Usage:
    # Option 1: With gcloud (recommended)
    export GOOGLE_PROJECT_ID=your-project-id
    gcloud auth application-default login
    python3 generate-gemini-vertex.py "prompt" output.png

    # Option 2: With access token directly
    export GOOGLE_ACCESS_TOKEN=ya29.xxx...
    export GOOGLE_PROJECT_ID=your-project-id
    python3 generate-gemini-vertex.py "prompt" output.png

    # Option 3: With service account key
    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
    export GOOGLE_PROJECT_ID=your-project-id
    python3 generate-gemini-vertex.py "prompt" output.png
"""
import os
import sys
import json
import base64
import subprocess
import urllib.request
import urllib.error

# Configuration
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
ACCESS_TOKEN = os.getenv("GOOGLE_ACCESS_TOKEN")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def get_access_token():
    """Get access token from gcloud or environment."""
    global ACCESS_TOKEN

    # Check if already set
    if ACCESS_TOKEN:
        return ACCESS_TOKEN

    # Try gcloud
    try:
        result = subprocess.run(
            ["gcloud", "auth", "application-default", "print-access-token"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except FileNotFoundError:
        pass  # gcloud not installed

    # Try service account
    if CREDENTIALS_PATH and os.path.exists(CREDENTIALS_PATH):
        try:
            import google.auth.transport.requests
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(
                CREDENTIALS_PATH,
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            credentials.refresh(google.auth.transport.requests.Request())
            return credentials.token
        except Exception as e:
            print(f"⚠️  Service account error: {e}")

    return None

def get_project_id():
    """Get project ID from environment or gcloud config."""
    global PROJECT_ID

    if PROJECT_ID:
        return PROJECT_ID

    # Try gcloud config
    try:
        result = subprocess.run(
            ["gcloud", "config", "get", "project"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except FileNotFoundError:
        pass

    return None

# Main execution
def main():
    # Check project ID
    PROJECT_ID = get_project_id()
    if not PROJECT_ID:
        print("❌ GOOGLE_PROJECT_ID not found")
        print("\nSetup options:")
        print("1. Install gcloud CLI and run: gcloud config set project YOUR_PROJECT_ID")
        print("2. Or set: export GOOGLE_PROJECT_ID=your-project-id")
        sys.exit(1)

    # Get access token
    ACCESS_TOKEN = get_access_token()
    if not ACCESS_TOKEN:
        print("❌ No access token available")
        print("\nAuthentication options:")
        print("1. Install gcloud CLI and run: gcloud auth application-default login")
        print("2. Or set: export GOOGLE_ACCESS_TOKEN=ya29.xxx...")
        print("3. Or set: export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json")
        sys.exit(1)

    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python3 generate-gemini-vertex.py \"prompt\" [output_path]")
        sys.exit(1)

    prompt = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "gemini-output.png"

    print(f"🎨 Generating with Gemini 3 Pro Image Preview (Vertex AI)...")
    print(f"📝 Project: {PROJECT_ID}")
    print(f"📝 Prompt: {prompt[:80]}...")

    # Vertex AI API endpoint
    url = f"https://aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/global/publishers/google/models/gemini-3-pro-image-preview:generateContent"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "contents": {
            "role": "user",
            "parts": {
                "text": prompt
            }
        },
        "generation_config": {
            "response_modalities": ["TEXT", "IMAGE"]
        }
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers)

        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))

        # Parse response
        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            content = candidate.get('content', {})

            if 'parts' in content and len(content['parts']) > 0:
                for part in content['parts']:
                    if 'inline_data' in part:
                        image_b64 = part['inline_data']['data']
                        image_bytes = base64.b64decode(image_b64)

                        with open(output, 'wb') as f:
                            f.write(image_bytes)

                        print("✅ Image generated successfully!")
                        print(f"💾 Saved to: {output}")
                        return
                    elif 'text' in part:
                        print(f"⚠️  Got text: {part['text'][:100]}...")

            print(f"❌ No image in response")
            print(f"Response: {json.dumps(result, indent=2)[:500]}")
        else:
            print(f"❌ Unexpected response: {result}")

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.headers.get('content-length') else str(e)
        print(f"❌ HTTP Error {e.code}: {error_body}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
