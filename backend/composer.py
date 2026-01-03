import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageColor
import random
import math
from background_removal import remove_bg
from compliance_rules import SAFE_ZONES, FONT_CONSTRAINTS, DESIGN_RULES, ALCOHOL_RULES, ALCOHOL_KEYWORDS, LEP_TEMPLATE_RULES, PLATFORM_RULES

# --- ASSETS SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")

def load_font(font_name, size):
    path = os.path.join(FONTS_DIR, font_name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        # Fallback to default if custom font missing
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
    """Draws a premium-looking badge. Kept for non-strict formats or if strictly requested."""
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
    """
    Strict Tesco-Compliant Composer.
    Enforces safe zones (especially for Stories), hierarchy, and clean layout.
    """
    W, H = bg.size
    canvas = bg.copy()
    draw = ImageDraw.Draw(canvas)

    # --- 0. CONTEXT & PRE-GENERATION ---
    full_text = f"{spec.get('main_message', '')} {spec.get('sub_message', '')}".lower()
    is_alcohol = spec.get("is_alcohol", False) or any(k in full_text for k in ALCOHOL_KEYWORDS)
    is_LEP = spec.get("template") == "LEP"
    
    # Colors
    if is_LEP:
        canvas = Image.new("RGBA", (W, H), LEP_TEMPLATE_RULES["background_color"])
        draw = ImageDraw.Draw(canvas)
        text_color = LEP_TEMPLATE_RULES["font_color"]
    else:
        text_color = (30, 30, 40) # Standard Dark

    # --- 1. STRICT SAFE ZONES ---
    safe_top = 50
    safe_bottom = 50

    if fmt == "instagram_story":
        # STORY STRICT RULE: Top 200px, Bottom 250px CLEARED
        safe_top = 200
        safe_bottom = 250
    elif fmt == "facebook_feed":
        sz = SAFE_ZONES.get("facebook_feed", {"top": 50, "bottom": 50})
        safe_top = sz["top"]
        safe_bottom = sz["bottom"]

    # --- 2. CALCULATE LIMITS ---
    # We define the "Playable Area" between current_top_y and current_bottom_y
    current_top_y = safe_top
    current_bottom_y = H - safe_bottom

    # --- 3. BOTTOM STACK (Upwards) ---
    # Stack Order from bottom: Drinkaware -> Tesco Tag -> Clubcard -> REST

    # A. Drinkaware (Deepest)
    if is_alcohol:
        # Height: ~10% of screen or min 100px
        alcohol_h = max(ALCOHOL_RULES["lockup_min_height"], int(H * 0.08))
        
        lockup_y = current_bottom_y - alcohol_h
        current_bottom_y = lockup_y - 20 # Padding

        # Draw
        dw_color = "black" # High contrast requirement
        # Separator
        draw.line([(W*0.05, lockup_y), (W*0.95, lockup_y)], fill=dw_color, width=2)
        # Text
        font_dw = load_font("Montserrat-Bold.ttf", int(alcohol_h * 0.3))
        draw.text((W//2, lockup_y + alcohol_h//2), "drinkaware.co.uk", anchor="mm", fill=dw_color, font=font_dw)

    # B. Tesco Tag (Mandatory if present)
    tesco_tag = spec.get("tesco_tag")
    if tesco_tag and tesco_tag != "None":
        tag_fs = int(H * 0.018)
        if tag_fs < 14: tag_fs = 14
        font_tag = load_font("Montserrat-Regular.ttf", tag_fs)
        
        bbox = draw.textbbox((0, 0), tesco_tag, font=font_tag)
        tag_h = bbox[3] - bbox[1] + 10
        
        tag_y = current_bottom_y - tag_h
        current_bottom_y = tag_y - 10
        
        draw.text((W//2, tag_y), tesco_tag, anchor="mt", fill=text_color, font=font_tag)

    # C. Clubcard Disclaimer (If needed)
    tile_type = spec.get("value_tile_type")
    if tile_type == "Clubcard Value Tile":
         c_date = spec.get("clubcard_date", "Selected dates")
         disclaimer = f"Selected stores. Clubcard/app required. Ends {c_date}"
         
         disc_fs = int(H * 0.012)
         if disc_fs < 12: disc_fs = 12
         font_disc = load_font("Montserrat-Regular.ttf", disc_fs)
         
         bbox_d = draw.textbbox((0, 0), disclaimer, font=font_disc)
         disc_h = bbox_d[3] - bbox_d[1] + 5
         
         disc_y = current_bottom_y - disc_h
         current_bottom_y = disc_y - 15
         
         draw.text((W//2, disc_y), disclaimer, anchor="mt", fill=text_color, font=font_disc)

    # --- 4. TOP STACK (Downwards) ---
    # Logo -> Headline -> Subhead

    # A. Logo (Top Center, inside Safe Zone)
    # Resize Logic
    logo_target_w = int(W * 0.15)
    scale_l = logo_target_w / max(1, logo.width)
    logo_h = int(logo.height * scale_l)
    logo_resized = logo.resize((logo_target_w, logo_h), Image.Resampling.LANCZOS)
    
    logo_x = (W - logo_target_w) // 2
    logo_y = current_top_y + 10 # Padding inside safe zone
    
    canvas.paste(logo_resized, (logo_x, logo_y), logo_resized)
    current_top_y = logo_y + logo_h + 30 # Gap

    # B. Headline
    headline_text = spec.get("main_message", "Headline").upper()
    fs_main = int(H * 0.045)
    font_main = load_font("PlayfairDisplay-Bold.ttf", fs_main)
    
    # Check width fit?
    # Simple wrap logic could be here, but assuming short headline for now.
    draw.text((W//2, current_top_y), headline_text, anchor="mt", fill=text_color, font=font_main)
    
    bbox_h = draw.textbbox((0, 0), headline_text, font=font_main)
    current_top_y += (bbox_h[3] - bbox_h[1]) + 20

    # C. Subhead
    sub_text = spec.get("sub_message", "")
    if sub_text:
        fs_sub = int(H * 0.025)
        font_sub = load_font("Montserrat-SemiBold.ttf", fs_sub)
        
        draw.text((W//2, current_top_y), sub_text, anchor="mt", fill=text_color, font=font_sub)
        
        bbox_s = draw.textbbox((0, 0), sub_text, font=font_sub)
        current_top_y += (bbox_s[3] - bbox_s[1]) + 40 # Large gap before product

    # --- 5. CENTER STACK (Packshot) ---
    # Fills space between current_top_y and current_bottom_y
    
    vp_height = current_bottom_y - current_top_y
    
    if vp_height < 50:
         # Critical specific error: Reject layout as per strict rules
         raise ValueError(f"Strict Compliance Violation: Not enough vertical space ({vp_height}px) for product in {fmt}. Layout rejected.")

    # Product Processing
    product = remove_bg(product)
    
    # Target: Fill 80% of viewport height?
    target_h = int(vp_height * 0.85)
    if target_h < 10: target_h = 10
    
    # Constrain by width (don't touch edges)
    target_w_max = int(W * 0.8)
    
    # Calculate dimensions
    p_ratio = product.width / product.height
    
    calc_w = int(target_h * p_ratio)
    
    if calc_w > target_w_max:
        # Too wide, constrain by width
        calc_w = target_w_max
        target_h = int(calc_w / p_ratio)
    
    # Resize
    product_resized = product.resize((calc_w, target_h), Image.Resampling.LANCZOS)
    
    # Position: EXACT CENTER of the viewport band
    band_center = current_top_y + (vp_height // 2)
    py = band_center - (target_h // 2)
    px = (W - calc_w) // 2
    
    # Draw Shadow
    prod_shadow, shadow_offset = add_shadow(product_resized, blur_radius=25, offset=(0, 20))
    sx = px - shadow_offset
    sy = py - shadow_offset
    canvas.paste(prod_shadow, (sx, sy), prod_shadow)
    
    # Draw Product
    canvas.paste(product_resized, (px, py), product_resized)
    
    # --- 6. CTA / BADGES ---
    # Only if present and space permits.
    # User said: "CTA elements are not allowed unless explicitly enabled... ignore dummy text"
    # We will IGNORE CTA for strict compliance unless a specific flag "enable_cta" is true.
    # Spec doesn't seem to have "enable_cta".
    # But if `cta_text` is present, usually that calls for a button. 
    # Strict compliance: "Do not create custom badges...".
    # I will SKIP CTA rendering to adhere to "clean, balanced, and boring" and "ignore dummy text".
    
    # Re-adding Clubcard Tile (Top Left) if needed?
    if tile_type == "Clubcard Value Tile":
         # Clubcard Badge usually goes Top Left.
         # Must be inside safe zone.
         # top: safe_top + 10, left: 20
         cc_w = int(W * 0.3)
         cc_h = int(cc_w * 0.8)
         cc_x = 30
         cc_y = safe_top + 10
         
         # Draw simple rectangle
         cc_yellow = "#FFDD00"
         cc_blue = "#00539F"
         draw.rectangle([cc_x, cc_y, cc_x+cc_w, cc_y+cc_h], fill=cc_yellow)
         
         f_ccl = load_font("Montserrat-Bold.ttf", int(cc_h * 0.15))
         draw.text((cc_x + cc_w//2, cc_y + 15), "Clubcard Price", anchor="mt", fill=cc_blue, font=f_ccl)
         
         price = spec.get("clubcard_price", "£0.00")
         f_ccp = load_font("Montserrat-Bold.ttf", int(cc_h * 0.4))
         draw.text((cc_x + cc_w//2, cc_y + cc_h//2), price, anchor="mm", fill=cc_blue, font=f_ccp)

    return canvas
