import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
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

def draw_premium_badge(draw, center, text, radius):
    """Draws a gold, premium-looking circular badge."""
    x, y = center
    
    # Gold Palette
    gold_outer = (218, 165, 32)
    gold_inner = (255, 215, 0)
    
    # Outer ring
    draw.ellipse(
        [x - radius, y - radius, x + radius, y + radius],
        fill=gold_outer
    )
    # Inner circle
    inset = 4
    draw.ellipse(
        [x - radius + inset, y - radius + inset, x + radius - inset, y + radius - inset],
        fill=gold_inner
    )
    
    # Text
    font_size = int(radius * 0.4)
    font = load_font("Montserrat-SemiBold.ttf", font_size)
    
    # Word wrap manually for badge (max 2 lines usually)
    words = text.split()
    if len(words) > 1:
        line1 = " ".join(words[:len(words)//2 + 1])
        line2 = " ".join(words[len(words)//2 + 1:])
        
        # Draw lines centered
        # Ascent/Descent calculation is complex, simplified centering:
        draw.text((x, y - font_size*0.6), line1.upper(), anchor="mm", fill=(50, 40, 0), font=font)
        draw.text((x, y + font_size*0.6), line2.upper(), anchor="mm", fill=(50, 40, 0), font=font)
    else:
        draw.text((x, y), text.upper(), anchor="mm", fill=(50, 40, 0), font=font)


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
        draw_premium_badge(draw, (bx, by), spec["cta_text"], badge_radius)
    
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
