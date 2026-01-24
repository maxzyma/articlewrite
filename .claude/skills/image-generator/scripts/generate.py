#!/usr/bin/env python3
"""
Universal Image Generator
Supports multiple AI image generation services including Gemini 3 Pro (Vertex AI).

Usage:
    # Gemini via Vertex AI (Recommended - First Choice)
    # Requires: gcloud CLI and authentication
    export GOOGLE_PROJECT_ID=your-project-id
    gcloud auth application-default login
    python3 scripts/generate.py "prompt" --service gemini --width 1920 --height 1080

    # Or with access token directly
    export GOOGLE_ACCESS_TOKEN=ya29.xxx...
    export GOOGLE_PROJECT_ID=your-project-id
    python3 scripts/generate.py "prompt" --service gemini

    # Pollinations.ai (Free, no API key)
    python3 scripts/generate.py "prompt" --service pollinations

    # OpenAI DALL-E 3
    export OPENAI_API_KEY=sk-...
    python3 scripts/generate.py "prompt" --service openai
"""
import os
import sys
import json
import base64
import argparse
import subprocess
import urllib.request
import urllib.error

from pathlib import Path


class ImageGenerator:
    """Universal image generator supporting multiple services."""

    def __init__(self):
        self.gemini_project_id = os.getenv("GOOGLE_PROJECT_ID")
        self.gemini_access_token = os.getenv("GOOGLE_ACCESS_TOKEN")
        self.gemini_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.stability_key = os.getenv("STABILITY_API_KEY")

    def _get_gemini_token(self) -> str:
        """Get access token for Vertex AI."""
        # Check if already set
        if self.gemini_access_token:
            return self.gemini_access_token

        # Try gcloud
        try:
            result = subprocess.run(
                ["gcloud", "auth", "application-default", "print-access-token"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except FileNotFoundError:
            pass

        # Try service account
        if self.gemini_credentials and os.path.exists(self.gemini_credentials):
            try:
                from google.auth.transport.requests import Request
                from google.oauth2 import service_account

                credentials = service_account.Credentials.from_service_account_file(
                    self.gemini_credentials,
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
                credentials.refresh(Request())
                return credentials.token
            except Exception as e:
                print(f"⚠️  Service account error: {e}")

        return None

    def generate_with_gemini(
        self, prompt: str, width: int = 1920, height: int = 1080
    ) -> bytes:
        """Generate image using Gemini 3 Pro Image Preview via Vertex AI API.

        Based on: https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/gemini-3-pro-image-preview

        Args:
            prompt: Image description
            width: Image width
            height: Image height

        Returns:
            Image bytes
        """
        # Check project ID
        if not self.gemini_project_id:
            raise ValueError(
                "❌ GOOGLE_PROJECT_ID not set\n"
                "Set with: export GOOGLE_PROJECT_ID=your-project-id\n"
                "Or run: gcloud config set project YOUR_PROJECT_ID"
            )

        # Get access token
        access_token = self._get_gemini_token()
        if not access_token:
            raise ValueError(
                "❌ No access token available\n"
                "Options:\n"
                "1. Install gcloud and run: gcloud auth application-default login\n"
                "2. Set: export GOOGLE_ACCESS_TOKEN=ya29.xxx...\n"
                "3. Set: export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json"
            )

        print(f"🎨 Generating with Gemini 3 Pro Image Preview (Vertex AI)...")
        print(f"📝 Prompt: {prompt[:100]}...")

        # Vertex AI API endpoint
        url = (
            f"https://aiplatform.googleapis.com/v1/projects/{self.gemini_project_id}"
            f"/locations/global/publishers/google/models/gemini-3-pro-image-preview:generateContent"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "contents": {
                "role": "user",
                "parts": {"text": prompt}
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
                            print("✅ Image generated successfully!")
                            return base64.b64decode(image_b64)
                        elif 'text' in part:
                            print(f"⚠️  Got text response: {part['text'][:100]}...")

                raise ValueError("No image found in response")
            else:
                raise ValueError(f"Unexpected response format: {result}")

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.headers.get('content-length') else str(e)
            raise ValueError(f"HTTP Error {e.code}: {error_body}")

    def generate_with_pollinations(
        self, prompt: str, width: int = 1920, height: int = 1080
    ) -> bytes:
        """Generate image using Pollinations.ai (FREE, no API key needed).

        Args:
            prompt: Image description
            width: Image width
            height: Image height

        Returns:
            Image bytes
        """
        print(f"🎨 Generating with Pollinations.ai...")
        print(f"📝 Prompt: {prompt[:100]}...")

        import urllib.parse
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=True&enhance=True"

        try:
            with urllib.request.urlopen(url, timeout=120) as response:
                print("✅ Image generated successfully!")
                return response.read()
        except Exception as e:
            raise ValueError(f"Pollinations API error: {e}")

    def generate_with_openai(
        self, prompt: str, size: str = "1792x1024"
    ) -> bytes:
        """Generate image using OpenAI DALL-E (requires API key).

        Args:
            prompt: Image description
            size: Image size (e.g., "1792x1024" for 16:9)

        Returns:
            Image bytes
        """
        if not self.openai_key:
            raise ValueError("❌ OPENAI_API_KEY not found in environment")

        print(f"🎨 Generating with DALL-E 3...")
        print(f"📝 Prompt: {prompt[:100]}...")

        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": size,
            "quality": "hd"
        }

        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))

        image_url = result["data"][0]["url"]
        with urllib.request.urlopen(image_url, timeout=30) as img_response:
            print("✅ Image generated successfully!")
            return img_response.read()

    def generate_with_stability(
        self, prompt: str, width: int = 1344, height: int = 768
    ) -> bytes:
        """Generate image using Stability AI (requires API key).

        Args:
            prompt: Image description
            width: Image width
            height: Image height

        Returns:
            Image bytes
        """
        if not self.stability_key:
            raise ValueError("❌ STABILITY_API_KEY not found in environment")

        print(f"🎨 Generating with Stability AI...")
        print(f"📝 Prompt: {prompt[:100]}...")

        model = "stable-diffusion-xl-1024-v1-0"
        url = f"https://api.stability.ai/v1/generation/{model}/text-to-image"

        headers = {
            "Authorization": f"Bearer {self.stability_key}",
            "Content-Type": "application/json"
        }

        data = json.dumps({
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "steps": 30,
            "samples": 1
        }).encode('utf-8')

        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))

        image_b64 = result["artifacts"][0]["base64"]
        image_bytes = base64.b64decode(image_b64)

        print("✅ Image generated successfully!")
        return image_bytes

    def save(self, image_data: bytes, output_path: str) -> str:
        """Save image to file.

        Args:
            image_data: Image bytes
            output_path: Output file path

        Returns:
            Absolute path to saved file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(image_data)

        print(f"💾 Saved to: {output_path.absolute()}")
        return str(output_path.absolute())


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI images using multiple services",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Services:
  gemini          Gemini 3 Pro Image Preview (recommended first choice)
  pollinations    Free, no API key needed
  openai          Requires OPENAI_API_KEY
  stability       Requires STABILITY_API_KEY

Examples:
  # Gemini (recommended)
  %(prog)s "A cute cat" --service gemini

  # Free service
  %(prog)s "A cute cat" --service pollinations

  # DALL-E (16:9 cover)
  %(prog)s "Cyberpunk city" --service openai --output cover.png

  # Custom size
  %(prog)s "Abstract art" --service gemini --width 1920 --height 1080
        """
    )

    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument(
        "-s", "--service",
        default="gemini",
        choices=["gemini", "pollinations", "openai", "stability"],
        help="Service to use (default: gemini, recommended)"
    )
    parser.add_argument(
        "-o", "--output",
        default="./generated_image.png",
        help="Output path (default: ./generated_image.png)"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1920,
        help="Image width (default: 1920)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1080,
        help="Image height (default: 1080)"
    )

    args = parser.parse_args()

    try:
        generator = ImageGenerator()

        # Generate based on service
        if args.service == "gemini":
            image_data = generator.generate_with_gemini(
                args.prompt, args.width, args.height
            )
        elif args.service == "pollinations":
            image_data = generator.generate_with_pollinations(
                args.prompt, args.width, args.height
            )
        elif args.service == "openai":
            size = f"{args.width}x{args.height}"
            image_data = generator.generate_with_openai(args.prompt, size)
        elif args.service == "stability":
            image_data = generator.generate_with_stability(
                args.prompt, args.width, args.height
            )

        # Save image
        output_path = generator.save(image_data, args.output)
        print(f"\n🎉 Complete! Image saved to: {output_path}")

    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
