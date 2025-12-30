//Docs.jsx

import styles from "./styles.js";

const docStyles = {
  ...styles,
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '40px 20px',
    display: 'grid',
    gridTemplateColumns: '250px 1fr',
    gap: '40px',
    fontFamily: '"Inter", sans-serif',
    color: '#333',
  },
  sidebar: {
    position: 'sticky',
    top: '20px',
    height: 'fit-content',
    borderRight: '1px solid #eee',
    paddingRight: '20px',
  },
  sidebarLink: {
    display: 'block',
    padding: '8px 0',
    color: '#666',
    textDecoration: 'none',
    fontSize: '14px',
    cursor: 'pointer',
    transition: 'color 0.2s',
  },
  sidebarLinkActive: {
    color: '#0070f3',
    fontWeight: 'bold',
  },
  content: {
    lineHeight: '1.6',
  },
  section: {
    marginBottom: '60px',
    scrollMarginTop: '20px',
  },
  h1: {
    fontSize: '36px',
    fontWeight: '800',
    marginBottom: '10px',
    color: '#111',
  },
  h2: {
    fontSize: '24px',
    fontWeight: '700',
    marginBottom: '20px',
    marginTop: '40px',
    paddingBottom: '10px',
    borderBottom: '1px solid #eaeaea',
    color: '#222',
  },
  h3: {
    fontSize: '18px',
    fontWeight: '600',
    marginBottom: '15px',
    marginTop: '30px',
    color: '#333',
  },
  p: {
    marginBottom: '16px',
    fontSize: '16px',
    color: '#444',
  },
  codeBlock: {
    backgroundColor: '#f6f8fa',
    padding: '16px',
    borderRadius: '6px',
    fontFamily: '"Fira Code", monospace',
    fontSize: '14px',
    overflowX: 'auto',
    marginBottom: '20px',
    border: '1px solid #e1e4e8',
  },
  alert: {
    padding: '16px',
    borderRadius: '6px',
    marginBottom: '20px',
    fontSize: '15px',
  },
  alertWarning: {
    backgroundColor: '#fff8c5',
    border: '1px solid #f1e05a',
    color: '#735c0f',
  },
  alertError: {
    backgroundColor: '#ffeef0',
    border: '1px solid #ffdce0',
    color: '#b31d28',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginBottom: '20px',
  },
  th: {
    textAlign: 'left',
    padding: '12px',
    borderBottom: '2px solid #eaeaea',
    fontWeight: '600',
    fontSize: '14px',
  },
  td: {
    padding: '12px',
    borderBottom: '1px solid #eaeaea',
    fontSize: '14px',
  },
};

