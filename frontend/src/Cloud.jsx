import { useEffect, useState } from "react";
import { useAuth } from "./AuthContext";
import styles from "./styles.js";

export default function Cloud() {
  const { token, user } = useAuth();
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (token) {
      fetchImages();
    }
  }, [token]);

  const fetchImages = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/cloud-images", {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setImages(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <div style={styles.page}>
        <h1 style={styles.pageTitle}>Cloud Gallery</h1>
        <p style={styles.pageContent}>Please <a href="#" onClick={(e) => { e.preventDefault(); window.location.reload(); /* Dirty hack but user will likely use nav */ }}>sign in</a> to view your Cloud Gallery.</p>
      </div>
    )
  }

  return (
    <div style={styles.page}>
      <h1 style={styles.pageTitle}>Cloud Gallery</h1>
      <p style={styles.pageContent}>Your generated designs based on your saved colors.</p>

      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
          <div className="spinner"></div>
        </div>
      ) : (
        <div style={styles.gallery}>
          {images.map((img) => (
            <div key={img._id} style={styles.card}>
              <h3 style={styles.cardTitle}>{img.format} <span style={{ fontSize: '0.8em', color: img.color }}>{img.color}</span></h3>
              <img src={img.url} style={styles.image} alt="Generated Creative" />
            </div>
          ))}
          {images.length === 0 && <p>No images found. Save some colors and generate new images!</p>}
        </div>
      )}
    </div>
  );
}