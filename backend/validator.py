
import re
import cv2
import numpy as np
from compliance_rules import FORBIDDEN_TERMS, REQUIRED_TEXT_PATTERNS, PRICE_PATTERNS, ERROR_CODES, TILE_SCHEMAS, LEP_TEMPLATE_RULES

def validate_spec(spec):
    """
    Validates structural rules, Tile constraints, and LEP strictness.
    """
    errors = []
    
    # 1. Structure Check - Check for MISSING keys or empty values
    if not spec.get("main_message") or not str(spec.get("main_message")).strip():
         errors.append(f"[{ERROR_CODES['STRUCTURE_MISSING']}] Headline is mandatory.")
    if not spec.get("sub_message") or not str(spec.get("sub_message")).strip():
         errors.append(f"[{ERROR_CODES['STRUCTURE_MISSING']}] Subhead is mandatory.")
         
    # 2. Tile Constraints
    tile_type = spec.get("value_tile_type")
    if tile_type:
        schema = TILE_SCHEMAS.get(tile_type)
        if not schema:
            pass # Or fail if strictly only valid types allowed?
        else:
            # Check immutability
            if tile_type == "New":
                if spec.get("value_tile_text") and spec.get("value_tile_text") != "New":
                    errors.append(f"[{ERROR_CODES['TILE_CONSTRAINT']}] 'New' tile text is non-editable.")
            # White Value Tile -> Only price
            # Clubcard -> Offer + Regular
            
    # 3. LEP Mode Check
    if spec.get("template") == "LEP":
        # BG must be white
        if spec.get("background_color") and spec.get("background_color").upper() != "#FFFFFF":
            errors.append(f"[{ERROR_CODES['LEP_VIOLATION']}] LEP mode requires solid white background.")
        
        # Mandatory Tag
        tag = LEP_TEMPLATE_RULES["required_tag"]
        # Check if tag is present in inputs? Or assume composer adds it?
        # User says "mandatory tag text". We can auto-add or validate.
        # Let's validate if user supplied text matches? or forbid custom text?
        # Usually LEP has strict copy. 
        
    return errors

def validate_text_content(main_message, sub_message, cta_text):
    errors = []
    warnings = []
    
    # Structure Rule: Headline & Subhead Mandatory
    if not main_message or not main_message.strip():
        errors.append(f"[{ERROR_CODES['STRUCTURE_MISSING']}] Headline is MANDATORY.")
    if not sub_message or not sub_message.strip():
        errors.append(f"[{ERROR_CODES['STRUCTURE_MISSING']}] Subhead is MANDATORY.")
        
    combined_text = f"{main_message} {sub_message} {cta_text}".lower()
    
    # 0. Asterisk Check (Rule 2 & 8)
    if "*" in combined_text:
        errors.append(f"[{ERROR_CODES['FORBIDDEN_TERM']}] Asterisks (*) are strictly forbidden. No fine print allowed.")

    # 1. Dictionary Forbidden Terms Check (Rule 1-8)
    for category, terms in FORBIDDEN_TERMS.items():
        for term in terms:
            if term in combined_text:
                errors.append(f"[{ERROR_CODES['FORBIDDEN_TERM']}] Forbidden term '{term}' detected ({category}).")
            
    # 2. Price/Discount Check (Rule 6)
    for pattern in PRICE_PATTERNS:
        if re.search(pattern, combined_text):
             errors.append(f"[{ERROR_CODES['FORBIDDEN_TERM']}] Price call-outs, discounts, or money-off references are NOT allowed.")
             break

    # 3. Mandatory Tags Check (Rule 9)
    # Check Clubcard Mandatory Text & Date Format
    if "clubcard" in combined_text:
        mandatory = REQUIRED_TEXT_PATTERNS["clubcard_mandatory"]
        norm_combined = " ".join(combined_text.split())
        
        # Check specific phrases
        if "selected stores" not in norm_combined or "clubcard/app required" not in norm_combined:
             errors.append(f"[{ERROR_CODES['STRUCTURE_MISSING']}] Clubcard tile detected but mandatory text is missing/incorrect.")
        
        # Date Check: Ends DD/MM
        date_pattern = r"ends\s+(\d{1,2}/\d{1,2})"
        match = re.search(date_pattern, norm_combined)
        if not match:
             errors.append(f"[{ERROR_CODES['STRUCTURE_MISSING']}] Clubcard text must include 'Ends DD/MM' with valid format.")

    # 4. CTA Validation
    # If explicitly detecting auto-generated 'Shop Now' without user intent - we assume validator receives user intent.
    
    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

def validate_image_content(image_obj):
    """
    Detects people and alcohol bottles in the image using OpenCV.
    Returns a dict with status and flags.
    """
    try:
        # distinct conversion if it's PIL or bytes
        img = None
        if hasattr(image_obj, 'read'):
             # It's a file-like object, read it. 
             try:
                 image_bytes = image_obj.read()
                 image_obj.seek(0)
                 nparr = np.frombuffer(image_bytes, np.uint8)
                 img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
             except Exception:
                 pass
        elif hasattr(image_obj, 'resize'): 
             # It's a PIL Image
             # Convert to numpy
             img = np.array(image_obj)
             # PIL is RGB, OpenCV is BGR
             if img.shape[2] == 4: # RGBA
                 img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
             else:
                 img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if img is not None:
             # 1. Human Detection
             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
             # Load face cascade
             face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
             
             # Higher threshold to reduce false positives (Set to 10 for strictness as requested)
             faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10, minSize=(40, 40))
             
             if len(faces) > 0:
                 return {
                     "valid": False, 
                     "requires_confirmation": True, 
                     "type": "people",
                     "message": f"[{ERROR_CODES['PEOPLE_DETECTED']}] Human detected in image. Compliance confirmation required."
                 }
            
             # 2. Alcohol/Bottle Detection
             if detect_bottles(img):
                 return {
                     "valid": False,
                     "requires_compliance": True,
                     "type": "alcohol",
                     "message": f"[{ERROR_CODES['ALCOHOL_LOCKUP']}] Alcohol product visual detected. Mandatory Drinkaware compliance required."
                 }

    except Exception as e:
        print(f"Image validation error: {e}")
        pass

    return {"valid": True, "requires_confirmation": False, "requires_compliance": False}

def detect_bottles(img):
    """
    Heuristic bottle detection using contour analysis.
    Refined for better recall (catching more bottles) while maintaining precision.
    """
    try:
        height, width, _ = img.shape
        img_area = height * width
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 1. Edge Detection (Canny) 
        edges = cv2.Canny(gray, 50, 150)
        
        # Dilation to close gaps
        kernel = np.ones((5,5),np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=2)
        
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            
            # Filter noise (0.5% area) and full-screen backgrounds (>90% area)
            if area < (img_area * 0.005) or area > (img_area * 0.9): 
                continue
                
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(h) / w
            
            # Bottles are vertically oriented.
            # Range 1.5 (stout) to 6.5 (tall)
            if 1.5 < aspect_ratio < 6.5:
                # Rectangularity check: extent
                rect_area = w * h
                extent = float(area) / rect_area
                
                # Bottles have necks, so they fill less of their bounding rect than a box.
                # 0.4 - 0.85 allows for various bottle shapes.
                if 0.4 < extent < 0.85:
                    return True
                
    except Exception as e:
        print(f"Bottle detection error: {e}")
        
    return False

def validate_layout(fmt, width, height, elements):
    # Placeholder for geometric validation (e.g. is logo top_right?)
    # elements = [{"type": "logo", "box": (x1, y1, x2, y2)}, ...]
    return True
