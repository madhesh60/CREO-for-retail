from PIL import Image
try:
    from rembg import remove
    HAS_REMBG = True
except ImportError:
    HAS_REMBG = False

def remove_bg_simple(img: Image.Image, bg_color=(255, 255, 255), tol=20):
    img = img.convert("RGBA")
    datas = img.getdata()

    new_data = []
    for r, g, b, a in datas:
        if (
            abs(r - bg_color[0]) < tol and
            abs(g - bg_color[1]) < tol and
            abs(b - bg_color[2]) < tol
        ):
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))

    img.putdata(new_data)
    return img

def remove_bg(img: Image.Image) -> Image.Image:
    if HAS_REMBG:
        try:
            return remove(img)
        except Exception as e:
            print(f"rembg failed: {e}, falling back to simple removal")
            return remove_bg_simple(img)
    else:
        return remove_bg_simple(img)
