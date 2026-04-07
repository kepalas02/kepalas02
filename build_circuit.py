"""
Build animated redstone circuit with proper MC physics:
- Torch outputs 15, each wire block loses 1
- Repeater receives any signal >= 1, outputs 15
- All connections visible, subtle grid, no gaps
"""
from PIL import Image, ImageDraw
import random
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
REF = "C:/Users/arthu/OneDrive/Bureau/moi/git"
MC = "assets/textures_mc"
OUT = "assets"

# ============================================================
# POWER COLORS (sampled from power.png)
# ============================================================
POWER_REDS = {
    15: 229, 14: 215, 13: 204, 12: 193,
    11: 182, 10: 176,  9: 166,  8: 154,
     7: 145,  6: 131,  5: 121,  4: 110,
     3: 100,  2:  89,  1:  78,  0:  68,
}

# Base wire colors at power 15
R15 = (254, 0, 0, 255)
r15 = (211, 14, 13, 255)
B = (0, 0, 0, 255)
b = (28, 26, 24, 255)
_ = (0, 0, 0, 0)

def tint(rgba, power):
    r, g, b_c, a = rgba
    if a == 0: return rgba
    if r < 35 and g < 35 and b_c < 35: return rgba
    f = POWER_REDS[power] / POWER_REDS[15]
    return (max(0, min(255, int(r * f))), max(0, min(255, int(g * f))),
            max(0, min(255, int(b_c * f))), a)

# ============================================================
# WIRE PATTERNS (16x16)
# ============================================================
def make_ew(power):
    """Straight EW wire at given power."""
    pattern = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [B,r15,B,R15,B,r15,R15,B,r15,B,R15,r15,B,R15,B,r15],
        [R15,B,R15,r15,R15,R15,B,R15,R15,R15,r15,B,R15,r15,R15,R15],
        [r15,R15,r15,B,r15,R15,r15,R15,B,r15,R15,R15,r15,B,r15,R15],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    ]
    img = Image.new("RGBA", (16, 16), (0,0,0,0))
    for y, row in enumerate(pattern):
        for x, c in enumerate(row):
            img.putpixel((x, y), tint(c, power))
    return img

