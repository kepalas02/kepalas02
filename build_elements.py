"""
Generate all MC redstone element textures individually for review.
Each saved at 16x16 (native) and 128x128 (8x preview).
Creates a gallery image showing all elements.
"""
from PIL import Image, ImageDraw
import random
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
REF = "C:/Users/arthu/OneDrive/Bureau/moi/git/Saves"
OUT = "assets/elements"
os.makedirs(OUT, exist_ok=True)

POWER_REDS = {
    15: 229, 14: 215, 13: 204, 12: 193,
    11: 182, 10: 176,  9: 166,  8: 154,
     7: 145,  6: 131,  5: 121,  4: 110,
     3: 100,  2:  89,  1:  78,  0:  68,
}

_ = (0, 0, 0, 0)

def save_el(img, name):
    img.save(f"{OUT}/{name}_16.png")
    big = img.resize((128, 128), Image.NEAREST)
    big.save(f"{OUT}/{name}_8x.png")
    print(f"  {name}")
    return img

# ============================================================
# 1. REPEATER (facing right: input=left, output=right)
# ============================================================
# Based on images.png (actual MC repeater slab texture) + torch marks
# from Redstone-Repeater-4.gif (top-down reference)
#
# In the GIF: repeater = gray slab filling tile, thin red wire groove,
# two small dark red torch marks (visible from above as ~2x3 px blobs)

