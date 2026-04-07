"""
Create all Minecraft redstone textures at 16 power levels + repeater.
"""
from PIL import Image
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
OUT = "assets/textures_mc"
os.makedirs(OUT, exist_ok=True)

# Base colors at power level 15 (brightest)
R15 = (254, 0, 0, 255)
r15 = (211, 14, 13, 255)
D15 = (182, 14, 13, 255)
B = (0, 0, 0, 255)
b = (28, 26, 24, 255)
_ = (0, 0, 0, 0)

# Average red per power level (from sampling)
POWER_REDS = {
    15: 229, 14: 215, 13: 204, 12: 193,
    11: 192, 10: 176,  9: 166,  8: 154,
     7: 145,  6: 131,  5: 121,  4: 110,
     3: 100,  2:  89,  1:  78,  0:  68,
}

def tint_color(base_rgba, power_level):
    """Scale a red-channel color to match a power level."""
    r, g, b, a = base_rgba
    if a == 0:
        return base_rgba
    if r < 35 and g < 35 and b < 35:
        # Black outline stays black
        return base_rgba
    # Scale the red channel proportionally
    factor = POWER_REDS[power_level] / POWER_REDS[15]
    new_r = max(0, min(255, int(r * factor)))
    new_g = max(0, min(255, int(g * factor)))
    new_b = max(0, min(255, int(b * factor)))
    return (new_r, new_g, new_b, a)

# ============================================================
# NS WIRE pattern (base at power 15)
# ============================================================
ns_pattern = [
    [_,_,_,_,_,_,_,R15,B,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,B,R15,r15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,r15,R15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,R15,B,R15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,R15,B,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,B,R15,r15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,r15,R15,B,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,R15,R15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,B,r15,R15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,R15,B,r15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,R15,R15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,r15,R15,B,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,B,R15,r15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,r15,R15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,R15,B,R15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,b,R15,r15,_,_,_,_,_,_,_],
]

# CROSS pattern (base at power 15) - extracted from power.png
# Using the pixel map from earlier extraction + the arm wire pattern
cross_pattern = [
    [_,_,_,_,_,_,_,R15,B,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,B,R15,r15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,r15,R15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,R15,B,R15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,R15,B,_,_,_,_,_,_,_],
    [_,_,_,_,_,R15,B,R15,r15,B,_,_,_,_,_,_],
    [R15,_,r15,D15,_,R15,R15,R15,R15,R15,r15,R15,R15,R15,_,_],
    [_,_,_,R15,R15,R15,R15,R15,R15,B,B,R15,_,_,R15,_],
    [B,_,B,B,_,R15,R15,R15,R15,R15,_,B,B,B,_,_],
    [_,_,_,b,b,B,R15,B,R15,_,_,b,_,_,b,_],
    [_,_,_,_,_,_,_,R15,R15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,r15,R15,B,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,B,R15,r15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,r15,R15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,R15,B,R15,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,b,R15,r15,_,_,_,_,_,_,_],
]

