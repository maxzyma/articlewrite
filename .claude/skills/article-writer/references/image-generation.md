# Image Generation Reference

Detailed patterns for generating article images on macOS.

## PIL Python Infographics

Best for: evolution chains, comparison cards, custom flowcharts, any layout needing precise control.

### Reliable Chinese Fonts (macOS)

| Font | Path | Notes |
|------|------|-------|
| **STHeiti Light** | `/System/Library/Fonts/STHeiti Light.ttc` | Primary choice |
| Hiragino Sans GB | `/System/Library/Fonts/Hiragino Sans GB.ttc` | Fallback |
| Arial Unicode | `/Library/Fonts/Arial Unicode.ttf` | Broad coverage |

**PingFang.ttc does NOT work** with PIL — avoid.

### Card-Based Infographic Pattern

Proven layout for "evolution chain" or "multi-item comparison" visuals (1200×440px):

```python
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 440
img = Image.new('RGB', (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

# Fonts
font_title = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 22)
font_body = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 13)

# Card with shadow
def draw_card(draw, x, y, w, h, header_color):
    # Shadow
    draw.rounded_rectangle((x+3, y+3, x+w+3, y+h+3), radius=16, fill=(230,230,230))
    # Card body
    draw.rounded_rectangle((x, y, x+w, y+h), radius=16, fill=(255,255,255), outline=(220,220,220))
    # Header band
    draw.rounded_rectangle((x, y, x+w, y+80), radius=16, fill=header_color)
    draw.rectangle((x, y+64, x+w, y+80), fill=header_color)  # Fix bottom corners

# Arrow between cards
def draw_arrow(draw, x1, y, x2, label, font):
    draw.line([(x1, y), (x2-8, y)], fill=(180,180,180), width=2)
    draw.polygon([(x2, y), (x2-10, y-6), (x2-10, y+6)], fill=(180,180,180))
    bbox = draw.textbbox((0,0), label, font=font)
    draw.text(((x1+x2)//2 - (bbox[2]-bbox[0])//2, y-22), label, fill=(150,150,150), font=font)

# Save at retina DPI
img.save('output.png', 'PNG', dpi=(144, 144))
```

### Key Techniques

- **Shadow effect**: Draw rounded rect offset by (3,3) in gray before the white card
- **Header band fix**: After drawing rounded header, fill a rectangle to square off bottom corners
- **Centered text**: Use `textbbox()` to measure width, then `(container_w - text_w) // 2`
- **Color badges**: Small rounded rectangles with text for tags/labels
- **Attribute rows**: Label (left) + value (right) + separator line, incrementing y by 32px
- **Always save DPI 144**: `img.save(path, 'PNG', dpi=(144, 144))` for retina displays
- **Clean up scripts**: Delete `gen_*.py` after successful generation

### VS Comparison Layout Pattern

Two-panel layout (1200×500px) with "VS" divider:

- Left panel: Problem/old approach (warm color: green/orange)
- Right panel: Solution/new approach (cool color: purple/blue)
- Center: Rounded "VS" badge
- Bottom of each panel: callout box (problem/advantage summary)

For circular flow diagrams in the right panel, use `math.cos/sin` to position nodes.

## AntV Chart MCP (`mcp-server-chart`)

Best for: data-driven visualizations with standard chart types.

### Hand-Drawn Style

Always use `texture: "rough"` for blog-friendly aesthetics:

```json
{
  "style": {
    "texture": "rough",
    "backgroundColor": "#fff",
    "palette": ["#a855f7", "#10b981"]
  }
}
```

### Recommended Chart Types for Articles

| Chart Type | Use Case | Tool Function |
|-----------|----------|---------------|
| **Radar** | Multi-dimension comparison (A vs B) | `generate_radar_chart` |
| **Column** | Category comparison | `generate_column_chart` (group: true) |
| **Area** | Trend over time | `generate_area_chart` |
| **Bar** | Horizontal category comparison | `generate_bar_chart` |
| **Flow** | Simple process flows | `generate_flow_diagram` |

### Gotchas

- **Mind maps have excessive whitespace** — avoid for tight layouts; use PIL instead
- **Flow diagrams may be too sparse** — add more nodes or use PIL for complex flows
- **Returns a URL** — must `curl -sL <url> -o local-path.png` to download
- **Chinese text renders correctly** in chart labels and titles
- **Width/height**: Default 600×400. For articles, use 800×500 for charts

### Radar Chart Data Format

```json
[
  {"name": "维度A", "value": 90, "group": "Product X"},
  {"name": "维度A", "value": 60, "group": "Product Y"},
  {"name": "维度B", "value": 70, "group": "Product X"},
  {"name": "维度B", "value": 85, "group": "Product Y"}
]
```

## Workflow Summary

1. Identify 3-5 key visual opportunities in the article
2. Classify each by type (infographic / data chart / AI art)
3. Create `images/` directory
4. Generate in parallel when independent (PIL scripts + AntV calls)
5. Download AntV outputs to local `images/`
6. Read each PNG to visually verify quality
7. Insert `![alt](images/fig-name.png)` at relevant article positions
8. Delete generation scripts
9. Commit images + article changes
