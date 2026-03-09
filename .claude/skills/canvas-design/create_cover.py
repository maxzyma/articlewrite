#!/usr/bin/env python3
import cairo
import math

# Canvas dimensions (portrait for cover)
WIDTH = 1200
HEIGHT = 1600

# Create surface
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

# Background - deep, technical blue-black
ctx.set_source_rgb(0.02, 0.04, 0.08)
ctx.paint()

# Define color progression for three stages
stage1_primary = (0.3, 0.35, 0.4)
stage1_secondary = (0.2, 0.25, 0.3)

stage2_primary = (0.0, 0.6, 0.65)
stage2_secondary = (0.1, 0.4, 0.5)

stage3_primary = (0.3, 0.5, 0.95)
stage3_secondary = (0.6, 0.3, 0.85)
stage3_accent = (0.95, 0.4, 0.3)

# Helper function for drawing circles
def circle(x, y, r, color):
    ctx.set_source_rgb(*color)
    ctx.arc(x, y, r, 0, 2 * math.pi)
    ctx.fill()

# Helper function for drawing lines
def line(x1, y1, x2, y2, color, width=1):
    ctx.set_source_rgb(*color)
    ctx.set_line_width(width)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# STAGE 1: Simple Completions (bottom third)
y1_start = HEIGHT * 0.75
for i in range(8):
    x = 150 + i * 120
    y = y1_start + (i % 3) * 40
    r = 8 + (i % 3) * 4
    circle(x, y, r, stage1_primary)
    if i < 7:
        line(x + r, y, x + 120 - r, y + ((i+1) % 3) * 40, stage1_secondary, 0.5)

# Stage 1 label
ctx.set_source_rgb(0.4, 0.45, 0.5)
ctx.set_font_size(11)
ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.move_to(150, HEIGHT * 0.92)
ctx.show_text("/v1/completions")

# STAGE 2: Chat/Interaction (middle third)
y2_start = HEIGHT * 0.45
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
        line(x - 90, y2_start, x, y, stage2_secondary, 1.5)
    if i < 11 and i % 2 == 0:
        line(x + 12, y2_start, x + 90 - 10, y2_start, stage2_secondary, 1)

# Stage 2 label
ctx.set_source_rgb(0.0, 0.5, 0.55)
ctx.set_font_size(11)
ctx.move_to(150, HEIGHT * 0.62)
ctx.show_text("/v1/chat/completions")

# STAGE 3: Agentic/Complex (top third)
import random
y3_start = HEIGHT * 0.15
nodes = []
for i in range(18):
    random.seed(42 + i)
    x = 80 + random.random() * 1040
    y = y3_start + random.random() * 200
    r = 6 + random.random() * 8
    nodes.append((x, y, r))

    pos_factor = (x / WIDTH)
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
            alpha = max(0.1, 0.4 - dist/450)
            ctx.set_source_rgba(stage3_primary[0], stage3_primary[1], stage3_primary[2], alpha)
            ctx.set_line_width(0.5)
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()

# Stage 3 label
ctx.set_source_rgb(0.4, 0.5, 0.9)
ctx.set_font_size(11)
ctx.move_to(150, HEIGHT * 0.32)
ctx.show_text("/v1/responses")

# Evolution arrows
for y_pos, arrow_color in [(HEIGHT * 0.69, (0.3, 0.4, 0.45)), (HEIGHT * 0.43, (0.0, 0.45, 0.5))]:
    ctx.set_source_rgb(*arrow_color)
    ctx.set_line_width(1.5)
    ctx.move_to(WIDTH * 0.5, y_pos)
    ctx.line_to(WIDTH * 0.5, y_pos - 25)
    ctx.stroke()
    ctx.move_to(WIDTH * 0.5 - 6, y_pos - 18)
    ctx.line_to(WIDTH * 0.5, y_pos - 28)
    ctx.line_to(WIDTH * 0.5 + 6, y_pos - 18)
    ctx.close_path()
    ctx.fill()

# Main title
ctx.set_source_rgb(0.95, 0.97, 1.0)
ctx.set_font_size(28)
ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.move_to(80, 80)
ctx.show_text("LLM API")

ctx.set_font_size(20)
ctx.move_to(80, 110)
ctx.show_text("形态演进")

# Technical annotation
ctx.set_source_rgb(0.5, 0.55, 0.65)
ctx.set_font_size(9)
ctx.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.move_to(80, HEIGHT - 60)
ctx.show_text("API EVOLUTION: COMPLETIONS → CHAT → AGENTIC")

# Subtle grid pattern
ctx.set_source_rgba(0.1, 0.12, 0.15, 0.3)
ctx.set_line_width(0.5)
for i in range(0, WIDTH, 60):
    ctx.move_to(i, 0)
    ctx.line_to(i, HEIGHT)
    ctx.stroke()
for i in range(0, HEIGHT, 60):
    ctx.move_to(0, i)
    ctx.line_to(WIDTH, i)
    ctx.stroke()

# Stage dividers
for y_div in [HEIGHT * 0.35, HEIGHT * 0.68]:
    ctx.set_source_rgba(0.15, 0.2, 0.25, 0.5)
    ctx.set_line_width(1)
    ctx.move_to(80, y_div)
    ctx.line_to(WIDTH - 80, y_div)
    ctx.stroke()

# Save
output_path = "/Users/magooup/workspace/default/research/articlewrite/llm-agentic-api/cover.png"
surface.write_to_png(output_path)
surface.finish()

print(f"Cover created: {output_path}")
