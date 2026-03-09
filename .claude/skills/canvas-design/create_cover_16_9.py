#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import math
import random

# Canvas dimensions - 16:9 landscape ratio
WIDTH = 1920
HEIGHT = 1080

# Create image
img = Image.new('RGB', (WIDTH, HEIGHT), color=(5, 10, 20))
draw = ImageDraw.Draw(img)

# Color definitions - progressive evolution
stage1_primary = (77, 89, 102)      # Simple gray-blue
stage1_secondary = (51, 64, 76)

stage2_primary = (0, 153, 166)       # Teal/cyan
stage2_secondary = (26, 102, 128)

stage3_primary = (77, 128, 242)      # Bright blue
stage3_secondary = (153, 77, 217)   # Purple
stage3_accent = (242, 102, 77)      # Orange accent

# Helper functions
def circle(x, y, r, color):
    draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

def line(x1, y1, x2, y2, color, width=1):
    draw.line([x1, y1, x2, y2], fill=color, width=width)

# Subtle grid pattern
for i in range(0, WIDTH, 80):
    line(i, 0, i, HEIGHT, (26, 31, 38), 1)
for i in range(0, HEIGHT, 80):
    line(0, i, WIDTH, i, (26, 31, 38), 1)

# Three horizontal zones representing API evolution
# Zone 1: Simple Completions (left)
x1_center = int(WIDTH * 0.17)
for i in range(6):
    x = x1_center - 150 + i * 60
    y = HEIGHT // 2 + (i % 2) * 50 - 25
    r = 10 + (i % 2) * 5
    circle(x, y, r, stage1_primary)
    if i < 5:
        line(x + r, y, x + 60 - r, HEIGHT // 2 + ((i+1) % 2) * 50 - 25, stage1_secondary, 2)

# Zone 2: Chat/Interaction (center)
x2_center = int(WIDTH * 0.5)
for i in range(10):
    x = x2_center - 200 + i * 45
    if i % 2 == 0:
        y = HEIGHT // 2 - 60
        r = 14
        color = stage2_primary
    else:
        y = HEIGHT // 2 + 60
        r = 12
        color = stage2_secondary
    circle(x, y, r, color)
    if i % 2 == 1:
        line(x - 45, HEIGHT // 2 - 60, x, y, stage2_secondary, 3)
    if i < 9 and i % 2 == 0:
        line(x + 14, HEIGHT // 2 - 60, x + 45 - 12, HEIGHT // 2 - 60, stage2_secondary, 2)

# Zone 3: Agentic/Complex (right)
x3_start = int(WIDTH * 0.72)
random.seed(42)
nodes = []
for i in range(15):
    x = int(x3_start + random.random() * 420)
    y = int(HEIGHT * 0.25 + random.random() * HEIGHT * 0.5)
    r = int(6 + random.random() * 10)
    nodes.append((x, y, r))

    pos_factor = (x - x3_start) / 420
    if pos_factor < 0.33:
        color = stage3_secondary
    elif pos_factor < 0.66:
        color = stage3_primary
    else:
        color = stage3_accent
    circle(x, y, r, color)

# Complex interconnections in zone 3
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        x1, y1, r1 = nodes[i]
        x2, y2, r2 = nodes[j]
        dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if dist < 200:
            alpha = int(max(30, 120 - dist*2))
            line_color = tuple(max(0, c - alpha//4) for c in stage3_primary)
            line(x1, y1, x2, y2, line_color, 2)

# Evolution arrows between zones
arrow_y = HEIGHT // 2
for x_arrow, arrow_color in [(int(WIDTH * 0.32), stage1_secondary), (int(WIDTH * 0.68), stage2_secondary)]:
    line(x_arrow, arrow_y, x_arrow + 60, arrow_y, arrow_color, 4)
    # Arrow head
    draw.polygon([
        (x_arrow + 60, arrow_y),
        (x_arrow + 45, arrow_y - 8),
        (x_arrow + 45, arrow_y + 8)
    ], fill=arrow_color)

# Vertical dividers between zones
for x_div in [int(WIDTH * 0.33), int(WIDTH * 0.66)]:
    line(x_div, HEIGHT * 0.15, x_div, HEIGHT * 0.85, (38, 51, 64), 3)

# Load fonts
try:
    font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
    font_subtitle = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
    font_label = ImageFont.truetype("/System/Library/Fonts/Courier.dfont", 18)
    font_small = ImageFont.truetype("/System/Library/Fonts/Courier.dfont", 14)
except:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_label = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Main title
draw.text((100, 80), "LLM API 形态演进", fill=(242, 247, 255), font=font_title)
draw.text((100, 140), "从简单完成到智能代理", fill=(180, 190, 200), font=font_subtitle)

# Stage labels (positioned in each zone)
draw.text((int(WIDTH * 0.08), HEIGHT - 150), "/v1/completions", fill=(102, 115, 128), font=font_label)
draw.text((int(WIDTH * 0.08), HEIGHT - 120), "简单文本生成", fill=(77, 89, 102), font=font_small)

draw.text((int(WIDTH * 0.41), HEIGHT - 150), "/v1/chat/completions", fill=(0, 140, 150), font=font_label)
draw.text((int(WIDTH * 0.41), HEIGHT - 120), "对话式交互", fill=(0, 120, 130), font=font_small)

draw.text((int(WIDTH * 0.75), HEIGHT - 150), "/v1/responses", fill=(102, 128, 230), font=font_label)
draw.text((int(WIDTH * 0.75), HEIGHT - 120), "智能代理系统", fill=(77, 102, 200), font=font_small)

# Technical annotation
draw.text((100, HEIGHT - 60), "API EVOLUTION: COMPLETIONS → CHAT → AGENTIC",
         fill=(128, 140, 166), font=font_small)

# Save
output_path = "/Users/magooup/workspace/default/research/articlewrite/llm-agentic-api/cover.png"
img.save(output_path, "PNG", quality=95)
print(f"Cover created: {output_path}")