def make_ns(power):
    """Straight NS wire at given power."""
    pattern = [
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
    img = Image.new("RGBA", (16, 16), (0,0,0,0))
    for y, row in enumerate(pattern):
        for x, c in enumerate(row):
            img.putpixel((x, y), tint(c, power))
    return img

def make_cross(power):
    """Cross = EW + NS overlaid."""
    ew = make_ew(power)
    ns = make_ns(power)
    cross = Image.new("RGBA", (16, 16), (0,0,0,0))
    cross.paste(ns, (0, 0), ns)
    cross.paste(ew, (0, 0), ew)
    return cross

# ============================================================
# COMPONENT TEXTURES
# ============================================================

# Repeater: base slab + 2 mini torches (red/yellow/stick) + wire channel
def make_repeater(on=True):
    base = Image.open(f"{REF}/images.png").convert("RGBA")
    rep = base.resize((16, 16), Image.NEAREST)

    # Colors from reference images
    if on:
        FLAME_TOP = (255, 50, 10, 255)    # red tip
        FLAME_MID = (255, 200, 0, 255)    # yellow glow
        FLAME_HOT = (255, 140, 30, 255)   # orange
        WIRE_C = (200, 0, 0, 255)         # bright wire channel
    else:
        FLAME_TOP = (120, 20, 10, 255)    # dark red
        FLAME_MID = (100, 40, 10, 255)    # dark orange
        FLAME_HOT = (90, 30, 10, 255)     # dark
        WIRE_C = (80, 0, 0, 255)          # dim wire

    STICK = (140, 100, 50, 255)            # wood
    STICK_D = (100, 70, 35, 255)           # dark wood

    # Left torch (input side) at x=3-5, y=4-8
    rep.putpixel((4, 4), FLAME_TOP)
    rep.putpixel((3, 5), FLAME_TOP)
    rep.putpixel((4, 5), FLAME_MID)
    rep.putpixel((5, 5), FLAME_HOT)
    rep.putpixel((4, 6), STICK)
    rep.putpixel((4, 7), STICK_D)

    # Right torch (output side) at x=10-12, y=4-8
    rep.putpixel((11, 4), FLAME_TOP)
    rep.putpixel((10, 5), FLAME_HOT)
    rep.putpixel((11, 5), FLAME_MID)
    rep.putpixel((12, 5), FLAME_TOP)
    rep.putpixel((11, 6), STICK)
    rep.putpixel((11, 7), STICK_D)

    # Wire channel between torches (red groove in the slab)
    for x in range(5, 11):
        rep.putpixel((x, 7), WIRE_C)
        rep.putpixel((x, 8), (max(0, WIRE_C[0]-40), 0, 0, 255))

    # Wire extending to edges (input from left, output to right)
    for x in range(0, 4):
        rep.putpixel((x, 7), WIRE_C)
        rep.putpixel((x, 8), (max(0, WIRE_C[0]-40), 0, 0, 255))
    for x in range(12, 16):
        rep.putpixel((x, 7), WIRE_C)
        rep.putpixel((x, 8), (max(0, WIRE_C[0]-40), 0, 0, 255))

    return rep

# Torch on block with wire going RIGHT
def make_torch_with_wire_right(wire_power=14):
    """Torch block: torch in center + EW wire going right."""
    img = Image.new("RGBA", (16, 16), (0,0,0,0))
    # Torch flame
    FLAME = (255, 50, 10, 255)
    FLAME_Y = (255, 200, 0, 255)
    FLAME_W = (255, 240, 200, 255)
    STICK_L = (153, 112, 66, 255)
    STICK_D = (101, 67, 33, 255)
    # Flame 3x3
    for y in [5, 6, 7]:
        for x in [6, 7, 8]:
            img.putpixel((x, y), FLAME)
    img.putpixel((7, 6), FLAME_Y)
    img.putpixel((7, 5), FLAME_W)
    # Stick
    for y in [8, 9, 10]:
        img.putpixel((7, y), STICK_L)
        img.putpixel((8, y), STICK_D)
    # Wire going RIGHT from torch (at wire height y=6-8)
    f = POWER_REDS[wire_power] / POWER_REDS[15]
    wr = int(254 * f)
    for x in range(9, 16):
        img.putpixel((x, 7), (wr, 0, 0, 255))
        img.putpixel((x, 8), (max(0, wr - 40), 0, 0, 255))
    return img

# Torch on block with wire going LEFT
def make_torch_with_wire_left(wire_power=14):
    img = Image.new("RGBA", (16, 16), (0,0,0,0))
    FLAME = (255, 50, 10, 255)
    FLAME_Y = (255, 200, 0, 255)
    FLAME_W = (255, 240, 200, 255)
    STICK_L = (153, 112, 66, 255)
    STICK_D = (101, 67, 33, 255)
    for y in [5, 6, 7]:
        for x in [6, 7, 8]:
            img.putpixel((x, y), FLAME)
    img.putpixel((7, 6), FLAME_Y)
    img.putpixel((7, 5), FLAME_W)
    for y in [8, 9, 10]:
        img.putpixel((7, y), STICK_L)
        img.putpixel((8, y), STICK_D)
    f = POWER_REDS[wire_power] / POWER_REDS[15]
    wr = int(254 * f)
    for x in range(0, 7):
        img.putpixel((x, 7), (wr, 0, 0, 255))
        img.putpixel((x, 8), (max(0, wr - 40), 0, 0, 255))
    return img

# Torch with wire going UP (for vertical branch end)
def make_torch_with_wire_up(wire_power=14):
    img = Image.new("RGBA", (16, 16), (0,0,0,0))
    FLAME = (255, 50, 10, 255)
    FLAME_Y = (255, 200, 0, 255)
    FLAME_W = (255, 240, 200, 255)
    STICK_L = (153, 112, 66, 255)
    STICK_D = (101, 67, 33, 255)
    for y in [7, 8, 9]:
        for x in [6, 7, 8]:
            img.putpixel((x, y), FLAME)
    img.putpixel((7, 8), FLAME_Y)
    img.putpixel((7, 7), FLAME_W)
    for y in [10, 11, 12]:
        img.putpixel((7, y), STICK_L)
        img.putpixel((8, y), STICK_D)
    # Wire going UP
    f = POWER_REDS[wire_power] / POWER_REDS[15]
    wr = int(254 * f)
    for y in range(0, 7):
        img.putpixel((7, y), (wr, 0, 0, 255))
        img.putpixel((6, y), (max(0, wr - 40), 0, 0, 255))
    return img

# Lamp
lamp = Image.open(f"{REF}/120px-On_Redstone_Lamp_(texture)_JE3_BE2.png").convert("RGBA").resize((16, 16), Image.NEAREST)

# Redstone block
rs_block = Image.open(f"{REF}/images.jpg").convert("RGBA").resize((16, 16), Image.NEAREST)

# Piston
piston = Image.open(f"{REF}/637793521418142450.jpeg").convert("RGBA").resize((16, 16), Image.NEAREST)

repeater_on = make_repeater(on=True)
repeater_off = make_repeater(on=False)

# Save previews
for name, img in [("repeater_on", repeater_on), ("repeater_off", repeater_off)]:
    img.save(f"{MC}/{name}.png")
    img.resize((128, 128), Image.NEAREST).save(f"{MC}/{name}_8x.png")

# ============================================================
# CIRCUIT LAYOUT with proper MC redstone physics
# ============================================================
# 21 wide x 5 tall
#
# Signal flow:
# [Torch(15)] ->ew14->ew13->ew12->ew11->ew10->[Cross9(branch up)]-ew8->ew7->[Repeater(out:15)]->ew14->ew13->ew12->ew11->[Cross10(branch down)]->ew9->ew8->ew7->ew6->[Lamp]
#
# Branch up from Cross9: ns8 -> [RS Block] (decoration)
# Branch down from Cross10: ns9 -> [Piston]

W = 21
H = 5
TILE = 16
SCALE = 4

# Build the grid with (tile_image, description)
grid = [[None] * W for _ in range(H)]

# Row 2 = main horizontal wire
# x=0: Torch (source, power 15) with wire going right
grid[2][0] = make_torch_with_wire_right(14)

# x=1-5: wire decaying from 14
for i, p in enumerate([13, 12, 11, 10, 9]):
    grid[2][1 + i] = make_ew(p)

# x=6: Cross with branch UP (power 8)
grid[2][6] = make_cross(8)

# x=7-8: wire continues
grid[2][7] = make_ew(7)
grid[2][8] = make_ew(6)

# x=9: Repeater ON (receives 6, outputs 15)
grid[2][9] = repeater_on

# x=10-14: wire from repeater output (15, 14, 13, 12, 11)
for i, p in enumerate([14, 13, 12, 11, 10]):
    grid[2][10 + i] = make_ew(p)

# x=15: Cross with branch DOWN (power 9)
grid[2][15] = make_cross(9)

# x=16-19: wire continues (8, 7, 6, 5)
for i, p in enumerate([8, 7, 6, 5]):
    grid[2][16 + i] = make_ew(p)

# x=20: Lamp (receives signal)
grid[2][20] = lamp

# Branch UP from x=6: ns wire -> redstone block
grid[1][6] = make_ns(7)
grid[0][6] = rs_block

# Branch DOWN from x=15: ns wire -> piston
grid[3][15] = make_ns(8)
grid[4][15] = piston

# ============================================================
# RENDER
# ============================================================
# GitHub dark mode background
BG = (13, 17, 23, 255)
GRID_COLOR = (30, 35, 45, 255)  # very subtle grid

canvas = Image.new("RGBA", (W * TILE * SCALE, H * TILE * SCALE), BG)

# Draw subtle grid
draw = ImageDraw.Draw(canvas)
for tx in range(W + 1):
    x = tx * TILE * SCALE
    draw.line([(x, 0), (x, canvas.height)], fill=GRID_COLOR, width=1)
for ty in range(H + 1):
    y = ty * TILE * SCALE
    draw.line([(0, y), (canvas.width, y)], fill=GRID_COLOR, width=1)

# Paste tiles
for row_i in range(H):
    for col_i in range(W):
        tile = grid[row_i][col_i]
        if tile:
            # Scale tile up
            tile_big = tile.resize((TILE * SCALE, TILE * SCALE), Image.NEAREST)
            canvas.paste(tile_big, (col_i * TILE * SCALE, row_i * TILE * SCALE), tile_big)

canvas.save(f"{OUT}/redstone-circuit-static.png")
print(f"Static: {canvas.size}")

# ============================================================
# ANIMATE WITH PARTICLES
# ============================================================
active_tiles = []
for row_i in range(H):
    for col_i in range(W):
        if grid[row_i][col_i] is not None:
            cx = col_i * TILE * SCALE + (TILE * SCALE) // 2
            cy = row_i * TILE * SCALE + (TILE * SCALE) // 2
            active_tiles.append((cx, cy))

PARTICLE_COLORS = [
    (255, 30, 0), (230, 20, 0), (255, 60, 20),
    (200, 10, 0), (255, 80, 30), (180, 0, 0),
]

NUM_FRAMES = 24
FRAME_MS = 180
frames = []
random.seed(42)

for fi in range(NUM_FRAMES):
    frame = canvas.copy()
    # 3-6 particles per frame
    for _ in range(random.randint(3, 6)):
        cx, cy = random.choice(active_tiles)
        # Particles float upward slightly, within tile bounds
        px = cx + random.randint(-20, 20)
        py = cy + random.randint(-25, 15)
        size = random.randint(2, 5)
        color = random.choice(PARTICLE_COLORS)
        alpha = random.randint(120, 220)
        for dy in range(size):
            for dx in range(size):
                ppx, ppy = px + dx, py + dy
                if 0 <= ppx < frame.width and 0 <= ppy < frame.height:
                    # Blend with existing pixel
                    er, eg, eb, ea = frame.getpixel((ppx, ppy))
                    blend = alpha / 255
                    nr = int(er * (1 - blend) + color[0] * blend)
                    ng = int(eg * (1 - blend) + color[1] * blend)
                    nb = int(eb * (1 - blend) + color[2] * blend)
                    frame.putpixel((ppx, ppy), (nr, ng, nb, 255))
    frames.append(frame.convert("RGB"))

# Save GIF
frames[0].save(
    f"{OUT}/redstone-circuit.gif",
    save_all=True,
    append_images=frames[1:],
    duration=FRAME_MS,
    loop=0,
    optimize=True,
)

print(f"GIF: {len(frames)} frames @ {FRAME_MS}ms = {len(frames)*FRAME_MS/1000:.1f}s loop")
print("Done!")
