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
        # Height: ~10% of screen or min 20px (Strict Rule)
        min_dh = ALCOHOL_RULES.get("lockup_min_height", 20)
        alcohol_h = max(min_dh, int(H * 0.08))
        lockup_y = current_bottom_y - alcohol_h
        current_bottom_y = lockup_y - 20 

        # Contrast Check
        # Sample the background in the lockup area to determine color
        # Since canvas might be RGBA, we handle transparency if needed, but usually BG is solid.
        # We'll take a crop of the bottom area
        try:
            # Crop box: (0, lockup_y, W, lockup_y + alcohol_h)
            # Resize to 1x1 to get average color
            region = canvas.crop((0, int(lockup_y), int(W), int(lockup_y + alcohol_h)))
            avg_color = region.resize((1, 1)).getpixel((0, 0))
            
            # Brightness formula: (R+G+B)/3 or luminance
            if len(avg_color) >= 3:
                brightness = sum(avg_color[:3]) / 3
            else:
                brightness = 255 # Default white
            
            dw_color = "white" if brightness < 128 else "black"
        except Exception:
            dw_color = "black" # Fallback

        # Line
        draw.line([(W*0.05, lockup_y), (W*0.95, lockup_y)], fill=dw_color, width=2)
        # Text
        font_dw = load_font("Montserrat-Bold.ttf", int(alcohol_h * 0.45))
        draw.text((W//2, lockup_y + alcohol_h//2), "drinkaware.co.uk", anchor="mm", fill=dw_color, font=font_dw)

    # B. Tesco Tag
    tesco_tag = spec.get("tesco_tag")
    if tesco_tag and tesco_tag != "None":
        tag_fs = int(H * 0.025)
        if tag_fs < 16: tag_fs = 16
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
         disc_fs = int(H * 0.018)
         if disc_fs < 14: disc_fs = 14
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

    # --- 5. CENTER CONTENT (Strict Product Centering + Sidekick) ---
    # Strategy: Product is ALWAYS visual center. Sidekick hangs to the right.
    # If Sidekick hits edge, we scale down the Product to make room, but KEEP Product centered.
    
    side_element = None
    side_w, side_h = 0, 0
    gap = 30 # px
    
    # A. Determine Sidekick
    if tile_type == "Clubcard Value Tile":
        side_element = "Clubcard"
        # Dimensions for Clubcard (Reduce to ~26% W as requested, maintaining aspect)
        side_w = int(W * 0.26)
        side_h = int(side_w * 0.75)
    elif spec.get("cta_text") and not is_alcohol: 
        # Render CTA if text exists (and not overridden by Clubcard)
        side_element = "CTA"
        cta_txt = spec.get("cta_text", "SHOP NOW").upper()
        # Estimate dimensions
        est_fs = int(H * 0.02)
        if est_fs < 14: est_fs = 14
        f_cta = load_font("Montserrat-Bold.ttf", est_fs)
        bbox_c = draw.textbbox((0,0), cta_txt, font=f_cta)
        txt_w = bbox_c[2] - bbox_c[0]
        side_w = txt_w + 60 # Padding
        side_h = int(est_fs * 2.5) 

    # B. Vertical Space Calculation
    vp_height = current_bottom_y - current_top_y
    if vp_height < 50:
         raise ValueError(f"Compliance Violation: Not enough vertical space ({vp_height}px) for product. Layout rejected.")

    # C. Product Prep
    product = remove_bg(product)
    p_ratio = product.width / product.height
    
    # Initial Target Height for Product (85% of viewport)
    target_h = int(vp_height * 0.85)
    if target_h < 10: target_h = 10
    calc_pw = int(target_h * p_ratio)
    
    # D. Strict Centering & Side Constraint Logic
    # Concept: We have width W. Center is W/2.
    # Product occupies [W/2 - pw/2, W/2 + pw/2].
    # Sidekick occupies [W/2 + pw/2 + gap, W/2 + pw/2 + gap + side_w].
    # Constraint: The Right Edge of Sidekick must be < W - margin.
    
    safe_margin_x = int(W * 0.05)
    max_x = W - safe_margin_x
    
    current_right_edge = (W // 2) + (calc_pw // 2) + (gap + side_w if side_element else 0)
    
    if current_right_edge > max_x:
        # We need to shrink the Product (which shrinks pw). 
        # Sidekick size is fixed or proportional? Let's scale Sidekick proportionally too to maintain balance.
        # Equation: (W/2) + (h*ratio / 2) + gap + (side_w * scalefactor?) ... roughly.
        # Easier approach: Calculate required reduction factor.
        
        # Available width for (HalfProduct + Gap + Sidekick)
        available_right_width = (W // 2) - safe_margin_x
        required_right_width = (calc_pw // 2) + (gap + number_or_zero(side_w) if side_element else 0)
        
        scale_factor = available_right_width / required_right_width
        
        # Apply Scale
        target_h = int(target_h * scale_factor)
        calc_pw = int(target_h * p_ratio)
        if side_element:
            side_w = int(side_w * scale_factor)
            side_h = int(side_h * scale_factor)
            gap = int(gap * scale_factor)

    # E. Positioning (STRICT CENTER)
    product_resized = product.resize((calc_pw, target_h), Image.Resampling.LANCZOS)
    
    # Center X
    px = (W - calc_pw) // 2
    
    # Center Y (Visual Band)
    band_center = current_top_y + (vp_height // 2)
    py = band_center - (target_h // 2)
    
    # F. Render Product
    prod_shadow, shadow_offset = add_shadow(product_resized, blur_radius=25, offset=(0, 20))
    canvas.paste(prod_shadow, (px - shadow_offset, py - shadow_offset), prod_shadow)
    canvas.paste(product_resized, (px, py), product_resized)
    
    # G. Render Sidekick (Right Side)
    if side_element:
        sx = px + calc_pw + gap
        sy = band_center - (side_h // 2) # Vertically centered to product visual center
        
        if side_element == "CTA":
            # Draw CTA Button (Pill Shape)
            cta_color = "#00539F" # Tesco Blue
            draw.rounded_rectangle([sx, sy, sx+side_w, sy+side_h], radius=side_h//2, fill=cta_color)
            
            # Text
            f_cta_render = load_font("Montserrat-Bold.ttf", int(side_h * 0.4))
            draw.text((sx + side_w//2, sy + side_h//2), cta_txt, anchor="mm", fill="white", font=f_cta_render)
            
        elif side_element == "Clubcard":
             # Draw Clubcard Tile (Yellow/Blue Lozenge style or Rect)
             cc_w, cc_h = side_w, side_h
             cc_x, cc_y = sx, sy
             
             cc_yellow = "#FFDD00"
             cc_blue = "#00539F"
             
             # Shadow
             draw.rectangle([cc_x+5, cc_y+5, cc_x+cc_w+5, cc_y+cc_h+5], fill="rgba(0,0,0,50)")
             draw.rectangle([cc_x, cc_y, cc_x+cc_w, cc_y+cc_h], fill=cc_yellow)
             
             f_ccl = load_font("Montserrat-Bold.ttf", int(cc_h * 0.18))
             draw.text((cc_x + cc_w//2, cc_y + 15), "Clubcard Price", anchor="mt", fill=cc_blue, font=f_ccl)
             
             price = spec.get("clubcard_price", "£0.00")
             f_ccp = load_font("Montserrat-Bold.ttf", int(cc_h * 0.42))
             draw.text((cc_x + cc_w//2, cc_y + cc_h//2 + 5), price, anchor="mm", fill=cc_blue, font=f_ccp)

    return canvas
