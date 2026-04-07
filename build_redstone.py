"""
Build Minecraft redstone circuit images for GitHub profile.
Uses known coordinates from power.png to extract the cross,
then derives EW/NS wire from it.
"""
from PIL import Image
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
REF = "C:/Users/arthu/OneDrive/Bureau/moi/git"
OUT = "assets"

def keep_redstone(img):
    """Keep only red and black pixels, rest -> transparent."""
    w, h = img.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            r, g, b, a = img.getpixel((x, y))
            is_red = r > 80 and g < 60 and b < 60 and r > g * 1.8
            is_black = r < 35 and g < 35 and b < 35
            if is_red or is_black:
                out.putpixel((x, y), (r, g, b, 255))
    return out

# ============================================================
# EXTRACT CROSS from power.png with known coordinates
# ============================================================
power = Image.open(f"{REF}/power.png").convert("RGBA")

# Known from analysis: first cross (brightest) at x=130-277, y=296-453
cross_crop = power.crop((130, 296, 278, 454))
cross_filtered = keep_redstone(cross_crop)
cross_filtered.save(f"{OUT}/cross_raw.png")
print(f"Cross raw: {cross_filtered.size}")

# Downscale: 148x158 at ~10x scale -> 15x16
scale = 10
mc_w = round(148 / scale)  # 15
mc_h = round(158 / scale)  # 16
cross_small = cross_filtered.resize((mc_w, mc_h), Image.NEAREST)

# Center on 16x16
cross_16 = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
cross_16.paste(cross_small, ((16 - mc_w) // 2, (16 - mc_h) // 2), cross_small)
cross_16.save(f"{OUT}/cross_16.png")

# ============================================================
# DERIVE EW and NS wire from the cross
# ============================================================
# Analyze row widths to find horizontal band
row_info = {}
for y in range(16):
    pixels = []
    for x in range(16):
        r, g, b, a = cross_16.getpixel((x, y))
        if a > 50:
            pixels.append(x)
    row_info[y] = {"count": len(pixels), "min_x": min(pixels) if pixels else 16, "max_x": max(pixels) if pixels else 0}

# Similarly for columns (to find vertical band)
col_info = {}
for x in range(16):
    pixels = []
    for y in range(16):
        r, g, b, a = cross_16.getpixel((x, y))
        if a > 50:
            pixels.append(y)
    col_info[x] = {"count": len(pixels), "min_y": min(pixels) if pixels else 16, "max_y": max(pixels) if pixels else 0}

print("\nRow analysis:")
for y in range(16):
    info = row_info[y]
    bar = ""
    for x in range(16):
        r, g, b, a = cross_16.getpixel((x, y))
        if a < 50: bar += "."
        elif r > 150: bar += "R"
        elif r > 80: bar += "r"
        else: bar += "#"
    print(f"  y={y:2d} [{info['count']:2d}px]: {bar}")

print("\nColumn analysis:")
for x in range(16):
    info = col_info[x]
    print(f"  x={x:2d}: {info['count']:2d}px (y={info['min_y']}-{info['max_y']})")

# Horizontal band = rows with widest spread (reach to edges)
max_width = max(i["count"] for i in row_info.values())
horiz_rows = set()
for y, info in row_info.items():
    # Part of horizontal arm if it reaches close to edges
    if info["count"] >= max_width * 0.5 and info["max_x"] - info["min_x"] >= 10:
        horiz_rows.add(y)

# Vertical band = columns with tallest spread
max_height = max(i["count"] for i in col_info.values())
vert_cols = set()
for x, info in col_info.items():
    if info["count"] >= max_height * 0.5 and info["max_y"] - info["min_y"] >= 10:
        vert_cols.add(x)

print(f"\nHorizontal rows: {sorted(horiz_rows)}")
print(f"Vertical columns: {sorted(vert_cols)}")

# EW wire: keep horizontal rows + 1px outline margin
ew_rows = set()
for y in horiz_rows:
    for dy in range(-1, 2):
        if 0 <= y + dy < 16:
            ew_rows.add(y + dy)

ew_16 = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
for y in range(16):
    if y not in ew_rows:
        continue
    for x in range(16):
        px = cross_16.getpixel((x, y))
        if px[3] > 50:
            ew_16.putpixel((x, y), px)

ew_16.save(f"{OUT}/ew_wire_16.png")

# NS wire: keep vertical columns + 1px outline margin
ns_cols = set()
for x in vert_cols:
    for dx in range(-1, 2):
        if 0 <= x + dx < 16:
            ns_cols.add(x + dx)

ns_16 = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
for y in range(16):
    for x in range(16):
        if x not in ns_cols:
            continue
        px = cross_16.getpixel((x, y))
        if px[3] > 50:
            ns_16.putpixel((x, y), px)

ns_16.save(f"{OUT}/ns_wire_16.png")

# Print final textures
print("\n--- Final Textures ---")
for name, img in [("cross", cross_16), ("ew", ew_16), ("ns", ns_16)]:
    vis = sum(1 for y in range(16) for x in range(16) if img.getpixel((x, y))[3] > 50)
    print(f"\n{name}: {vis} pixels")
    for y in range(16):
        row = ""
        for x in range(16):
            r, g, b, a = img.getpixel((x, y))
            if a < 50: row += "."
            elif r > 150: row += "R"
            elif r > 80: row += "r"
            else: row += "#"
        if any(c != "." for c in row):
            print(f"  {row}")

# ============================================================
# COMPOSE on transparent background
# ============================================================
UPSCALE = 4
TILES = 21

# Separator
sep = Image.new("RGBA", (TILES * 16, 16), (0, 0, 0, 0))
for tx in range(TILES):
    sep.paste(ew_16, (tx * 16, 0), ew_16)
for pos in [5, 10, 15]:
    sep.paste(cross_16, (pos * 16, 0), cross_16)

sep_big = sep.resize((sep.width * UPSCALE, sep.height * UPSCALE), Image.NEAREST)
sep_big.save(f"{OUT}/redstone-separator.png")
print(f"\nSeparator: {sep_big.size}")

# Header: mini circuit
TH = 3
hdr = Image.new("RGBA", (TILES * 16, TH * 16), (0, 0, 0, 0))
for tx in range(TILES):
    hdr.paste(ew_16, (tx * 16, 1 * 16), ew_16)
for tx in [5, 15]:
    for ty in range(TH):
        hdr.paste(ns_16, (tx * 16, ty * 16), ns_16)
    hdr.paste(cross_16, (tx * 16, 1 * 16), cross_16)
hdr.paste(cross_16, (10 * 16, 1 * 16), cross_16)

hdr_big = hdr.resize((hdr.width * UPSCALE, hdr.height * UPSCALE), Image.NEAREST)
hdr_big.save(f"{OUT}/redstone-header.png")
print(f"Header: {hdr_big.size}")

print("\nDone!")
