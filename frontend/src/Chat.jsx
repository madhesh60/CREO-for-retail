import { useState } from "react";
import { extractSpec, generateImages } from "./api";

export default function Chat() {
  const [form, setForm] = useState({
    main_message: "",
    sub_message: "",
    cta_text: "",
    style: "clean"
  });

  const [product, setProduct] = useState(null);
  const [logo, setLogo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [images, setImages] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const generate = async () => {
    if (!product || !logo) {
      alert("Upload product and logo");
      return;
    }

    setLoading(true);
    setImages(null);

    try {
      // -------- STEP 1: EXTRACT --------
      const extractData = new FormData();
      Object.entries(form).forEach(([k, v]) =>
        extractData.append(k, v)
      );

      const spec = await extractSpec(extractData);

      // -------- STEP 2: GENERATE --------
      const outputs = await generateImages(spec, product, logo);
      setImages(outputs);

    } catch (e) {
      console.error(e);
      alert("Error: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.app}>
      <h1 style={styles.title}>Retail Creative Builder</h1>

      <div style={styles.panel}>
        <input
          name="main_message"
          placeholder="Main Message"
          value={form.main_message}
          onChange={handleChange}
          style={styles.input}
        />

        <input
          name="sub_message"
          placeholder="Sub Message"
          value={form.sub_message}
          onChange={handleChange}
          style={styles.input}
        />

        <input
          name="cta_text"
          placeholder="CTA (Badge Text)"
          value={form.cta_text}
          onChange={handleChange}
          style={styles.input}
        />

        <input
          name="style"
          placeholder="Style (clean / bold)"
          value={form.style}
          onChange={handleChange}
          style={styles.input}
        />

        <label style={styles.label}>Product Image</label>
        <input type="file" onChange={(e) => setProduct(e.target.files[0])} />

        <label style={styles.label}>Logo Image</label>
        <input type="file" onChange={(e) => setLogo(e.target.files[0])} />

        <button style={styles.button} onClick={generate}>
          {loading ? "Generating..." : "Generate Creatives"}
        </button>
      </div>

      {images && (
        <div style={styles.gallery}>
          {Object.entries(images).map(([fmt, img]) => (
            <div key={fmt} style={styles.card}>
              <h3>{fmt}</h3>
              <img
                src={`data:image/png;base64,${img}`}
                style={styles.image}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  app: {
    background: "#0b0b0c",
    color: "#fff",
    minHeight: "100vh",
    padding: 32,
    fontFamily: "Inter, system-ui",
  },
  title: {
    marginBottom: 24,
  },
  panel: {
    background: "#151518",
    padding: 24,
    borderRadius: 12,
    maxWidth: 520,
  },
  input: {
    width: "100%",
    padding: 10,
    marginBottom: 12,
    background: "#0f0f12",
    color: "#fff",
    border: "1px solid #333",
    borderRadius: 6,
  },
  label: {
    marginTop: 12,
    display: "block",
    fontSize: 13,
    color: "#aaa",
  },
  button: {
    marginTop: 16,
    width: "100%",
    padding: 12,
    background: "#3b82f6",
    border: "none",
    color: "#fff",
    fontWeight: 600,
    borderRadius: 8,
    cursor: "pointer",
  },
  gallery: {
    marginTop: 40,
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
    gap: 24,
  },
  card: {
    background: "#151518",
    padding: 16,
    borderRadius: 12,
  },
  image: {
    width: "100%",
    borderRadius: 8,
    marginTop: 12,
  },
};
