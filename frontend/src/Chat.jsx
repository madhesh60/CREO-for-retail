import { useState } from "react";
import { extractSpec, generateImages } from "./api";

export default function Chat() {
  const [form, setForm] = useState({
    main_message: "",
    sub_message: "",
    cta_text: "",
    style: "clean",
    background_color: "#a8ddef", // Default light blue
    badge_color: "#daa520", // Default gold
    badge_shape: ""
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
        <div style={styles.sectionTitle}>Content</div>
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

        <div style={styles.sectionTitle}>Customization</div>

        <div style={styles.row}>
          <div style={styles.col}>
            <label style={styles.label}>Background Color</label>
            <div style={styles.colorWrapper}>
              <input
                type="color"
                name="background_color"
                value={form.background_color}
                onChange={handleChange}
                style={styles.colorInput}
              />
              <span style={styles.colorValue}>{form.background_color}</span>
            </div>
          </div>

          <div style={styles.col}>
            <label style={styles.label}>Badge Color</label>
            <div style={styles.colorWrapper}>
              <input
                type="color"
                name="badge_color"
                value={form.badge_color}
                onChange={handleChange}
                style={styles.colorInput}
              />
              <span style={styles.colorValue}>{form.badge_color}</span>
            </div>
          </div>
        </div>

        <label style={styles.label}>Badge Shape</label>
        <select
          name="badge_shape"
          value={form.badge_shape}
          onChange={handleChange}
          style={styles.select}
        >
          <option value="">Random (Dynamic)</option>
          <option value="circle">Circle</option>
          <option value="square">Square</option>
          <option value="hexagon">Hexagon</option>
        </select>

        <div style={styles.sectionTitle}>Assets</div>
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
    border: "1px solid #222",
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: "bold",
    color: "#eee",
    marginBottom: 8,
    marginTop: 16,
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  input: {
    width: "100%",
    padding: 10,
    marginBottom: 12,
    background: "#0f0f12",
    color: "#fff",
    border: "1px solid #333",
    borderRadius: 6,
    fontSize: 14,
  },
  select: {
    width: "100%",
    padding: 10,
    marginBottom: 12,
    background: "#0f0f12",
    color: "#fff",
    border: "1px solid #333",
    borderRadius: 6,
    fontSize: 14,
    cursor: "pointer",
  },
  row: {
    display: "flex",
    gap: 16,
    marginBottom: 12,
  },
  col: {
    flex: 1,
  },
  colorWrapper: {
    display: "flex",
    alignItems: "center",
    gap: 8,
    background: "#0f0f12",
    padding: 8,
    borderRadius: 6,
    border: "1px solid #333",
  },
  colorInput: {
    border: "none",
    width: 30,
    height: 30,
    padding: 0,
    background: "transparent",
    cursor: "pointer",
  },
  colorValue: {
    fontSize: 13,
    color: "#aaa",
    fontFamily: "monospace",
  },
  label: {
    marginTop: 0,
    marginBottom: 6,
    display: "block",
    fontSize: 13,
    color: "#aaa",
  },
  button: {
    marginTop: 24,
    width: "100%",
    padding: 14,
    background: "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
    border: "none",
    color: "#fff",
    fontWeight: 600,
    borderRadius: 8,
    cursor: "pointer",
    fontSize: 16,
    transition: "transform 0.1s",
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
    border: "1px solid #222",
  },
  image: {
    width: "100%",
    borderRadius: 8,
    marginTop: 12,
  },
};
