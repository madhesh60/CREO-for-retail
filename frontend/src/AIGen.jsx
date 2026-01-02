import { useState } from 'react';
import { generateAiImage } from './api.js';
import styles from './styles.js';

export default function AIgen() {
  const [headline, setHeadline] = useState('');
  const [productName, setProductName] = useState('');
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!headline) return;
    setLoading(true);
    setError('');
    setImageUrl(null);

    try {
      // Construct prompt exactly like the AD-generator reference
      const fullPrompt = `${headline}. Product: ${productName}. High quality commercial product photography. Award-winning product shot.`;
      const url = await generateAiImage(fullPrompt);
      setImageUrl(url);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.panel}>
      <h1 style={styles.heroTitle}>AI Concept Generator</h1>
      <p style={{ color: '#666', marginBottom: '20px' }}>
        Generate commercial product concepts. Enter a headline and product name below.
      </p>

      <div style={{ maxWidth: '600px', margin: '0 auto' }}>
        <div style={{ marginBottom: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>

          <div>
            <label style={styles.label}>Headline / Ad Copy</label>
            <input
              type="text"
              placeholder="e.g. Experience the freshness of nature"
              value={headline}
              onChange={(e) => setHeadline(e.target.value)}
              style={{ ...styles.input, width: '100%' }}
            />
          </div>

          <div>
            <label style={styles.label}>Product Name</label>
            <input
              type="text"
              placeholder="e.g. Luxury Shampoo Bottle"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              style={{ ...styles.input, width: '100%' }}
            />
          </div>

          <button
            onClick={handleGenerate}
            style={{ ...styles.button, justifyContent: 'center' }}
            disabled={loading}
          >
            {loading ? 'Generating Concept...' : 'Generate AI Image'}
          </button>
        </div>

        {error && (
          <div style={{ padding: '12px', backgroundColor: '#ffeef0', color: '#b31d28', borderRadius: '6px', marginBottom: '20px' }}>
            Error: {error}
          </div>
        )}

        {imageUrl && (
          <div style={{ borderRadius: '12px', overflow: 'hidden', border: '1px solid #eee', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
            <img src={imageUrl} alt="Generated Concept" style={{ width: '100%', display: 'block' }} />
            <div style={{ padding: '12px', background: '#f9fafb', fontSize: '13px', color: '#666', borderTop: '1px solid #eee' }}>
              Use for reference and AI generated ads
            </div>
          </div>
        )}
      </div>
    </div>
  );
}