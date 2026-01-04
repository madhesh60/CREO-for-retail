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
        return ImageFont.load_default()

def add_shadow(img, offset=(0, 10), blur_radius=15, shadow_color=(0, 0, 0, 80)):
    """Simple aesthetic shadow for floating objects."""
    w, h = img.size
    padding = blur_radius * 2
    
    shadow_layer = Image.new('RGBA', (w + padding, h + padding), (0,0,0,0))
    solid_shadow = Image.new('RGBA', img.size, shadow_color)
    solid_shadow.putalpha(img.split()[-1])
    
    shadow_layer.paste(solid_shadow, (padding//2 + offset[0], padding//2 + offset[1]))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(blur_radius))
    
    return shadow_layer, padding//2

def compose_creative(bg, product, logo, spec, fmt):
    """
    Strict Tesco-Compliant Composer.
    Features:
    - Universal Center Alignment (Vertical Stack) for ALL formats including Landscape.
    - 200px/250px prohibited safe zones for Stories.
    - Strict visual hierarchy (Headline -> Subhead -> Packshot -> Disclaimer -> Tag -> Drinkaware).
    - Clubcard Mode: Mandatory Date Check, Fixed Tile Position (Top-Left), Strict Disclaimer.
    - Rejects layout if space < 50px.
    """
    W, H = bg.size
    canvas = bg.copy()
    draw = ImageDraw.Draw(canvas)

    # --- 0. CONTEXT & PRE-GENERATION ---
    full_text = f"{spec.get('main_message', '')} {spec.get('sub_message', '')}".lower()
    # Alcohol check: Explicit flag OR Keyword detection
    is_alcohol = spec.get("is_alcohol", False) or any(k in full_text for k in ALCOHOL_KEYWORDS)
    is_LEP = spec.get("template") == "LEP"
    tile_type = spec.get("value_tile_type")
    
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
        # Strict Story Rules
        safe_top = 200
        safe_bottom = 250
    else:
        # Standard rules for feed/post
        sz = SAFE_ZONES.get(fmt, {"top": 50, "bottom": 50})
        safe_top = sz.get("top", 50)
        safe_bottom = sz.get("bottom", 50)

    # --- 2. CALCULATE LIMITS ---
    current_top_y = safe_top
    current_bottom_y = H - safe_bottom

    # --- 3. BOTTOM STACK (Upwards) ---
    # Stack: Drinkaware (Bottom) -> Tesco Tag -> Clubcard Disclaimer -> REST

    # A. Drinkaware
    if is_alcohol:
        # Height: ~10% of screen or min 100px
        alcohol_h = max(ALCOHOL_RULES["lockup_min_height"], int(H * 0.08))
        lockup_y = current_bottom_y - alcohol_h
        current_bottom_y = lockup_y - 20 

        dw_color = "black" 
        # Line
        draw.line([(W*0.05, lockup_y), (W*0.95, lockup_y)], fill=dw_color, width=2)
        # Text
        font_dw = load_font("Montserrat-Bold.ttf", int(alcohol_h * 0.3))
        draw.text((W//2, lockup_y + alcohol_h//2), "drinkaware.co.uk", anchor="mm", fill=dw_color, font=font_dw)

    # B. Tesco Tag
    tesco_tag = spec.get("tesco_tag")
    if tesco_tag and tesco_tag != "None":
        tag_fs = int(H * 0.018)
        if tag_fs < 14: tag_fs = 14
        font_tag = load_font("Montserrat-Regular.ttf", tag_fs)
        
        # Padding
        bbox = draw.textbbox((0, 0), tesco_tag, font=font_tag)
        tag_h = bbox[3] - bbox[1] + 10
        
        tag_y = current_bottom_y - tag_h
        current_bottom_y = tag_y - 10
        
        draw.text((W//2, tag_y), tesco_tag, anchor="mt", fill=text_color, font=font_tag)

    # C. Clubcard Disclaimer
    if tile_type == "Clubcard Value Tile":
         c_date = spec.get("clubcard_date")
         if not c_date:
             # STRICT REJECTION
             raise ValueError("Compliance Violation: Clubcard creatives MUST include an end date (DD/MM).")
             
         disclaimer = f"Available in selected stores. Clubcard/app required. Ends {c_date}"
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

    # A. Logo (Top Center)
    logo_target_w = int(W * 0.15)
    scale_l = logo_target_w / max(1, logo.width)
    logo_h = int(logo.height * scale_l)
    logo_resized = logo.resize((logo_target_w, logo_h), Image.Resampling.LANCZOS)
    
    logo_x = (W - logo_target_w) // 2
    logo_y = current_top_y + 10
    
    canvas.paste(logo_resized, (logo_x, logo_y), logo_resized)
    current_top_y = logo_y + logo_h + 30 

    # B. Headline
    headline_text = spec.get("main_message", "Headline").upper()
    fs_main = int(H * 0.045)
    font_main = load_font("PlayfairDisplay-Bold.ttf", fs_main)
    
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
        current_top_y += (bbox_s[3] - bbox_s[1]) + 40 

    # --- 5. PACKSHOT (Center Fill) ---
    # "ervey image the image shoul be in the center"
    vp_height = current_bottom_y - current_top_y
    
    if vp_height < 50:
         raise ValueError(f"Compliance Violation: Not enough vertical space ({vp_height}px) for product in {fmt}. Layout rejected.")

    product = remove_bg(product)
    
    # 85% of available height
    target_h = int(vp_height * 0.85)
    if target_h < 10: target_h = 10
    
    # Constraint by width (don't touch edges, max 80%)
    target_w_max = int(W * 0.8)
    
    # Standard calc
    p_ratio = product.width / product.height
    calc_w = int(target_h * p_ratio)
    
    if calc_w > target_w_max:
        calc_w = target_w_max
        target_h = int(calc_w / p_ratio)
    
    product_resized = product.resize((calc_w, target_h), Image.Resampling.LANCZOS)
    
    # STRICT CENTER
    # X Center: (W - calc_w) // 2
    # Y Center: Band middle
    band_center = current_top_y + (vp_height // 2)
    py = band_center - (target_h // 2)
    px = (W - calc_w) // 2
    
    # Shadow
    prod_shadow, shadow_offset = add_shadow(product_resized, blur_radius=25, offset=(0, 20))
    sx = px - shadow_offset
    sy = py - shadow_offset
    canvas.paste(prod_shadow, (sx, sy), prod_shadow)
    canvas.paste(product_resized, (px, py), product_resized)

    # --- 6. FLOATING ELEMENTS (Value Tiles) ---
    # Strictly Fixed Position: Top Left inside safe zone (Padded)
    if tile_type in ["New", "White Value Tile", "Clubcard Value Tile"]:
         t_x = 30
         t_y = safe_top + 10
         
         # Common Shadow
         # We'll calculate specific w/h per type

    if tile_type == "New":
        # Red Roundel
        r = int(W * 0.12) # Radius
        # Center of circle
        cx, cy = t_x + r, t_y + r
        
        # Shadow
        draw.ellipse([cx-r+5, cy-r+5, cx+r+5, cy+r+5], fill="rgba(0,0,0,50)")
        # Red Circle
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill="#CC0000", outline="white", width=2)
        
        # Text "NEW"
        font_new = load_font("Montserrat-Bold.ttf", int(r * 0.6))
        draw.text((cx, cy), "NEW", anchor="mm", fill="white", font=font_new)

    elif tile_type == "White Value Tile":
        # White Roundel with Price
        r = int(W * 0.14)
        cx, cy = t_x + r, t_y + r
        
        draw.ellipse([cx-r+5, cy-r+5, cx+r+5, cy+r+5], fill="rgba(0,0,0,50)")
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill="white", outline="#333333", width=1)
        
        price = spec.get("value_tile_text", "£0.00")
        # Auto-fit text check? Assuming short price.
        font_price = load_font("Montserrat-Bold.ttf", int(r * 0.5))
        draw.text((cx, cy), price, anchor="mm", fill="#CC0000", font=font_price) # Red price usually? Or black. "White Value Tile" usually has red/black price. Sticking to Red for impact, or Black for neutral. Let's use Red for price.

    elif tile_type == "Clubcard Value Tile":
         # Fixed Position: Top Left inside safe zone
         cc_x = 30
         cc_y = safe_top + 10
         
         # Width: 32% of W
         cc_w = int(W * 0.32)
         cc_h = int(cc_w * 0.75)
         
         cc_yellow = "#FFDD00"
         cc_blue = "#00539F"
         
         # Draw
         draw.rectangle([cc_x+5, cc_y+5, cc_x+cc_w+5, cc_y+cc_h+5], fill="rgba(0,0,0,50)")
         draw.rectangle([cc_x, cc_y, cc_x+cc_w, cc_y+cc_h], fill=cc_yellow)
         
         f_ccl = load_font("Montserrat-Bold.ttf", int(cc_h * 0.14))
         draw.text((cc_x + cc_w//2, cc_y + 15), "Clubcard Price", anchor="mt", fill=cc_blue, font=f_ccl)
         
         price = spec.get("clubcard_price", "£0.00")
         f_ccp = load_font("Montserrat-Bold.ttf", int(cc_h * 0.35))
         draw.text((cc_x + cc_w//2, cc_y + cc_h//2 + 5), price, anchor="mm", fill=cc_blue, font=f_ccp)

    return canvas
