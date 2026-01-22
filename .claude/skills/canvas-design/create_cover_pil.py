#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import math
import random

# Canvas dimensions
WIDTH = 1200
HEIGHT = 1600

# Create image
img = Image.new('RGB', (WIDTH, HEIGHT), color=(5, 10, 20))
draw = ImageDraw.Draw(img)

# Color definitions
stage1_primary = (77, 89, 102)
stage1_secondary = (51, 64, 76)

stage2_primary = (0, 153, 166)
stage2_secondary = (26, 102, 128)

stage3_primary = (77, 128, 242)
stage3_secondary = (153, 77, 217)
stage3_accent = (242, 102, 77)

# Helper functions
def circle(x, y, r, color):
    draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

def line(x1, y1, x2, y2, color, width=1):
    draw.line([x1, y1, x2, y2], fill=color, width=width)

# Subtle grid pattern
for i in range(0, WIDTH, 60):
    line(i, 0, i, HEIGHT, (26, 31, 38), 1)
for i in range(0, HEIGHT, 60):
    line(0, i, WIDTH, i, (26, 31, 38), 1)

# STAGE 1: Simple Completions
y1_start = int(HEIGHT * 0.75)
for i in range(8):
    x = 150 + i * 120
    y = y1_start + (i % 3) * 40
    r = 8 + (i % 3) * 4
    circle(x, y, r, stage1_primary)
    if i < 7:
        line(x + r, y, x + 120 - r, y + ((i+1) % 3) * 40, stage1_secondary, 1)

# STAGE 2: Chat/Interaction
y2_start = int(HEIGHT * 0.45)
for i in range(12):
    x = 100 + i * 90
    if i % 2 == 0:
        y = y2_start
        r = 12
        color = stage2_primary
    else:
        y = y2_start + 70
        r = 10
        color = stage2_secondary
    circle(x, y, r, color)
    if i % 2 == 1:
        line(x - 90, y2_start, x, y, stage2_secondary, 2)
    if i < 11 and i % 2 == 0:
        line(x + 12, y2_start, x + 90 - 10, y2_start, stage2_secondary, 2)

# STAGE 3: Agentic/Complex
y3_start = int(HEIGHT * 0.15)
random.seed(42)
nodes = []
for i in range(18):
    x = int(80 + random.random() * 1040)
    y = int(y3_start + random.random() * 200)
    r = int(6 + random.random() * 8)
    nodes.append((x, y, r))

    pos_factor = x / WIDTH
    if pos_factor < 0.33:
        color = stage3_secondary
    elif pos_factor < 0.66:
        color = stage3_primary
    else:
        color = stage3_accent
    circle(x, y, r, color)

# Complex interconnections
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        x1, y1, r1 = nodes[i]
        x2, y2, r2 = nodes[j]
        dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if dist < 180:
            alpha = int(max(30, 100 - dist*2.5))
            color = (*stage3_primary, alpha) if len(stage3_primary) == 3 else stage3_primary
            # PIL doesn't support alpha in line directly, use darker color
            line_color = tuple(max(0, c - alpha//4) for c in stage3_primary)
            line(x1, y1, x2, y2, line_color, 1)

# Stage dividers
for y_div in [int(HEIGHT * 0.35), int(HEIGHT * 0.68)]:
    line(80, y_div, WIDTH - 80, y_div, (38, 51, 64), 2)

# Evolution arrows
for y_pos, arrow_color in [(int(HEIGHT * 0.69), stage1_secondary), (int(HEIGHT * 0.43), stage2_secondary)]:
    x_center = WIDTH // 2
    line(x_center, y_pos, x_center, y_pos - 25, arrow_color, 3)
    # Arrow head
    draw.polygon([
        (x_center - 6, y_pos - 18),
        (x_center, y_pos - 28),
        (x_center + 6, y_pos - 18)
    ], fill=arrow_color)

# Labels - using default font
try:
    font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    font_small = ImageFont.truetype("/System/Library/Fonts/Courier.dfont", 11)
    font_tiny = ImageFont.truetype("/System/Library/Fonts/Courier.dfont", 9)
except:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_tiny = ImageFont.load_default()

# Main title
draw.text((80, 60), "LLM API", fill=(242, 247, 255), font=font_large)
draw.text((80, 95), "形态演进", fill=(242, 247, 255), font=font_medium)

# Stage labels
draw.text((150, int(HEIGHT * 0.91)), "/v1/completions", fill=(102, 115, 128), font=font_small)
draw.text((150, int(HEIGHT * 0.61)), "/v1/chat/completions", fill=(0, 128, 140), font=font_small)
draw.text((150, int(HEIGHT * 0.31)), "/v1/responses", fill=(102, 128, 230), font=font_small)

# Technical annotation
draw.text((80, HEIGHT - 60), "API EVOLUTION: COMPLETIONS → CHAT → AGENTIC",
         fill=(128, 140, 166), font=font_tiny)

# Save
output_path = "/Users/magooup/workspace/default/research/articlewrite/llm-agentic-api/cover.png"
img.save(output_path, "PNG", quality=95)
print(f"Cover created: {output_path}")