def make_texture(pattern, power_level):
    """Create a 16x16 texture from a pattern at a given power level."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(pattern):
        for x, c in enumerate(row):
            tinted = tint_color(c, power_level)
            img.putpixel((x, y), tinted)
    return img

# ============================================================
# Generate all 16 power levels for cross, NS wire, EW wire
# ============================================================
print("Generating textures for all 16 power levels...")
for pl in range(16):
    # Cross
    cross = make_texture(cross_pattern, pl)
    cross.save(f"{OUT}/cross_p{pl:02d}.png")

    # NS wire
    ns = make_texture(ns_pattern, pl)
    ns.save(f"{OUT}/ns_p{pl:02d}.png")

    # EW wire (rotated NS)
    ew = ns.rotate(-90, expand=False)
    ew.save(f"{OUT}/ew_p{pl:02d}.png")

    # Show color info
    avg_r = POWER_REDS[pl]
    print(f"  Power {pl:2d}: R={avg_r:3d} {'#' * (avg_r // 8)}")

# ============================================================
# REPEATER (top-down view, 16x16)
# ============================================================
print("\nCreating repeater texture...")

# Repeater = smooth stone slab + 2 redstone torches + direction indicator
# Colors
SLAB = (190, 190, 190, 255)      # light gray slab
SLAB_D = (170, 170, 170, 255)    # darker slab variation
SLAB_L = (200, 200, 200, 255)    # lighter slab
SLAB_E = (150, 150, 150, 255)    # edge/border
TORCH_R = (255, 50, 10, 255)     # torch flame bright
TORCH_D = (200, 20, 0, 255)      # torch darker
TORCH_S = (90, 60, 30, 255)      # torch stick (wood)
WIRE_R = (200, 0, 0, 255)        # wire on repeater

import random
random.seed(42)

rep = Image.new("RGBA", (16, 16), (0, 0, 0, 0))

# Stone slab base (fills most of the block)
for y in range(2, 14):
    for x in range(2, 14):
        c = random.choice([SLAB, SLAB, SLAB_D, SLAB_L, SLAB])
        rep.putpixel((x, y), c)

# Border
for x in range(2, 14):
    rep.putpixel((x, 2), SLAB_E)
    rep.putpixel((x, 13), SLAB_E)
for y in range(2, 14):
    rep.putpixel((2, y), SLAB_E)
    rep.putpixel((13, y), SLAB_E)

# Two redstone torches (along horizontal axis, facing right)
# Left torch (input side) at x=4-5, y=6-9
for y in [7, 8]:
    for x in [4, 5]:
        rep.putpixel((x, y), TORCH_R)
rep.putpixel((4, 7), TORCH_D)
# Stick below
rep.putpixel((4, 9), TORCH_S)
rep.putpixel((5, 9), TORCH_S)

# Right torch (output side) at x=9-10, y=6-9
for y in [7, 8]:
    for x in [9, 10]:
        rep.putpixel((x, y), TORCH_R)
rep.putpixel((10, 7), TORCH_D)
# Stick below
rep.putpixel((9, 9), TORCH_S)
rep.putpixel((10, 9), TORCH_S)

# Wire connecting input edge to left torch
for x in range(2, 5):
    rep.putpixel((x, 7), WIRE_R)
    rep.putpixel((x, 8), B)

# Wire connecting right torch to output edge
for x in range(10, 14):
    rep.putpixel((x, 7), WIRE_R)
    rep.putpixel((x, 8), B)

rep.save(f"{OUT}/repeater.png")

# Also save at 4x for preview
rep_big = rep.resize((64, 64), Image.NEAREST)
rep_big.save(f"{OUT}/repeater_4x.png")

# ============================================================
# COMPARATOR (top-down, 16x16) - 3 torches in triangle
# ============================================================
print("Creating comparator texture...")
comp = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
random.seed(99)

# Stone slab base
for y in range(2, 14):
    for x in range(2, 14):
        c = random.choice([SLAB, SLAB, SLAB_D, SLAB_L, SLAB])
        comp.putpixel((x, y), c)
for x in range(2, 14):
    comp.putpixel((x, 2), SLAB_E)
    comp.putpixel((x, 13), SLAB_E)
for y in range(2, 14):
    comp.putpixel((2, y), SLAB_E)
    comp.putpixel((13, y), SLAB_E)

# Two back torches (input side, left) at x=4, y=5-6 and y=9-10
for y in [5, 6]:
    for x in [4, 5]:
        comp.putpixel((x, y), TORCH_R)
comp.putpixel((4, 5), TORCH_D)

for y in [9, 10]:
    for x in [4, 5]:
        comp.putpixel((x, y), TORCH_R)
comp.putpixel((4, 10), TORCH_D)

# One front torch (output side, right) at x=9-10, y=7-8
for y in [7, 8]:
    for x in [9, 10]:
        comp.putpixel((x, y), TORCH_R)
comp.putpixel((10, 7), TORCH_D)

# Wires
for x in range(2, 5):
    comp.putpixel((x, 5), WIRE_R)
    comp.putpixel((x, 10), WIRE_R)
for x in range(10, 14):
    comp.putpixel((x, 7), WIRE_R)
    comp.putpixel((x, 8), B)

comp.save(f"{OUT}/comparator.png")
comp_big = comp.resize((64, 64), Image.NEAREST)
comp_big.save(f"{OUT}/comparator_4x.png")

# ============================================================
# REDSTONE TORCH (top-down, 16x16)
# ============================================================
print("Creating torch texture...")
torch = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
# Small torch centered
for y in [6, 7, 8]:
    for x in [7, 8]:
        torch.putpixel((x, y), TORCH_R)
torch.putpixel((7, 6), (255, 120, 50, 255))  # bright tip
torch.putpixel((8, 6), (255, 100, 40, 255))
# Stick
for y in [9, 10, 11]:
    torch.putpixel((7, y), TORCH_S)
    torch.putpixel((8, y), (75, 50, 25, 255))
# Glow
for dx, dy in [(-1,0),(2,0),(0,-1),(1,-1)]:
    px, py = 7+dx, 7+dy
    if 0 <= px < 16 and 0 <= py < 16:
        torch.putpixel((px, py), (255, 30, 0, 60))

torch.save(f"{OUT}/torch.png")
torch_big = torch.resize((64, 64), Image.NEAREST)
torch_big.save(f"{OUT}/torch_4x.png")

# ============================================================
# REDSTONE LAMP (top-down, 16x16) - ON and OFF
# ============================================================
print("Creating lamp textures...")
random.seed(77)
for state, brightness in [("on", 1.0), ("off", 0.4)]:
    lamp = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            # Glowstone-like pattern
            base_r = int(210 * brightness)
            base_g = int(170 * brightness)
            base_b = int(50 * brightness)
            variation = random.randint(-20, 20)
            r = max(0, min(255, base_r + variation))
            g = max(0, min(255, base_g + variation))
            b_val = max(0, min(255, base_b + int(variation * 0.5)))
            lamp.putpixel((x, y), (r, g, b_val, 255))
    # Grid lines for glowstone texture
    for i in [4, 8, 12]:
        for j in range(16):
            r, g, b_val, a = lamp.getpixel((i, j))
            lamp.putpixel((i, j), (int(r*0.8), int(g*0.8), int(b_val*0.8), a))
            r, g, b_val, a = lamp.getpixel((j, i))
            lamp.putpixel((j, i), (int(r*0.8), int(g*0.8), int(b_val*0.8), a))

    lamp.save(f"{OUT}/lamp_{state}.png")
    lamp_big = lamp.resize((64, 64), Image.NEAREST)
    lamp_big.save(f"{OUT}/lamp_{state}_4x.png")

# ============================================================
# Also copy best textures to main assets folder
# ============================================================
import shutil
for pl in [15, 12, 9, 6, 3, 0]:
    shutil.copy(f"{OUT}/cross_p{pl:02d}.png", f"assets/cross_p{pl}.png")
    shutil.copy(f"{OUT}/ew_p{pl:02d}.png", f"assets/ew_p{pl}.png")

shutil.copy(f"{OUT}/repeater.png", "assets/repeater_16.png")
shutil.copy(f"{OUT}/comparator.png", "assets/comparator_16.png")
shutil.copy(f"{OUT}/torch.png", "assets/torch_16.png")

print("\n=== All textures generated! ===")
print(f"  16 power levels x 3 types (cross, ns, ew) = 48 wire textures")
print(f"  + repeater, comparator, torch, lamp_on, lamp_off")
print(f"  Total: 53 textures in {OUT}/")
