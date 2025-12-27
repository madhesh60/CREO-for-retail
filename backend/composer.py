import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageColor
import random
import math
from background_removal import remove_bg

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
    # Make a blank image bigger than the original to hold the shadow
    padding = blur_radius * 2
    shadow_img = Image.new('RGBA', (w + padding, h + padding), (0,0,0,0))
    
    # Create the shadow shape (alpha mask)
    shadow_mask = img.split()[-1] if img.mode == 'RGBA' else img.convert("L")
    shadow_mask = ImageOps.invert(shadow_mask) # Need content to be black? No, mask: 255=opaque
    
    # Actually, simpler way: draw the alpha channel in shadow color
    shadow = Image.new('RGBA', (w + padding, h + padding), (0,0,0,0))
    # Paste the source image's alpha channel as the shadow color
    # (Simplified: Just drawing a dark oval for product shadow or drop shadow)
    
    # Let's do a simple drop shadow approach
    shadow_layer = Image.new('RGBA', (w + padding, h + padding), (0,0,0,0))
    shadow_content = img.copy()
    
    # Create a solid color version of the image
    solid_shadow = Image.new('RGBA', img.size, shadow_color)
    solid_shadow.putalpha(img.split()[-1])
    
    shadow_layer.paste(solid_shadow, (padding//2 + offset[0], padding//2 + offset[1]))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Crop back to reasonable relative size or return the large layer and offset
    return shadow_layer, padding//2

def draw_premium_badge(draw, center, text, radius, shape="circle", hex_color=None):
    """Draws a premium-looking badge with dynamic shape and color."""
    x, y = center
    
    # Palette
    if hex_color:
        try:
            primary_color = ImageColor.getrgb(hex_color)
            # Create a lighter/darker version for gradient effect (simplified)
            # Just use the color provided
            fill_color = primary_color
            border_color = (255, 255, 255) # White border for contrast
        except ValueError:
             # Fallback to Gold
            fill_color = (218, 165, 32)
            border_color = (255, 215, 0)
    else:
        # Default Gold
        fill_color = (218, 165, 32)
        border_color = (255, 215, 0)

    # Draw Shape
    if shape == "square":
        # Rounded square
        r = radius
        draw.rounded_rectangle(
            [x - r, y - r, x + r, y + r],
            radius=r*0.2,
            fill=fill_color,
            outline=border_color,
            width=3
        )
    elif shape == "hexagon":
        # Hexagon points
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30 
            angle_rad = math.pi / 180 * angle_deg
            px = x + radius * math.cos(angle_rad)
            py = y + radius * math.sin(angle_rad)
            points.append((px, py))
        draw.polygon(points, fill=fill_color, outline=border_color)
    else:
        # Circle (Default)
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=fill_color,
            outline=border_color,
            width=3
        )
    
    # Text
    font_size = int(radius * 0.4)
    font = load_font("Montserrat-SemiBold.ttf", font_size)
    
    # Word wrap manually for badge (max 2 lines usually)
    words = text.split()
    
    # Contrast text color based on brightness? Simplify to white or dark.
    # If gold (default), dark text looks good. If custom color, white text is usually safer for vibrant colors.
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

    # --- PROCESS IMAGES ---
    product = remove_bg(product)
    logo = remove_bg(logo)

    # --- LAYOUT CONFIG ---
    # Reference style:
    # Top: Logo (Small, Centered or Left)
    # Middle: Product
    # Middle-Left: Floating Medal/Badge
    # Bottom: Headlines
    
    # --- 1. LOGO ---
    # Clean, Top Center
    lw_target = int(W * 0.15)
    scale_l = lw_target / max(1, logo.width)
    lh = int(logo.height * scale_l)
    logo_resized = logo.resize((lw_target, lh), Image.Resampling.LANCZOS)
    
    logo_y = int(H * 0.05) if fmt != "instagram_story" else int(H * 0.08)
    # Center logo
    logo_x = (W - lw_target) // 2
    canvas.paste(logo_resized, (logo_x, logo_y), logo_resized)
    
    # --- 2. PRODUCT ---
    # Center, large
    if fmt == "facebook_feed": # 1:1
        pw_target = int(W * 0.4)
    elif fmt == "instagram_story": # 9:16
        pw_target = int(W * 0.6)
    else: # Landscape
        pw_target = int(W * 0.25)
        
    scale_p = pw_target / max(1, product.width)
    ph = int(product.height * scale_p)
    product_resized = product.resize((pw_target, ph), Image.Resampling.LANCZOS)
    
    # Generate Drop Shadow
    prod_shadow, shadow_offset = add_shadow(product_resized, blur_radius=20, offset=(0, 20))
    
    # Position
    # Centered horizontally
    px = (W - pw_target) // 2
    # Vertical: slightly above center to leave room for text
    py = int(H * 0.45) - (ph // 2)
    
    # Paste Shadow then Product
    sx = px - shadow_offset
    sy = py - shadow_offset
    canvas.paste(prod_shadow, (sx, sy), prod_shadow)
    canvas.paste(product_resized, (px, py), product_resized)
    
    # --- 3. BADGE (Floating Sticker) ---
    # Left of product?
    badge_radius = int(W * 0.09)
    # Position: To the left of product top-half
    if fmt == "instagram_story":
        bx = px - int(badge_radius * 1.5)
        by = py + int(ph * 0.1)
    else:
        # Standard layout
        bx = px - int(badge_radius * 1.2)
        by = py + int(ph * 0.2)
        
    # Ensure badge doesn't go off screen
    bx = max(bx, badge_radius + 20)
    
    if spec["cta_text"]:
        # Pick dynamic badge if not specified
        b_shape = spec.get("badge_shape")
        if not b_shape:
            b_shape = random.choice(["circle", "square", "hexagon"])
            
        b_color = spec.get("badge_color") 
        # If no color specified, maybe random vibrant color? 
        # Or keep default gold if not playing with colors.
        # User asked: "batches and the format should be dynamic", implies variety.
        # if not b_color:
        #    b_color = random.choice(["#ff0055", "#0055ff", "#22cc55", "#ffaa00"]) 
        # Leaving default as gold for safety unless specified, but shape varies.

        draw_premium_badge(draw, (bx, by), spec["cta_text"], badge_radius, shape=b_shape, hex_color=b_color)
    
    # --- 4. TEXT ---
    main_msg = spec["main_message"]
    sub_msg = spec["sub_message"]
    
    # Font Sizes
    if fmt == "instagram_story":
        fs_main = int(H * 0.04)
        fs_sub  = int(H * 0.025)
        ty_start = py + ph + 80
    else:
        fs_main = int(H * 0.06)
        fs_sub  = int(H * 0.035)
        ty_start = py + ph + 60

    font_main = load_font("PlayfairDisplay-Bold.ttf", fs_main)
    font_sub = load_font("Montserrat-SemiBold.ttf", fs_sub)
    
    # Draw Main
    # We want to properly center text with potentially multiple lines if too long?
    # For now assume relatively short headlines.
    
    draw.text((W//2, ty_start), main_msg.upper(), anchor="mt", fill=(30,30,40), font=font_main)
    
    # Draw Sub
    draw.text((W//2, ty_start + fs_main + 15), sub_msg, anchor="mt", fill=(60,60,70), font=font_sub)
    
    return canvas
