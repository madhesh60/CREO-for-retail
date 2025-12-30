// Chat.jsx
import { useState } from "react";
import { extractSpec, generateImages } from "./api";
import { useAuth } from "./AuthContext";
import styles from "./styles.js";

export default function Chat() {
  const { token, addColor, user } = useAuth();
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
      const outputs = await generateImages(spec, product, logo, token);
      setImages(outputs);

    } catch (e) {
      console.error(e);
      alert("Error: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div style={styles.hero}>
        <div style={styles.heroContent}>
          <div style={styles.illustration}>
            {/* Improved SVG illustration matching the reference: line art llama with VR headset, waving */}
            <svg viewBox="0 0 200 250" style={styles.illustrationSvg} xmlns="http://www.w3.org/2000/svg">
              {/* Body */}
              <ellipse cx="100" cy="140" rx="60" ry="70" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              {/* Head */}
              <circle cx="100" cy="70" r="40" fill="none" stroke="currentColor" strokeWidth="2" />
              {/* Ears */}
              <path d="M70 50 Q60 30 80 40" fill="none" stroke="currentColor" strokeWidth="2" />
              <path d="M130 50 Q140 30 120 40" fill="none" stroke="currentColor" strokeWidth="2" />
              {/* Eyes */}
              <circle cx="85" cy="65" r="4" fill="none" stroke="currentColor" strokeWidth="1" />
              <circle cx="115" cy="65" r="4" fill="none" stroke="currentColor" strokeWidth="1" />
              {/* Mouth/Smile */}
              <path d="M90 85 Q100 95 110 85" fill="none" stroke="currentColor" strokeWidth="2" />
              {/* Neck */}
              <path d="M100 110 L100 120" stroke="currentColor" strokeWidth="3" />
              {/* Legs */}
              <line x1="70" y1="190" x2="70" y2="220" stroke="currentColor" strokeWidth="3" />
              <line x1="130" y1="190" x2="130" y2="220" stroke="currentColor" strokeWidth="3" />
              <line x1="50" y1="190" x2="50" y2="220" stroke="currentColor" strokeWidth="3" />
              <line x1="150" y1="190" x2="150" y2="220" stroke="currentColor" strokeWidth="3" />
              {/* Tail */}
              <path d="M40 140 Q20 160 40 180" fill="none" stroke="currentColor" strokeWidth="2" />
              {/* Headset */}
              <ellipse cx="100" cy="50" rx="50" ry="8" fill="none" stroke="currentColor" strokeWidth="2" />
              <circle cx="60" cy="50" r="6" fill="none" stroke="currentColor" strokeWidth="1" />
              <circle cx="140" cy="50" r="6" fill="none" stroke="currentColor" strokeWidth="1" />
              {/* VR Glasses */}
              <rect x="80" y="60" width="40" height="12" rx="6" fill="none" stroke="currentColor" strokeWidth="2" />
              <line x1="80" y1="66" x2="120" y2="66" stroke="currentColor" strokeWidth="1" />
              {/* Mic */}
              <path d="M140 70 Q150 80 140 90" fill="none" stroke="currentColor" strokeWidth="1" />
              {/* Waving Arm */}
              <path d="M160 120 Q180 140 160 160" fill="none" stroke="currentColor" strokeWidth="3" />
              <circle cx="160" cy="140" r="3" fill="none" stroke="currentColor" strokeWidth="1" />
              {/* Cloud base */}
              <path d="M20 230 Q50 210 80 230 Q110 210 140 230 Q170 210 200 230" fill="none" stroke="currentColor" strokeWidth="2" />
            </svg>
          </div>
          <div style={styles.heroText}>
            <h1 style={styles.heroTitle}>AI Retail Creative<br />Studio</h1>
          </div>
        </div>

        <div style={styles.panel}>
          <div style={styles.formGrid}>
            <div style={styles.sectionTitle}>Content</div>

            <div style={styles.fullWidth}>
              <label style={styles.label}>Main Message</label>
              <input
                name="main_message"
                placeholder="e.g. Summer Sale"
                value={form.main_message}
                onChange={handleChange}
                style={styles.input}
              />
            </div>

            <div style={styles.fullWidth}>
              <label style={styles.label}>Sub Message</label>
              <input
                name="sub_message"
                placeholder="e.g. Up to 50% Off"
                value={form.sub_message}
                onChange={handleChange}
                style={styles.input}
              />
            </div>

            <div>
              <label style={styles.label}>CTA Text</label>
              <input
                name="cta_text"
                placeholder="e.g. Shop Now"
                value={form.cta_text}
                onChange={handleChange}
                style={styles.input}
              />
            </div>

            <div>
              <label style={styles.label}>Style</label>
              <input
                name="style"
                placeholder="clean / bold"
                value={form.style}
                onChange={handleChange}
                style={styles.input}
              />
            </div>

            <div style={styles.sectionTitle}>Customization</div>

            <div>
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
                {user && (
                  <button
                    onClick={() => addColor(form.background_color)}
                    title="Save to my colors"
                    style={{
                      border: 'none',
                      background: 'none',
                      cursor: 'pointer',
                      fontSize: '18px',
                      padding: '0 4px',
                      opacity: 0.6
                    }}
                  >
                    💾
                  </button>
                )}
              </div>
            </div>

            <div>
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

            <div style={styles.fullWidth}>
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
            </div>

            <div style={styles.sectionTitle}>Assets</div>

            <div>
              <label style={styles.label}>Product Image</label>
              <input type="file" onChange={(e) => setProduct(e.target.files[0])} style={styles.fileInput} />
            </div>

            <div>
              <label style={styles.label}>Logo Image</label>
              <input type="file" onChange={(e) => setLogo(e.target.files[0])} style={styles.fileInput} />
            </div>

            <div style={styles.fullWidth}>
              <button style={styles.button} onClick={generate}>
                {loading ? <div className="spinner" style={{ width: '20px', height: '20px', borderTopColor: '#fff' }}></div> : "Generate Create"}
              </button>
            </div>
          </div>
        </div>

        {images && (
          <div style={styles.gallery}>

            {/* Validation Feedback */}
            {images.validation && !images.validation.valid && (
              <div style={{ ...styles.fullWidth, padding: '16px', backgroundColor: '#fff0f0', border: '1px solid #ffcccc', borderRadius: '8px', marginBottom: '20px' }}>
                <h4 style={{ color: '#cc0000', margin: '0 0 8px 0' }}>Compliance Issues Detected:</h4>
                <ul style={{ margin: 0, paddingLeft: '20px', color: '#cc0000' }}>
                  {images.validation.errors.map((err, i) => (
                    <li key={i}>{err}</li>
                  ))}
                </ul>

                {/* People Confirmation Button */}
                {images.validation.requires_confirmation && (
                  <div style={{ marginTop: '16px', borderTop: '1px solid #ffcccc', paddingTop: '12px' }}>
                    <p style={{ color: '#cc0000', fontSize: '14px', marginBottom: '8px' }}>
                      User confirmation required: detected people in image. By proceeding, you confirm this person logic is integral to the campaign.
                    </p>
                    <button
                      style={{
                        backgroundColor: '#cc0000', color: 'white', border: 'none', padding: '8px 16px',
                        borderRadius: '4px', cursor: 'pointer', fontSize: '14px', fontWeight: 'bold'
                      }}
                      onClick={() => {
                        // Retry with confirmation flag
                        setForm(prev => ({ ...prev, confirm_people: true }));
                        // We need to trigger generation again. 
                        // Since setForm is async, we can't just call generate() broadly.
                        // But for this simple implementation, let's create a specific retry function or just rely on user clicking Generate again?
                        // Better: A specific "Confirm & Generate" button.
                        // Actually, let's modify the handler to call generate with override.
                      }}
                    >
                      Confirm & Retry Generation
                    </button>
                    <small style={{ display: 'block', marginTop: '4px', color: '#888' }}>
                      (Click this, then click "Generate Create" again to proceed)
                    </small>
                  </div>
                )}
              </div>
            )}

            {Object.entries(images)
              .filter(([k]) => k !== 'validation')
              .map(([fmt, data]) => {
                const imgSrc = typeof data === 'string' ? data : (data ? (data.png || data.jpg) : null);
                if (!imgSrc) return null;

                return (
                  <div key={fmt} style={styles.card}>
                    <h3 style={styles.cardTitle}>{fmt}</h3>
                    <img
                      src={`data:image/png;base64,${imgSrc}`}
                      style={styles.image}
                      alt={fmt}
                    />
                    <div style={{ display: 'flex', gap: '8px', justifyContent: 'center', marginTop: '10px' }}>
                      {typeof data === 'object' && data.png && (
                        <a
                          href={`data:image/png;base64,${data.png}`}
                          download={`creative_${fmt}.png`}
                          style={{ color: '#0070f3', fontSize: '13px', textDecoration: 'none', border: '1px solid #eee', padding: '4px 8px', borderRadius: '4px' }}
                        >
                          PNG
                        </a>
                      )}
                      {typeof data === 'object' && data.jpg && (
                        <a
                          href={`data:image/jpeg;base64,${data.jpg}`}
                          download={`creative_${fmt}.jpg`}
                          style={{ color: '#0070f3', fontSize: '13px', textDecoration: 'none', border: '1px solid #eee', padding: '4px 8px', borderRadius: '4px' }}
                        >
                          JPG
                        </a>
                      )}
                    </div>
                  </div>
                );
              })}
          </div>
        )}
      </div >
    </>
  );
}
