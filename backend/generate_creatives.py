from formats import FORMATS
from background_generator import generate_background
from composer import compose_creative
from exporter import export_image

def generate_all(spec, product, logo):
    outputs = {}

    for fmt, (W, H) in FORMATS.items():
        bg = generate_background("clean", W, H, custom_color=spec.get("background_color"))
        img = compose_creative(bg, product, logo, spec, fmt)
        outputs[fmt] = export_image(img)

    return outputs
