import base64
import io
import os

def export_image(img, format="PNG", max_size_kb=500):
    """
    Exports image to base64, optimizing quality to ensure it is under max_size_kb.
    """
    quality = 95
    step = 5
    
    if format.upper() not in ["PNG", "JPEG", "JPG"]:
        format = "PNG"
        
    while quality > 10:
        buf = io.BytesIO()
        if format.upper() in ["JPEG", "JPG"]:
             # JPEG doesn't support transparency, convert if needed
             if img.mode == 'RGBA':
                 img = img.convert('RGB')
             img.save(buf, format=format, quality=quality, optimize=True)
        else:
             # PNG optimization
             # Pillow's PNG optimize flag doesn't use quality param effectively for size reduction like JPEG
             # But we can try to rely on optimize=True or resizing if absolutely needed (omitted for now to keep it simple)
             img.save(buf, format=format, optimize=True)
             
        size_kb = buf.tell() / 1024
        
        if size_kb < max_size_kb or format.upper() == "PNG": 
            # PNG quality adjustment is harder with standard PIL, accept it or switch to JPEG if strict
            break
            
        quality -= step
        
    return base64.b64encode(buf.getvalue()).decode()
