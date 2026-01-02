import os
import json
from io import BytesIO
from PIL import Image
from huggingface_hub import InferenceClient

# Your existing load_ad_env() function (unchanged)
def load_ad_env():
    if os.environ.get("HUGGINGFACE_API_TOKEN"):
        return

    try:
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'AD-generator', '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('HUGGINGFACE_API_TOKEN='):
                        val = line.split('=', 1)[1]
                        val = val.strip('"').strip("'")
                        os.environ['HUGGINGFACE_API_TOKEN'] = val
                        print("Loaded HF Token from AD-generator/.env")
                        break
    except Exception as e:
        print(f"Could not load AD-generator extension env: {e}")

load_ad_env()

def generate_ad_image(prompt):
    token = os.environ.get("HUGGINGFACE_API_TOKEN")
    if not token:
        raise Exception("Missing HUGGINGFACE_API_TOKEN. Please set it in backend environment or AD-generator/.env")

    client = InferenceClient(token=token)

    try:
        # Generate image (returns PIL Image)
        image = client.text_to_image(
            prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0",
            # Optional: Add negative_prompt="blurry, low quality" for better results
        )

        # Convert to bytes (matching your original return type)
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        return img_byte_arr.getvalue()

    except Exception as e:
        raise Exception(f"HF Inference Error: {str(e)}")