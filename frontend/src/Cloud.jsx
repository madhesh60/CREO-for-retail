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
        <p style={{ ...styles.pageContent, textAlign: 'center' }}>Please sign in to view your Cloud Gallery.</p>
      </div>
    )
  }

  // Group images by batch_id
  const batchedImages = images.reduce((acc, img) => {
    // Fallback if batch_id not present (legacy images)
    const batchId = img.batch_id || 'legacy';
    if (!acc[batchId]) {
      acc[batchId] = {
        color: img.color,
        timestamp: img.created_at || 'Older',
        items: []
      };
    }
    acc[batchId].items.push(img);
    return acc;
  }, {});

  // Sort batches by creation? (Assuming backend sort, or reverse keys)
  const sortedBatches = Object.entries(batchedImages).reverse();

  return (
    <div style={styles.page}>
      <h1 style={styles.pageTitle}>Cloud Gallery</h1>
      <p style={styles.pageContent}>Your generated campaigns, organized by session.</p>

      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
          <div className="spinner"></div>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '40px' }}>
          {sortedBatches.map(([batchId, group]) => (
            <div key={batchId} style={{
              border: '1px solid #eaeaea',
              borderRadius: '12px',
              padding: '24px',
              background: '#fafafa'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '20px', gap: '12px' }}>
                <div style={{
                  width: '32px', height: '32px',
                  borderRadius: '50%',
                  backgroundColor: group.color,
                  border: '2px solid #fff',
                  boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
                }}></div>
                <h2 style={{ fontSize: '1.2rem', margin: 0, color: '#333' }}>
                  Campaign Set <span style={{ fontWeight: 'normal', color: '#777', fontSize: '0.9rem' }}>({group.color})</span>
                </h2>
              </div>

              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '20px',
                alignItems: 'start'
              }}>
                {group.items.map((img) => {
                  // Handle legacy format (img.url) vs new format (img.urls)
                  // img.urls = { png: "...", jpg: "..." }
                  const displayUrl = img.urls ? (img.urls.png || img.urls.jpg) : img.url;

                  return (
                    <div key={img._id} style={{ ...styles.card, margin: 0 }}>
                      <h3 style={styles.cardTitle}>{img.format}</h3>
                      <img src={displayUrl} style={{ ...styles.image, height: 'auto', maxHeight: '300px', objectFit: 'contain' }} alt="Generated Creative" />

                      <div style={{ display: 'flex', gap: '8px', justifyContent: 'center', marginTop: '10px' }}>
                        {img.urls && img.urls.png ? (
                          <a href={img.urls.png} download target="_blank" style={{ color: '#0070f3', fontSize: '12px', textDecoration: 'none', border: '1px solid #ccc', padding: '2px 6px', borderRadius: '4px' }}>PNG</a>
                        ) : (
                          <a href={displayUrl} download target="_blank" style={{ color: '#0070f3', fontSize: '12px', textDecoration: 'none', border: '1px solid #ccc', padding: '2px 6px', borderRadius: '4px' }}>PNG</a>
                        )}

                        {img.urls && img.urls.jpg && (
                          <a href={img.urls.jpg} download target="_blank" style={{ color: '#0070f3', fontSize: '12px', textDecoration: 'none', border: '1px solid #ccc', padding: '2px 6px', borderRadius: '4px' }}>JPG</a>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          ))}
          {images.length === 0 && <p style={{ textAlign: 'center', color: '#666' }}>No campaigns found. Start creating!</p>}
        </div>
      )}
    </div>
  );
}
