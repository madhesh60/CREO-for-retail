import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageColor
import random
import math
from background_removal import remove_bg
from compliance_rules import SAFE_ZONES

# --- ASSETS SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")

def load_font(font_name, size):
    path = os.path.join(FONTS_DIR, font_name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()

def add_shadow(img, offset=(0, 10), blur_radius=15, shadow_color=(0, 0, 0, 80)):
    """Simple aesthetic shadow for floating objects."""
    w, h = img.size
    padding = blur_radius * 2
    
    shadow_layer = Image.new('RGBA', (w + padding, h + padding), (0,0,0,0))
    
    # Create a solid color version of the image
    solid_shadow = Image.new('RGBA', img.size, shadow_color)
    solid_shadow.putalpha(img.split()[-1])
    
    shadow_layer.paste(solid_shadow, (padding//2 + offset[0], padding//2 + offset[1]))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(blur_radius))
    
    return shadow_layer, padding//2

def draw_premium_badge(draw, center, text, radius, shape="circle", hex_color=None):
    """Draws a premium-looking badge with dynamic shape and color."""
    x, y = center
    
    # Palette
    if hex_color:
        try:
            primary_color = ImageColor.getrgb(hex_color)
            fill_color = primary_color
            border_color = (255, 255, 255) 
        except ValueError:
            fill_color = (218, 165, 32)
            border_color = (255, 215, 0)
    else:
        # Default Gold
        fill_color = (218, 165, 32)
        border_color = (255, 215, 0)

    # Draw Shape
    if shape == "square":
        r = radius
        draw.rounded_rectangle(
            [x - r, y - r, x + r, y + r],
            radius=r*0.2,
            fill=fill_color,
            outline=border_color,
            width=3
        )
    elif shape == "hexagon":
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30 
            angle_rad = math.pi / 180 * angle_deg
            px = x + radius * math.cos(angle_rad)
            py = y + radius * math.sin(angle_rad)
            points.append((px, py))
        draw.polygon(points, fill=fill_color, outline=border_color)
    else:
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=fill_color,
            outline=border_color,
            width=3
        )
    
    # Text
    font_size = int(radius * 0.4)
    font = load_font("Montserrat-SemiBold.ttf", font_size)
    
    words = text.split()
    text_color = (50, 40, 0) if not hex_color else (255, 255, 255)

    if len(words) > 1:
        line1 = " ".join(words[:len(words)//2 + 1])
        line2 = " ".join(words[len(words)//2 + 1:])
        
        draw.text((x, y - font_size*0.6), line1.upper(), anchor="mm", fill=text_color, font=font)
        draw.text((x, y + font_size*0.6), line2.upper(), anchor="mm", fill=text_color, font=font)
    else:
        draw.text((x, y), text.upper(), anchor="mm", fill=text_color, font=font)


def compose_creative(bg, product, logo, spec, fmt):
    W, H = bg.size
    canvas = bg.copy()
    draw = ImageDraw.Draw(canvas)

    # --- SAFE ZONES ---
    # Determine safe area based on format
    # 9x16 usually corresponds to instagram_story
    safe_top = 0
    safe_bottom = 0
    
    if fmt == "instagram_story": # 1080x1920
        safe_zone = SAFE_ZONES.get("9x16", {})
        safe_top = safe_zone.get("top", 200)
        safe_bottom = safe_zone.get("bottom", 250)
    
    valid_h = H - safe_top - safe_bottom
    content_start_y = safe_top
    
    # --- PROCESS IMAGES ---
    product = remove_bg(product)
    logo = remove_bg(logo)

    # --- 1. LOGO ---
    lw_target = int(W * 0.15)
    scale_l = lw_target / max(1, logo.width)
    lh = int(logo.height * scale_l)
    logo_resized = logo.resize((lw_target, lh), Image.Resampling.LANCZOS)
    
    # Position: Top Center but respected SAFE ZONE
    # For stories, below top safe zone. For others, just padding.
    logo_y = content_start_y + int(H * 0.02)
    logo_x = (W - lw_target) // 2
    canvas.paste(logo_resized, (logo_x, logo_y), logo_resized)
    
    # Update next available Y
    current_y = logo_y + lh + int(H * 0.03)

    # --- 2. PRODUCT ---
    if fmt == "facebook_feed": # 1:1
        pw_target = int(W * 0.45)
    elif fmt == "instagram_story": # 9:16
        pw_target = int(W * 0.65)
    else: # Landscape
        pw_target = int(W * 0.25)
        
    scale_p = pw_target / max(1, product.width)
    ph = int(product.height * scale_p)
    product_resized = product.resize((pw_target, ph), Image.Resampling.LANCZOS)
    
    # Generate Drop Shadow
    prod_shadow, shadow_offset = add_shadow(product_resized, blur_radius=20, offset=(0, 20))
    
    # Position
    px = (W - pw_target) // 2
    
    # Vertical: Adaptive.
    # Try to center in the remaining valid space between logo and bottom text area
    # Or just fixed logic relative to safe zone.
    # Let's place it at roughly 35-40% of visual center of valid area
    
    # approximate center of safe area
    safe_center_y = content_start_y + (valid_h // 2)
    py = safe_center_y - (ph // 2) - int(H * 0.05) # Shift up slightly
    
    # Paste Shadow then Product
    sx = px - shadow_offset
    sy = py - shadow_offset
    canvas.paste(prod_shadow, (sx, sy), prod_shadow)
    canvas.paste(product_resized, (px, py), product_resized)
    
    # --- 3. BADGE (Floating Sticker) ---
    badge_radius = int(W * 0.09)
    bx = px - int(badge_radius * 1.1)
    by = py + int(ph * 0.85) # Lower corner
    
    # Constraints
    bx = max(bx, badge_radius + 10)
    
    if spec["cta_text"]:
        b_shape = spec.get("badge_shape") or random.choice(["circle", "square", "hexagon"])
        b_color = spec.get("badge_color")
        draw_premium_badge(draw, (bx, by), spec["cta_text"], badge_radius, shape=b_shape, hex_color=b_color)
    
    # --- 4. TEXT ---
    main_msg = spec["main_message"]
    sub_msg = spec["sub_message"]
    
    if fmt == "instagram_story":
        fs_main = int(H * 0.04)
        fs_sub  = int(H * 0.025)
        # Position at bottom logic, but ABOVE safe bottom
        # Bottom safe zone is H - safe_bottom
        # We assume bottom area is for UI, so we put text just above it
        text_baseline = H - safe_bottom - fs_sub - fs_main - 60
    else:
        fs_main = int(H * 0.06)
        fs_sub  = int(H * 0.035)
        text_baseline = py + ph + 40

    font_main = load_font("PlayfairDisplay-Bold.ttf", fs_main)
    font_sub = load_font("Montserrat-SemiBold.ttf", fs_sub)
    
    # Draw Main
    draw.text((W//2, text_baseline), main_msg.upper(), anchor="ms", fill=(30,30,40), font=font_main)
    
    # Draw Sub
    draw.text((W//2, text_baseline + fs_main + 10), sub_msg, anchor="ms", fill=(60,60,70), font=font_sub)
    
    return canvas
