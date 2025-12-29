from formats import FORMATS
from background_generator import generate_background
from composer import compose_creative
from exporter import export_image
from validator import validate_text_content

def generate_all(spec, product, logo):
    outputs = {}
    
    # 1. Validation
    validation = validate_text_content(
        spec.get("main_message", ""),
        spec.get("sub_message", ""),
        spec.get("cta_text", "")
    )
    
    outputs["validation"] = validation

    outputs["validation"] = validation

    # Block generation on hard failure
    if not validation["valid"]:
        return outputs
    
    for fmt, (W, H) in FORMATS.items():
        bg = generate_background("clean", W, H, custom_color=spec.get("background_color"))
        img = compose_creative(bg, product, logo, spec, fmt)
        
        # Requirement: Enable download in final Jpeg and Png.
        # We generate both
        png_b64 = export_image(img, format="PNG")
        jpg_b64 = export_image(img, format="JPEG", max_size_kb=500)
        
        outputs[fmt] = {
            "png": png_b64,
            "jpg": jpg_b64
        }

    return outputs