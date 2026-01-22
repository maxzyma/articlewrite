#!/usr/bin/env python3
"""
Universal Image Generator
Supports multiple AI image generation services.
"""
import os
import sys
import argparse
import base64
from pathlib import Path

try:
    import requests
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("\nInstall with: pip install requests python-dotenv")
    sys.exit(1)

# Load environment variables from project root
load_dotenv()


class ImageGenerator:
    """Universal image generator supporting multiple services."""

    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.stability_key = os.getenv("STABILITY_API_KEY")

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

        encoded_prompt = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        params = {"width": width, "height": height, "nologo": True, "enhance": True}

        response = requests.get(url, params=params, timeout=120)
        response.raise_for_status()

        print("✅ Image generated successfully!")
        return response.content

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

        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()

        image_url = response.json()["data"][0]["url"]
        img_response = requests.get(image_url, timeout=30)
        img_response.raise_for_status()

        print("✅ Image generated successfully!")
        return img_response.content

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

        data = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "steps": 30,
            "samples": 1
        }

        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()

        image_b64 = response.json()["artifacts"][0]["base64"]
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
  pollinations    Free, no API key needed (recommended)
  openai          Requires OPENAI_API_KEY
  stability       Requires STABILITY_API_KEY

Examples:
  # Free service
  %(prog)s "A cute cat" --service pollinations

  # DALL-E (16:9 cover)
  %(prog)s "Cyberpunk city" --service openai --output cover.png

  # Custom size
  %(prog)s "Abstract art" --service pollinations --width 1920 --height 1080
        """
    )

    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument(
        "-s", "--service",
        default="pollinations",
        choices=["pollinations", "openai", "stability"],
        help="Service to use (default: pollinations, FREE)"
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
        if args.service == "pollinations":
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
