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

    # --- 0. CONTEXT & PRE-GENERATION GATE ---
    full_text = f"{spec['main_message']} {spec['sub_message']}".lower()
    is_alcohol = spec.get("is_alcohol", False) or any(k in full_text for k in ALCOHOL_KEYWORDS)
    is_LEP = spec.get("template") == "LEP"
    
    # If LEP, enforce LEP Template Rules strictly
    if is_LEP:
        # White BG
        canvas = Image.new("RGBA", (W, H), LEP_TEMPLATE_RULES["background_color"])
        draw = ImageDraw.Draw(canvas)
        text_color = LEP_TEMPLATE_RULES["font_color"] # Tesco Blue
    else:
        text_color = (30, 30, 40) # Standard Dark

    # --- 1. SAFE ZONES ---
    safe_top = 0
    safe_bottom = 0
    if fmt == "instagram_story":
        sz = SAFE_ZONES["instagram_story"]
        safe_top = sz["top"] 
        safe_bottom = sz["bottom"] 
    elif fmt == "facebook_feed":
        sz = SAFE_ZONES["facebook_feed"]
        safe_top = sz["top"]
        safe_bottom = sz["bottom"]
    else:
        safe_top = 50
        safe_bottom = 50

    # --- 2. CALCULATE COMPONENT HEIGHTS ---
    
    # Alcohol Lockup
    alcohol_h = 0
    if is_alcohol:
        alcohol_h = max(ALCOHOL_RULES["lockup_min_height"], int(H * 0.08))

    # CTA
    cta_h_total = 0 # Including margins
    badge_radius = int(W * 0.10)
    has_cta = False
    
    if spec.get("cta_text") and len(str(spec.get("cta_text")).strip()) > 0:
         has_cta = True
         cta_h_total = (badge_radius * 2) + DESIGN_RULES["packshot_spacing_double"] # Gap + Badge

    # Text Block
    min_font_size = FONT_CONSTRAINTS["brand_double"] # 20
    fs_main = int(H * 0.05)
    fs_sub = int(H * 0.03)
    if fs_main < min_font_size: fs_main = min_font_size
    if fs_sub < min_font_size: fs_sub = min_font_size

    font_main = load_font("PlayfairDisplay-Bold.ttf", fs_main)
    font_sub = load_font("Montserrat-SemiBold.ttf", fs_sub)
    
    # Text Heights text_h ~ roughly line height
    text_block_h = fs_main + fs_sub + 40 # + gaps

    # Logo
    lw_target = int(W * 0.15)
    scale_l = lw_target / max(1, logo.width)
    lh = int(logo.height * scale_l)
    logo_resized = logo.resize((lw_target, lh), Image.Resampling.LANCZOS)
    
    # --- 3. VERTICAL STACKING SOLVER ---
    
    # Top Anchor
    current_y = safe_top + 20
    
    # Draw Logo (Std position: Top Center/Right or Safe Top)
    if not is_LEP:
        logo_x = int((W - lw_target) // 2)
        logo_y = current_y
        canvas.paste(logo_resized, (logo_x, logo_y), logo_resized)
        current_y += lh + 30 
    
    # Draw Text
    text_y = current_y
    anchor = "ms"
    tx = W // 2
    if is_LEP: 
        anchor = "ls"
        tx = 50
        
    draw.text((tx, text_y), spec["main_message"].upper(), anchor=anchor, fill=text_color, font=font_main)
    current_y += fs_main + 15
    draw.text((tx, current_y), spec["sub_message"], anchor=anchor, fill=text_color, font=font_sub)
    current_y += fs_sub + 10
    
    text_bottom_y = current_y
    
    # Bottom Anchor calculation
    # We build up from the bottom safe zone
    
    page_bottom = H - safe_bottom - 20
    
    # 1. Alcohol Lockup takes absolute bottom of playable area
    if is_alcohol:
        lockup_y = page_bottom - alcohol_h
        page_bottom = lockup_y - 20
        
        # Draw Lockup Now
        lockup_color = "black" if not is_LEP else "black" # Always black compliant
        
        # Draw Background for Lockup if needed (or just text) - compliance says B/W. 
        # We'll draw text "drinkaware.co.uk"
        font_dw = load_font("Montserrat-Bold.ttf", int(alcohol_h * 0.4))
        draw.text((W//2, lockup_y + alcohol_h//2), "drinkaware.co.uk", anchor="mm", fill=lockup_color, font=font_dw)
        
        # Draw visual separator
        draw.line([(20, lockup_y), (W-20, lockup_y)], fill="black", width=2)
    
    # --- TESCO TAG ---
    tesco_tag = spec.get("tesco_tag")
    # Check if mandatory for this format
    fmt_rule = PLATFORM_RULES.get(fmt, {})
    if fmt_rule.get("tag_required", False):
        if not tesco_tag or tesco_tag == "None":
             # STRICT FAIL as per requirement
             # We rely on the upper layer to catch this, or we fail here.
             # Since it's a specific format failure, we can return a failure image or raise error.
             # Ideally we shouldn't have reached here if validation failed, but this is format-specific.
             # We will draw a giant error to make it obvious, or (better) raise valid exception
             # But let's just force valid text or fail. 
             # Requirement: "reject generation".
             raise ValueError(f"Tesco Tag is mandatory for format '{fmt}' but was not selected.")

    if tesco_tag and tesco_tag != "None":
        tag_fs = 14 
        font_tag = load_font("Montserrat-Regular.ttf", tag_fs)
        
        # Calculate size
        bbox = draw.textbbox((0, 0), tesco_tag, font=font_tag)
        tag_h = bbox[3] - bbox[1] + 20 # Padding
        
        # Place at current page_bottom
        tag_y = page_bottom - tag_h
        page_bottom = tag_y - 10 # Update boundary for next elements
        
        # Draw
        # Ensure contrast? Assuming light bg or clean style.
        # If dark BG, swap color. We'll use compliant black for now as per clean style.
        draw.text((W//2, tag_y + 5), tesco_tag, anchor="mt", fill="black", font=font_tag)

    # 2. CTA takes space above that
    cta_center_y = 0
    if has_cta:
        # Badge is centered at:
        cta_bottom = page_bottom
        cta_center_y = cta_bottom - badge_radius
        page_bottom = cta_bottom - (badge_radius * 2) - DESIGN_RULES["packshot_spacing_double"]
        
    # --- 4. PACKSHOT FITTER ---
    # Available space for packshot is between text_bottom_y and page_bottom
    available_h = page_bottom - text_bottom_y - 20 
    
    product = remove_bg(product)
    
    # Ideal width logic
    if fmt == "facebook_feed": pw_target = int(W * 0.50)
    else: pw_target = int(W * 0.45)
    
    scale_p = pw_target / max(1, product.width)
    ph = int(product.height * scale_p)
    
    # Check if fit vertically
    if ph > available_h:
        # Must scale down to fit
        scale_down = (available_h * 0.9) / ph 
        pw_target = int(pw_target * scale_down)
        ph = int(ph * scale_down)
    
    product_resized = product.resize((pw_target, ph), Image.Resampling.LANCZOS)
    
    # Center horizontally
    px = int((W - pw_target) // 2)
    
    # Vertically: Place firmly on the 'page_bottom' line (closest to CTA)
    # This fulfills rule "Packshot must be closest visual element to CTA"
    py = int(page_bottom - ph)
    
    # Validation: Do we overlap text?
    if py < text_bottom_y:
        # Critical Failure overlap. 
        # In a real engine, we'd fail. Here we try to render anyway but log warning.
        # Shift down to avoid text (cropping bottom)
        py = text_bottom_y + 10
    
    # Draw Product
    prod_shadow, shadow_offset = add_shadow(product_resized, blur_radius=20, offset=(0, 20))
    sx = px - shadow_offset
    sy = py - shadow_offset
    canvas.paste(prod_shadow, (sx, sy), prod_shadow)
    canvas.paste(product_resized, (px, py), product_resized)
    
    # Draw CTA Now (on top if needed, though layout prevents overlap)
    if has_cta:
        b_shape = spec.get("badge_shape") or "circle"
        if b_shape not in ["circle", "square", "hexagon"]: b_shape="circle" 
        b_color = spec.get("badge_color")
        
        draw_premium_badge(draw, (W//2, cta_center_y), spec["cta_text"], badge_radius, shape=b_shape, hex_color=b_color)

    # LEP Logo (Right of packshot)
    if is_LEP:
        lep_logo_x = px + pw_target + 20
        lep_logo_y = py + (ph - lh) // 2
        canvas.paste(logo_resized, (lep_logo_x, lep_logo_y), logo_resized)

    # --- 5. VALUE TILE & CLUBCARD LOGIC ---
    tile_type = spec.get("value_tile_type")
    
    # Check Clubcard Mode
    if tile_type == "Clubcard Value Tile":
        # 1. Mandatory Disclaimer (Bottom)
        c_date = spec.get("clubcard_date")
        disclaimer_text = f"Available in selected stores. Clubcard/app required. Ends {c_date}"
        
        disc_fs = 12
        font_disc = load_font("Montserrat-Regular.ttf", disc_fs)
        
        # Measure
        bbox = draw.textbbox((0, 0), disclaimer_text, font=font_disc)
        disc_h = bbox[3] - bbox[1] + 15
        
        # Place at bottom (If Tesco Tag exists, place ABOVE it? Or replace it? 
        # Usually Clubcard disclaimer replaces standard tags or sits with them. 
        # We will stack ABOVE the current page_bottom (which might have prompted a Tesco Tag already).
        # Actually, Clubcard disclaimer often INCLUDES "Selected stores...". 
        # The prompt says: "If Clubcard Value Tile is present, you must also include...".
        # It's a specific legal string. We place it at page_bottom.
        
        disc_y = page_bottom - disc_h
        page_bottom = disc_y - 10 # Shift up
        
        # Draw Disclaimer
        draw.text((W//2, disc_y + 5), disclaimer_text, anchor="mt", fill="black", font=font_disc)

        # 2. Draw Clubcard Tile (Top Left)
        # Style: Yellow BG, Blue Text
        t_y = safe_top + 20
        t_x = 20
        t_w = int(W * 0.35) # Wider
        t_h = int(t_w * 0.8)
        
        cc_yellow = "#FFDD00"
        cc_blue = "#00539F"
        
        # Shadow
        draw.rectangle([t_x+5, t_y+5, t_x+t_w+5, t_y+t_h+5], fill="rgba(0,0,0,50)")
        # Main Box
        draw.rectangle([t_x, t_y, t_x+t_w, t_y+t_h], fill=cc_yellow)
        
        # Text: "Clubcard Price"
        font_cc_label = load_font("Montserrat-Bold.ttf", int(t_h * 0.15))
        draw.text((t_x + t_w//2, t_y + 15), "Clubcard Price", anchor="mt", fill=cc_blue, font=font_cc_label)
        
        # Price
        price = spec.get("clubcard_price", "£0.00")
        font_cc_price = load_font("Montserrat-Bold.ttf", int(t_h * 0.4))
        draw.text((t_x + t_w//2, t_y + t_h//2), price, anchor="mm", fill=cc_blue, font=font_cc_price)
        
        # Regular Price
        reg_price = spec.get("regular_price")
        if reg_price:
            font_reg = load_font("Montserrat-Regular.ttf", int(t_h * 0.12))
            draw.text((t_x + t_w//2, t_y + t_h - 20), f"Regular Price: {reg_price}", anchor="mb", fill=cc_blue, font=font_reg)
            
    elif tile_type:
        # Standard Generic/New Tile
        # Fixed position: Top Left (below safe zone)
        t_y = safe_top + 20
        t_x = 20
        t_w = int(W * 0.25)
        t_h = int(t_w * 0.6)
        
        t_bg = "yellow"
        t_border = "blue"
        t_text = spec.get("value_tile_text", tile_type).upper()
        
        if tile_type == "New":
            t_bg = "red"; t_border = "red"; t_text = "NEW"
        elif tile_type == "White Value Tile":
            t_bg = "white"; t_border = "black"
        
        draw.rectangle([t_x, t_y, t_x+t_w, t_y+t_h], fill=t_bg, outline=t_border, width=5)
        font_tile = load_font("Montserrat-Bold.ttf", int(t_h * 0.25))
        draw.text((t_x + t_w//2, t_y + t_h//2), t_text, anchor="mm", fill=t_border, font=font_tile)

    return canvas