export default function Docs() {
  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div style={docStyles.container}>
      {/* Sidebar Navigation */}
      <nav style={docStyles.sidebar}>
        <div style={{ marginBottom: '20px', fontWeight: 'bold', textTransform: 'uppercase', fontSize: '12px', letterSpacing: '1px', color: '#999' }}>Contents</div>
        <a style={docStyles.sidebarLink} onClick={() => scrollTo('intro')}>Introduction</a>
        <a style={docStyles.sidebarLink} onClick={() => scrollTo('features')}>Core Features</a>
        <a style={docStyles.sidebarLink} onClick={() => scrollTo('compliance')}>Compliance Engine</a>
        <a style={docStyles.sidebarLink} onClick={() => scrollTo('workflow')}>Usage Workflow</a>
        <a style={docStyles.sidebarLink} onClick={() => scrollTo('api')}>API Reference</a>
        <a style={docStyles.sidebarLink} onClick={() => scrollTo('deploy')}>Deployment (Docker)</a>
      </nav>

      {/* Main Content */}
      <div style={docStyles.content}>
        
        {/* Introduction */}
        <div id="intro" style={docStyles.section}>
          <h1 style={docStyles.h1}>AI Retail Creative Studio</h1>
          <p style={{ fontSize: '20px', color: '#666', marginBottom: '30px' }}>
            Enterprise-grade generative design system for localized retail assets.
          </p>
          <p style={docStyles.p}>
            The AI Retail Creative Studio is a Strict Compliance Generation engine designed to produce retail marketing assets that inherently adhere to complex brand guidelines. It eliminates the "human error" factor by encoding rules for copy, layout, and legal requirements directly into the generation pipeline.
          </p>
        </div>

        {/* Features */}
        <div id="features" style={docStyles.section}>
          <h2 style={docStyles.h2}>Core Features</h2>
          
          <h3 style={docStyles.h3}>Strict Compliance Enforcement</h3>
          <p style={docStyles.p}>
            The engine operates on a "Zero Tolerance" policy. Any generation request that violates structural, legal, or brand rules is rejected pre-generation or requires explicit high-level override.
          </p>
          
          <h3 style={docStyles.h3}>Dynamic Template Engine</h3>
          <ul style={{ paddingLeft: '20px', marginBottom: '20px', lineHeight: '1.8' }}>
            <li><strong>LEP Mode:</strong> Low Everyday Price templates with mandated white backgrounds, left-aligned blue text, and no promotional fluff.</li>
            <li><strong>Social Safe Zones:</strong> Hard-coded exclusions for UI elements in Instagram Stories (Top 200px / Bottom 250px protection).</li>
            <li><strong>Value Tiles:</strong> Immutable components for visual consistency (New, Clubcard, White Value).</li>
          </ul>

          <h3 style={docStyles.h3}>Safety & Logic Gates</h3>
          <div style={{ ...docStyles.alert, ...docStyles.alertWarning }}>
            <strong>People Detection:</strong> Integration with OpenCV to detect human faces in product imagery. Triggers a mandatory "Confirmation Required" workflow to ensure compliance with talent usage rights.
          </div>
          <div style={{ ...docStyles.alert, ...docStyles.alertError }}>
            <strong>Alcohol & Age Gating:</strong> Semantic detection of alcohol keywords forces the injection of high-contrast Drinkaware lock-ups.
          </div>
        </div>

        {/* Compliance */}
        <div id="compliance" style={docStyles.section}>
          <h2 style={docStyles.h2}>Compliance Rulebook</h2>
          <p style={docStyles.p}>
            The system enforces rules derived from Appendix A & B of the Retail Guidelines.
          </p>

          <table style={docStyles.table}>
            <thead>
              <tr>
                <th style={docStyles.th}>Category</th>
                <th style={docStyles.th}>Rule / Constraint</th>
                <th style={docStyles.th}>Enforcement</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style={docStyles.td}><strong>Alcohol</strong></td>
                <td style={docStyles.td}>Mandatory Drinkaware lock-up (Black/White), Min Height 20px.</td>
                <td style={docStyles.td}>Auto-Injection / Hard Fail if space insufficient</td>
              </tr>
              <tr>
                <td style={docStyles.td}><strong>Forbidden Copy</strong></td>
                <td style={docStyles.td}>No claims ("Best"), Money-back, Competitions, Sustainability.</td>
                <td style={docStyles.td}>Hard Fail (E002)</td>
              </tr>
              <tr>
                <td style={docStyles.td}><strong>Accessibility</strong></td>
                <td style={docStyles.td}>Min Font Size 20px (Brand). WCAG AA Contrast.</td>
                <td style={docStyles.td}>Auto-Scaling / Hard Fail</td>
              </tr>
              <tr>
                <td style={docStyles.td}><strong>Layout</strong></td>
                <td style={docStyles.td}>Packshot must be closest element to CTA. No Safe Zone violation.</td>
                <td style={docStyles.td}>Geometric Solver</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Workflow */}
        <div id="workflow" style={docStyles.section}>
          <h2 style={docStyles.h2}>Usage Workflow</h2>
          
          <h3 style={docStyles.h3}>1. Asset Ingestion</h3>
          <p style={docStyles.p}>
            User uploads a Product Image (raw packshot) and a Logo. The background remover automatically cleans the product image.
          </p>

          <h3 style={docStyles.h3}>2. Specification</h3>
          <p style={docStyles.p}>
            User defines the campaign parameters: Headline, Subhead, CTA, Style, and Template Mode.
          </p>

          <h3 style={docStyles.h3}>3. Validation (The Gate)</h3>
          <p style={docStyles.p}>
            Before any pixels are drawn, the request passes through the <code>validator.py</code> engine. 
            <ul>
              <li>Check structural integrity.</li>
              <li>Scan for forbidden keywords.</li>
              <li>Verify visual constraints (e.g. White BG for LEP).</li>
              <li>Scan image for People (OpenCV).</li>
            </ul>
          </p>

          <h3 style={docStyles.h3}>4. Generation</h3>
          <p style={docStyles.p}>
            If validated, the <code>composer.py</code> engine calculates the optimal layout for every requested format (Square, Portrait, Landscape), obeying all safe zones and collision rules.
          </p>
        </div>

        {/* Deployment */}
        {/* Deployment */}
        <div id="deploy" style={docStyles.section}>
          <h2 style={docStyles.h2}>Deployment (Docker)</h2>
          <p style={docStyles.p}>
            The application is containerized for consistent deployment across environments.
          </p>

          <h3 style={docStyles.h3}>Prerequisites</h3>
          <p style={docStyles.p}>Docker Desktop and Docker Compose.</p>

          <h3 style={docStyles.h3}>Running the Stack</h3>
          <div style={docStyles.codeBlock}>
            {`# Build and Run
docker-compose up --build

# Backend will act on localhost:8000
# Frontend will act on localhost:3000`}
          </div>

          <h3 style={docStyles.h3}>Backend Container</h3>
          <p style={docStyles.p}>
             Python 3.10-slim based. Installs OpenCV dependencies (libgl1) and Python requirements.
          </p>

          <h3 style={docStyles.h3}>Frontend Container</h3>
          <p style={docStyles.p}>
             Node 18-alpine based. Builds the Vite React app and serves it (dev mode for this demo).
          </p>
        </div>

      </div>
    </div>
  );
}