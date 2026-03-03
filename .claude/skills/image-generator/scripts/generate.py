#!/usr/bin/env python3
"""
Image Generator - Quality-focused AI image generation.

Supports:
  - Gemini (via AI Studio API Key) — Recommended first choice
  - OpenAI DALL-E 3 — Highest quality, best text rendering

Usage:
    # Gemini (Recommended)
    export GEMINI_API_KEY=AIza...
    python3 scripts/generate.py "prompt" --service gemini

    # OpenAI DALL-E 3
    export OPENAI_API_KEY=sk-...
    python3 scripts/generate.py "prompt" --service openai
"""
import os
import sys
import json
import base64
import argparse
import urllib.request
import urllib.error

from pathlib import Path


class ImageGenerator:
    """Quality-focused image generator: Gemini + DALL-E."""

    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")

    def generate_with_gemini(
        self, prompt: str, width: int = 1920, height: int = 1080
    ) -> bytes:
        """Generate image using Gemini via AI Studio API.

        API docs: https://ai.google.dev/gemini-api/docs/image-generation
        """
        if not self.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY not set\n"
                "Get your key at: https://aistudio.google.com/apikey\n"
                "Set with: export GEMINI_API_KEY=AIza..."
            )

        print(f"Generating with Gemini...")
        print(f"Prompt: {prompt[:100]}...")

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.0-flash-exp:generateContent?key={self.gemini_api_key}"
        )

        headers = {"Content-Type": "application/json"}

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"]
            }
        }

        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=headers)

            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode('utf-8'))

            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                content = candidate.get('content', {})

                if 'parts' in content and len(content['parts']) > 0:
                    for part in content['parts']:
                        if 'inlineData' in part:
                            image_b64 = part['inlineData']['data']
                            print("Image generated successfully!")
                            return base64.b64decode(image_b64)
                        elif 'text' in part:
                            print(f"Got text response: {part['text'][:100]}...")

                raise ValueError("No image found in response")
            else:
                raise ValueError(f"Unexpected response format: {json.dumps(result)[:500]}")

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.headers.get('content-length') else str(e)
            raise ValueError(f"HTTP Error {e.code}: {error_body}")

    def generate_with_openai(
        self, prompt: str, size: str = "1792x1024"
    ) -> bytes:
        """Generate image using OpenAI DALL-E 3."""
        if not self.openai_key:
            raise ValueError(
                "OPENAI_API_KEY not set\n"
                "Get your key at: https://platform.openai.com/api-keys\n"
                "Set with: export OPENAI_API_KEY=sk-..."
            )

        print(f"Generating with DALL-E 3...")
        print(f"Prompt: {prompt[:100]}...")

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
            print("Image generated successfully!")
            return img_response.read()

    def save(self, image_data: bytes, output_path: str) -> str:
        """Save image to file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(image_data)

        print(f"Saved to: {output_path.absolute()}")
        return str(output_path.absolute())


def main():
    parser = argparse.ArgumentParser(
        description="Quality-focused AI image generation (Gemini + DALL-E)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Services:
  gemini    Gemini via AI Studio API Key (recommended)
  openai    DALL-E 3 - highest quality, best text rendering

Examples:
  %(prog)s "A cute cat" --service gemini
  %(prog)s "Cyberpunk city" --service openai --output cover.png
  %(prog)s "Abstract art" --width 1920 --height 1080
        """
    )

    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument(
        "-s", "--service",
        default="gemini",
        choices=["gemini", "openai"],
        help="Service to use (default: gemini)"
    )
    parser.add_argument(
        "-o", "--output",
        default="./generated_image.png",
        help="Output path (default: ./generated_image.png)"
    )
    parser.add_argument("--width", type=int, default=1920, help="Image width (default: 1920)")
    parser.add_argument("--height", type=int, default=1080, help="Image height (default: 1080)")

    args = parser.parse_args()

    try:
        generator = ImageGenerator()

        if args.service == "gemini":
            image_data = generator.generate_with_gemini(args.prompt, args.width, args.height)
        elif args.service == "openai":
            size = f"{args.width}x{args.height}"
            image_data = generator.generate_with_openai(args.prompt, size)

        output_path = generator.save(image_data, args.output)
        print(f"\nComplete! Image saved to: {output_path}")

    except KeyboardInterrupt:
        print("\nCancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
