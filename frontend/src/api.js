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

export async function generateImages(spec, productFiles, logoFile, token) {
  const formData = new FormData();
  formData.append("spec", JSON.stringify(spec));

  // Handle single file (legacy) or array of files
  const products = Array.isArray(productFiles) ? productFiles : [productFiles];

  if (products[0]) formData.append("product_image", products[0]);
  if (products[1]) formData.append("product_image_2", products[1]);
  if (products[2]) formData.append("product_image_3", products[2]);

  formData.append("logo_image", logoFile);

  const headers = {};
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}/generate-images`, {
    method: "POST",
    headers: headers,
    body: formData
  });

  if (!res.ok) {
    throw new Error("Image generation failed");
  }

  return await res.json();
}

export async function generateAiImage(prompt) {
  const formData = new FormData();
  formData.append("prompt", prompt);

  const res = await fetch(`${API_BASE}/ai-generate`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Unknown Error" }));
    throw new Error(err.detail || "AI Generation failed");
  }

  // It returns binary image blob
  const blob = await res.blob();
  return URL.createObjectURL(blob);
}