def make_repeater(on=True):
    # Load actual MC texture and downscale
    base = Image.open(f"{REF}/images.png").convert("RGBA")
    rep = base.resize((16, 16), Image.NEAREST)

    # Original texture: wire channel runs VERTICALLY (top-bottom)
    # Rotate 90 CW so wire runs LEFT-RIGHT (input left, output right)
    rep = rep.rotate(-90, expand=False)

    # If OFF: darken the red wire channel too
    if not on:
        for y in range(16):
            for x in range(16):
                r, g, b_c, a = rep.getpixel((x, y))
                if r > 100 and g < 40 and b_c < 40:
                    # This is a red pixel (wire channel) -> darken it
                    rep.putpixel((x, y), (r // 3, g // 3, b_c // 3, a))

    # Torch marks: taller (5px) with red on top, wood on bottom
    # User: "+2px de marron vers le haut, en remontant le rouge"
    if on:
        TORCH_R = (190, 30, 15, 255)      # dark red torch top
        TORCH_B = (230, 50, 20, 255)      # brighter center
        TORCH_W = (130, 90, 45, 255)      # wood
        TORCH_WD = (100, 70, 35, 255)     # darker wood
    else:
        TORCH_R = (65, 15, 10, 255)
        TORCH_B = (45, 10, 5, 255)
        TORCH_W = (80, 55, 30, 255)
        TORCH_WD = (60, 40, 22, 255)

    # Back torch (input side) - 6px tall: 2px red + 4px wood
    rep.putpixel((3, 3), TORCH_R)
    rep.putpixel((4, 3), TORCH_R)
    rep.putpixel((3, 4), TORCH_B)
    rep.putpixel((4, 4), TORCH_R)
    rep.putpixel((3, 5), TORCH_W)
    rep.putpixel((4, 5), TORCH_W)
    rep.putpixel((3, 6), TORCH_WD)
    rep.putpixel((4, 6), TORCH_W)
    rep.putpixel((3, 7), TORCH_W)
    rep.putpixel((4, 7), TORCH_WD)
    rep.putpixel((3, 8), TORCH_WD)
    rep.putpixel((4, 8), TORCH_W)

    # Front torch (output side) - same 6px tall
    rep.putpixel((11, 3), TORCH_R)
    rep.putpixel((12, 3), TORCH_R)
    rep.putpixel((11, 4), TORCH_B)
    rep.putpixel((12, 4), TORCH_R)
    rep.putpixel((11, 5), TORCH_W)
    rep.putpixel((12, 5), TORCH_W)
    rep.putpixel((11, 6), TORCH_WD)
    rep.putpixel((12, 6), TORCH_W)
    rep.putpixel((11, 7), TORCH_W)
    rep.putpixel((12, 7), TORCH_WD)
    rep.putpixel((11, 8), TORCH_WD)
    rep.putpixel((12, 8), TORCH_W)

    return rep


# ============================================================
# 2. TORCH (standalone, top-down view)
# ============================================================
# From 51-514803... reference (side view):
#   - Flame head: red cross, yellow center, white/cream highlight
#   - Stick: brown/dark brown
# From above: see the flame top (red ring + bright center) + stick base

def make_torch_standalone():
    """Redstone torch STANDING UP (side view sprite, like the reference).
    Flame cross at top, brown stick below."""
    img = Image.new("RGBA", (16, 16), _)

    RED   = (230, 40, 15, 255)
    RED_D = (200, 25, 10, 255)
    ORANGE= (240, 140, 30, 255)
    YELLOW= (255, 220, 50, 255)
    WHITE = (255, 240, 200, 255)
    STK_L = (150, 110, 60, 255)
    STK_D = (100, 70, 35, 255)

    # Flame cross (4px wide, 4px tall)
    img.putpixel((7, 1), RED)
    img.putpixel((8, 1), RED_D)
    img.putpixel((6, 2), RED)
    img.putpixel((7, 2), YELLOW)
    img.putpixel((8, 2), ORANGE)
    img.putpixel((9, 2), RED)
    img.putpixel((6, 3), RED_D)
    img.putpixel((7, 3), WHITE)
    img.putpixel((8, 3), RED)
    img.putpixel((9, 3), RED_D)
    img.putpixel((7, 4), RED)
    img.putpixel((8, 4), RED_D)

    # Stick (2px wide, 6px tall — longer)
    img.putpixel((7, 5), STK_L)
    img.putpixel((8, 5), STK_D)
    img.putpixel((7, 6), STK_D)
    img.putpixel((8, 6), STK_L)
    img.putpixel((7, 7), STK_L)
    img.putpixel((8, 7), STK_D)
    img.putpixel((7, 8), STK_D)
    img.putpixel((8, 8), STK_L)
    img.putpixel((7, 9), STK_L)
    img.putpixel((8, 9), STK_D)
    img.putpixel((7, 10), STK_D)
    img.putpixel((8, 10), STK_L)

    return img


# ============================================================
# 3. TORCH + WIRE (all 4 directions)
# ============================================================
# User feedback: "le fil part toujours du bas du baton"
# = wire exits from the BOTTOM of the stick (flame end is source)
# Flow: FLAME -> STICK -> WIRE -> tile edge
# Everything aligned in same direction

def make_torch_wire(direction="right", wire_power=14):
    """Torch STANDING UP (side view) + wire from stick base.
    Torch is always upright: flame top, stick below.
    Wire exits from the BASE of the stick going in the specified direction.
    """
    img = Image.new("RGBA", (16, 16), _)

    RED   = (230, 40, 15, 255)
    RED_D = (200, 25, 10, 255)
    ORANGE= (240, 140, 30, 255)
    YELLOW= (255, 220, 50, 255)
    WHITE = (255, 240, 200, 255)
    STK_L = (150, 110, 60, 255)
    STK_D = (100, 70, 35, 255)

    f = POWER_REDS[wire_power] / POWER_REDS[15]
    WR   = (max(0, min(255, int(254 * f))), 0, 0, 255)
    WR_D = (max(0, min(255, int(200 * f))), 0, 0, 255)

    def draw_upright_torch(cx=7, flame_y=1):
        """Draw standing torch at center x=cx, flame starting at flame_y.
        Returns the y-coordinate of the stick base."""
        # Flame cross (4px wide, 4px tall)
        img.putpixel((cx, flame_y), RED)
        img.putpixel((cx+1, flame_y), RED_D)
        img.putpixel((cx-1, flame_y+1), RED)
        img.putpixel((cx, flame_y+1), YELLOW)
        img.putpixel((cx+1, flame_y+1), ORANGE)
        img.putpixel((cx+2, flame_y+1), RED)
        img.putpixel((cx-1, flame_y+2), RED_D)
        img.putpixel((cx, flame_y+2), WHITE)
        img.putpixel((cx+1, flame_y+2), RED)
        img.putpixel((cx+2, flame_y+2), RED_D)
        img.putpixel((cx, flame_y+3), RED)
        img.putpixel((cx+1, flame_y+3), RED_D)

        # Stick (2px wide, 5px tall — longer stick)
        sy = flame_y + 4
        img.putpixel((cx, sy), STK_L)
        img.putpixel((cx+1, sy), STK_D)
        img.putpixel((cx, sy+1), STK_D)
        img.putpixel((cx+1, sy+1), STK_L)
        img.putpixel((cx, sy+2), STK_L)
        img.putpixel((cx+1, sy+2), STK_D)
        img.putpixel((cx, sy+3), STK_D)
        img.putpixel((cx+1, sy+3), STK_L)
        img.putpixel((cx, sy+4), STK_L)
        img.putpixel((cx+1, sy+4), STK_D)
        return sy + 4  # y of stick base

    # Textured wire colors (like real redstone wire: alternating R, r, B)
    WR_r = (max(0, min(255, int(211 * f))), max(0, min(255, int(14 * f))),
            max(0, min(255, int(13 * f))), 255)  # darker red
    WR_B = (0, 0, 0, 255)  # black accent

    # Wire row patterns (matching the EW/NS wire texture style)
    def wire_color_h(x):
        """Alternating texture for horizontal wire, 2 rows."""
        pat = [WR, WR_B, WR, WR_r, WR, WR, WR_B, WR, WR, WR, WR_r, WR_B, WR, WR_r, WR, WR]
        pat2 = [WR_r, WR, WR_r, WR_B, WR_r, WR, WR_r, WR, WR_B, WR_r, WR, WR, WR_r, WR_B, WR_r, WR]
        return pat[x % 16], pat2[x % 16]

    def wire_color_v(y):
        """Alternating texture for vertical wire, 2 cols."""
        pat = [WR, WR_B, WR, WR_r, WR, WR, WR_B, WR, WR, WR, WR_r, WR_B, WR, WR_r, WR, WR]
        pat2 = [WR_r, WR, WR_r, WR_B, WR_r, WR, WR_r, WR, WR_B, WR_r, WR, WR, WR_r, WR_B, WR_r, WR]
        return pat[y % 16], pat2[y % 16]

    if direction == "right":
        base_y = draw_upright_torch(cx=3, flame_y=1)
        # Textured wire going RIGHT from stick base
        for x in range(5, 16):
            c1, c2 = wire_color_h(x)
            img.putpixel((x, base_y - 1), c2)
            img.putpixel((x, base_y), c1)

    elif direction == "left":
        base_y = draw_upright_torch(cx=11, flame_y=1)
        # Textured wire going LEFT
        for x in range(0, 10):
            c1, c2 = wire_color_h(x)
            img.putpixel((x, base_y - 1), c2)
            img.putpixel((x, base_y), c1)

    elif direction == "down":
        base_y = draw_upright_torch(cx=7, flame_y=1)
        # Textured wire going DOWN
        for y in range(base_y + 1, 16):
            c1, c2 = wire_color_v(y)
            img.putpixel((7, y), c1)
            img.putpixel((8, y), c2)

    elif direction == "up":
        base_y = draw_upright_torch(cx=7, flame_y=7)
        # Wire goes UP from above the flame
        for y in range(0, 7):
            c1, c2 = wire_color_v(y)
            img.putpixel((7, y), c1)
            img.putpixel((8, y), c2)

    return img


# ============================================================
# 4. PISTON (signal enters from LEFT = stone side,
#            push goes RIGHT = wood side)
# ============================================================
# Reference: 637793521418142450.jpeg
#   - Top of image = wood planks (gold/brown + iron band)
#   - Bottom of image = cobblestone (gray)
# Rotate 90 CW: wood goes RIGHT, stone goes LEFT

def make_piston():
    base = Image.open(f"{REF}/637793521418142450.jpeg").convert("RGBA")
    p = base.resize((16, 16), Image.NEAREST)
    # Original: wood=top, stone=bottom
    # 90 CW: top->right, bottom->left => wood=right, stone=left
    p = p.rotate(-90, expand=False)
    return p


def make_piston_extended_frames():
    """Generate piston extension frames facing DOWN.
    Base (stone) stays at top, head (wood) moves down, arm grows between.
    Returns dict: extension_px -> Image (16 x (16+ext)).
    Steps of 2px from 0 to 16 (full block extension).
    """
    # Load piston facing down: stone=top (y0-11), wood=bottom (y12-15)
    base_img = Image.open(f"{REF}/637793521418142450.jpeg").convert("RGBA")
    p = base_img.resize((16, 16), Image.NEAREST)
    p = p.rotate(-90, expand=False)   # horizontal
    piston_down = p.rotate(-90, expand=False)  # stone=top, wood=bottom

    # Split: base = stone rows (y=0-11), head = wood rows (y=12-15)
    base_part = piston_down.crop((0, 0, 16, 12))   # 16x12
    head_part = piston_down.crop((0, 12, 16, 16))   # 16x4

    # Arm colors sampled from reference minecraft-piston.gif
    # Arm is 6px wide centered (x=5 to x=10)
    LW  = (188, 153, 99, 255)   # light wood (tan/golden)
    MW  = (180, 145, 91, 255)   # medium wood
    DW  = (159, 132, 77, 255)   # dark wood
    DDW = (120,  90, 55, 255)   # darkest wood (edges)
    LI  = (175, 175, 175, 255)  # light iron
    MI  = (145, 145, 145, 255)  # medium iron
    DI  = (118, 118, 118, 255)  # dark iron

    def draw_arm_row(img, x_start, y, is_iron_band):
        """Draw one row of arm (6px wide: x_start to x_start+5)."""
        if is_iron_band:
            colors = [DI, MI, LI, LI, MI, DI]
        else:
            colors = [DDW, DW, LW, MW, DW, DDW]
        for i, c in enumerate(colors):
            img.putpixel((x_start + i, y), c)

    frames = {}

    # Frame 0: retracted (original piston)
    frames[0] = piston_down.copy()

    # Frames 2 to 16: arm extends 2px at a time
    for ext in range(2, 18, 2):
        h = 16 + ext
        frame = Image.new("RGBA", (16, h), (0, 0, 0, 0))

        # Paste stone base at top
        frame.paste(base_part, (0, 0))

        # Draw arm rows (ext pixels tall, centered at x=5-10)
        for ay in range(ext):
            y = 12 + ay
            # Iron band every 4 rows (at row 1-2, 5-6, 9-10, 13-14)
            is_iron = ((ay % 4) >= 2)
            draw_arm_row(frame, 5, y, is_iron)

        # Paste wood head at bottom
        frame.paste(head_part, (0, 12 + ext))

        frames[ext] = frame

    return frames


# ============================================================
# 5. LAMP (ON and OFF)
# ============================================================
def make_lamp_on():
    lamp = Image.open(f"{REF}/120px-On_Redstone_Lamp_(texture)_JE3_BE2.png").convert("RGBA")
    return lamp.resize((16, 16), Image.NEAREST)

def make_lamp_off():
    """Dim version of the lamp."""
    lamp = make_lamp_on()
    out = Image.new("RGBA", (16, 16), _)
    for y in range(16):
        for x in range(16):
            r, g, b, a = lamp.getpixel((x, y))
            # Darken significantly
            out.putpixel((x, y), (int(r*0.35), int(g*0.35), int(b*0.35), a))
    return out


# ============================================================
# 6. REDSTONE BLOCK
# ============================================================
def make_rs_block():
    block = Image.open(f"{REF}/images.jpg").convert("RGBA")
    return block.resize((16, 16), Image.NEAREST)


# ============================================================
# 7. WIRES at sample power levels
# ============================================================
R15 = (254, 0, 0, 255)
r15 = (211, 14, 13, 255)
B = (0, 0, 0, 255)
b = (28, 26, 24, 255)

def tint(rgba, power):
    r, g, b_c, a = rgba
    if a == 0: return rgba
    if r < 35 and g < 35 and b_c < 35: return rgba
    f = POWER_REDS[power] / POWER_REDS[15]
    return (max(0,min(255,int(r*f))), max(0,min(255,int(g*f))), max(0,min(255,int(b_c*f))), a)

def make_ew(power):
    pattern = [
        [_]*16, [_]*16, [_]*16, [_]*16, [_]*16, [_]*16,
        [B,r15,B,R15,B,r15,R15,B,r15,B,R15,r15,B,R15,B,r15],
        [R15,B,R15,r15,R15,R15,B,R15,R15,R15,r15,B,R15,r15,R15,R15],
        [r15,R15,r15,B,r15,R15,r15,R15,B,r15,R15,R15,r15,B,r15,R15],
        [_]*16, [_]*16, [_]*16, [_]*16, [_]*16, [_]*16, [_]*16,
    ]
    img = Image.new("RGBA", (16,16), _)
    for y, row in enumerate(pattern):
        for x, c in enumerate(row):
            img.putpixel((x,y), tint(c, power))
    return img

def make_ns(power):
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
    img = Image.new("RGBA", (16,16), _)
    for y, row in enumerate(pattern):
        for x, c in enumerate(row):
            img.putpixel((x,y), tint(c, power))
    return img


# ============================================================
# GENERATE ALL ELEMENTS
# ============================================================
print("Generating elements...")
elements = {}

print("\n--- Repeaters ---")
elements["repeater_on"]  = save_el(make_repeater(on=True),  "repeater_on")
elements["repeater_off"] = save_el(make_repeater(on=False), "repeater_off")

print("\n--- Torches ---")
elements["torch"]            = save_el(make_torch_standalone(), "torch")
elements["torch_wire_right"] = save_el(make_torch_wire("right", 14), "torch_wire_right")
elements["torch_wire_left"]  = save_el(make_torch_wire("left", 14),  "torch_wire_left")
elements["torch_wire_down"]  = save_el(make_torch_wire("down", 14),  "torch_wire_down")
elements["torch_wire_up"]    = save_el(make_torch_wire("up", 14),    "torch_wire_up")

print("\n--- Piston ---")
elements["piston"] = save_el(make_piston(), "piston")

print("\n--- Piston Extension Frames ---")
piston_frames = make_piston_extended_frames()
for ext_px, frame in piston_frames.items():
    name = f"piston_ext_{ext_px:02d}"
    frame.save(f"{OUT}/{name}_16.png")
    # Save 8x preview
    big = frame.resize((frame.width * 8, frame.height * 8), Image.NEAREST)
    big.save(f"{OUT}/{name}_8x.png")
    print(f"  {name} ({frame.width}x{frame.height})")
    elements[name] = frame

print("\n--- Lamp ---")
elements["lamp_on"]  = save_el(make_lamp_on(),  "lamp_on")
elements["lamp_off"] = save_el(make_lamp_off(), "lamp_off")

print("\n--- Redstone Block ---")
elements["rs_block"] = save_el(make_rs_block(), "rs_block")

print("\n--- Wires (sample power levels) ---")
for p in [15, 12, 9, 6, 3, 0]:
    elements[f"ew_p{p}"] = save_el(make_ew(p), f"ew_p{p}")
    elements[f"ns_p{p}"] = save_el(make_ns(p), f"ns_p{p}")


# ============================================================
# GALLERY: all elements side by side at 8x scale
# ============================================================
print("\nBuilding gallery...")
SCALE = 8
TILE = 16
PAD = 4  # padding between tiles (at scaled size)

# Layout: group by category
groups = [
    ("REPEATER", ["repeater_on", "repeater_off"]),
    ("TORCH", ["torch", "torch_wire_right", "torch_wire_left", "torch_wire_down", "torch_wire_up"]),
    ("COMPONENTS", ["piston", "lamp_on", "lamp_off", "rs_block"]),
    ("PISTON EXT", [f"piston_ext_{e:02d}" for e in range(0, 18, 2)]),
    ("WIRE EW", [f"ew_p{p}" for p in [15, 12, 9, 6, 3, 0]]),
    ("WIRE NS", [f"ns_p{p}" for p in [15, 12, 9, 6, 3, 0]]),
]

# Calculate gallery size
max_row_items = max(len(items) for _, items in groups)
scaled = TILE * SCALE  # 128px per tile

gal_w = max_row_items * (scaled + PAD) + PAD
# Calculate height per row based on tallest element in that row
row_heights = []
for gn, items in groups:
    max_h = max(elements[n].height for n in items) * SCALE
    row_heights.append(max_h)
gal_h = sum(h + PAD + 16 for h in row_heights) + PAD

BG = (20, 22, 28, 255)
gallery = Image.new("RGBA", (gal_w, gal_h), BG)

y_pos = PAD
for ri, (group_name, items) in enumerate(groups):
    x_pos = PAD
    for name in items:
        el = elements[name]
        tw = el.width * SCALE
        th = el.height * SCALE
        tile = el.resize((tw, th), Image.NEAREST)
        border = Image.new("RGBA", (tw + 4, th + 4), (50, 55, 65, 255))
        border.paste(tile, (2, 2), tile)
        gallery.paste(border, (x_pos - 2, y_pos - 2))
        x_pos += tw + PAD
    y_pos += row_heights[ri] + PAD + 16

gallery.save(f"{OUT}/gallery.png")
print(f"Gallery: {gallery.size}")

# Also save individual elements at 16x for use in circuit builder
for name, img in elements.items():
    img.save(f"{OUT}/{name}_16.png")

# ============================================================
# SAVE KEY TEXTURES to assets/ root for circuit builder use
# ============================================================
import shutil
ASSETS = "assets"
key_elements = [
    "repeater_on", "repeater_off",
    "torch", "torch_wire_right", "torch_wire_left", "torch_wire_down", "torch_wire_up",
    "piston", "lamp_on", "lamp_off", "rs_block",
] + [f"piston_ext_{e:02d}" for e in range(0, 18, 2)] + [
]
print("\nCopying key textures to assets/...")
for name in key_elements:
    src16 = f"{OUT}/{name}_16.png"
    src8x = f"{OUT}/{name}_8x.png"
    shutil.copy(src16, f"{ASSETS}/{name}_16.png")
    shutil.copy(src8x, f"{ASSETS}/{name}_8x.png")
    print(f"  -> assets/{name}_16.png + 8x")

# Also save wires for all 16 power levels
for p in range(16):
    ew = make_ew(p)
    ns = make_ns(p)
    ew.save(f"{ASSETS}/ew_p{p:02d}.png")
    ns.save(f"{ASSETS}/ns_p{p:02d}.png")
print(f"  -> assets/ew_pXX.png + ns_pXX.png (16 levels each)")

print(f"\nTotal: {len(elements)} elements generated in {OUT}/")
print("Key textures also saved to {ASSETS}/")
print("Done!")
