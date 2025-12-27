from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io, json

from generate_creatives import generate_all

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- EXTRACT ----------------
@app.post("/extract")
async def extract(
    main_message: str = Form(...),
    sub_message: str = Form(...),
    cta_text: str = Form(...),
    style: str = Form("clean"),
    background_color: str = Form(None),
    badge_color: str = Form(None),
    badge_shape: str = Form(None),
):
    """
    Normalize all user input into ONE spec.
    This prevents KeyError, 422, and mismatch bugs.
    """

    spec = {
        "main_message": main_message.strip(),
        "sub_message": sub_message.strip(),
        "cta_text": cta_text.strip(),
        "style": style.strip() or "clean",
        "background_color": background_color.strip() if background_color else None,
        "badge_color": badge_color.strip() if badge_color else None,
        "badge_shape": badge_shape.strip() if badge_shape else None,
    }

    return spec


# ---------------- GENERATE IMAGES ----------------
@app.post("/generate-images")
async def generate_images(
    spec: str = Form(...),
    product_image: UploadFile = Form(...),
    logo_image: UploadFile = Form(...)
):
    """
    Uses ONLY the spec JSON + images
    """

    spec = json.loads(spec)

    product = Image.open(
        io.BytesIO(await product_image.read())
    ).convert("RGBA")

    logo = Image.open(
        io.BytesIO(await logo_image.read())
    ).convert("RGBA")

    outputs = generate_all(
        spec=spec,
        product=product,
        logo=logo,
    )

    return outputs
