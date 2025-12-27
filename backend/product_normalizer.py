from PIL import Image

def normalize_product(product, W, H):
    scale = 0.45 if H < 1500 else 0.55
    new_w = int(W * scale)
    new_h = int(product.height * new_w / product.width)
    product = product.resize((new_w, new_h), Image.Resampling.LANCZOS)

    x = (W - new_w) // 2
    y = int(H * 0.25)

    return product, (x, y)
