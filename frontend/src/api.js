const API_BASE = "http://127.0.0.1:8000";

export async function extractSpec(formData) {
  const res = await fetch(`${API_BASE}/extract`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Extraction failed");
  }

  return await res.json();
}

export async function generateImages(spec, productFile, logoFile) {
  const formData = new FormData();
  formData.append("spec", JSON.stringify(spec));
  formData.append("product_image", productFile);
  formData.append("logo_image", logoFile);

  const res = await fetch(`${API_BASE}/generate-images`, {
    method: "POST",
    body: formData
  });

  if (!res.ok) {
    throw new Error("Image generation failed");
  }

  return await res.json();
}
