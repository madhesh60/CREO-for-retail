from formats import FORMATS
from background_generator import generate_background
from composer import compose_creative
from exporter import export_image
from validator import validate_text_content, validate_image_content, validate_spec

def generate_all(spec, product, logo):
    outputs = {}
    
    # 0. Spec Validation (Fail Fast)
    spec_errors = validate_spec(spec)
    if spec_errors:
        return {
            "validation": {
                "valid": False, 
                "errors": spec_errors, 
                "warnings": []
            }
        }

    # 1. Text Validation
    validation = validate_text_content(
        spec.get("main_message", ""),
        spec.get("sub_message", ""),
        spec.get("cta_text", "")
    )
    
    # 2. Image Validation (People & Alcohol Detection)
    # We validate the product image (PIL object)
    img_val = validate_image_content(product)
    
    if not img_val["valid"]:
        # Handle People Detection
        if img_val.get("type") == "people":
            if not spec.get("confirm_people", False):
                validation["valid"] = False
                validation["errors"].append(img_val["message"])
                validation["requires_confirmation"] = True
        
        # Handle Alcohol Detection
        elif img_val.get("type") == "alcohol":
            if not spec.get("confirm_drinkaware", False):
                validation["valid"] = False
                validation["errors"].append(img_val["message"])
                validation["requires_compliance"] = True
            else:
                # User confirmed compliance, force alcohol mode in composer
                spec["is_alcohol"] = True

    outputs["validation"] = validation

    # Block generation on hard failure
    if not validation["valid"]:
        return outputs
    
    for fmt, (W, H) in FORMATS.items():
        bg = generate_background("clean", W, H, custom_color=spec.get("background_color"))
        
        try:
            # Pass validation warnings/flags to composer if needed
            img = compose_creative(bg, product, logo, spec, fmt)
            
            # Requirement: Enable download in final Jpeg and Png.
            # We generate both
            png_b64 = export_image(img, format="PNG")
            jpg_b64 = export_image(img, format="JPEG", max_size_kb=500)
            
            outputs[fmt] = {
                "png": png_b64,
                "jpg": jpg_b64
            }
        except ValueError as e:
            # Handle specific composition failures (e.g. Mandatory Tag missing)
            # We return a simple error object or just skip this format
            print(f"Skipping format {fmt} due to error: {e}")
            outputs[fmt] = {"error": str(e)}

    return outputs