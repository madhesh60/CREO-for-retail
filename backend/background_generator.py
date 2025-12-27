from PIL import Image

def generate_background(style, w, h):
    if style == "blue":
        color = (180, 215, 235)
    elif style == "pink":
        color = (255, 220, 230)
    else:
        # Default premium light blue from reference
        color = (168, 218, 239)

    return Image.new("RGB", (w, h), color)
