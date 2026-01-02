import { useState } from "react";
import styles from "./styles.js";

const COMPLIANCE_RULES = [
  { id: "1", title: "Mandatory Elements", desc: "Every creative must include a Headline, Subhead, Logo, and Packshot. If any one is missing, the creative is structurally invalid." },
  { id: "2", title: "Headline & Subhead Rules", desc: "Headline and Subhead are required text slots. They must be neutral, factual, and cannot contain claims, prices, or offers." },
  { id: "3", title: "CTA (Call To Action)", desc: "CTA is not allowed by default. It can appear only when explicitly enabled for that format or template." },
  { id: "4", title: "Value Tiles (Core Concept)", desc: "Value tiles are pre-designed locked boxes used to show value or status. They are not normal text and cannot be freely edited or moved." },
  { id: "5", title: "Allowed Value Tile Types", desc: "Only three tile types are allowed: New, White Value Tile, Clubcard Value Tile. Any other tile type is invalid." },
  { id: "6", title: "Value Tile Immutability", desc: "Value tiles have fixed position, size, color, and style. No text, image, or CTA may overlap a tile." },
  { id: "7", title: "Tile Edit Permissions", desc: "New Tile → no editable text. White Value Tile → price only. Clubcard Tile → offer price + regular price only." },
  { id: "8", title: "Clubcard Definition", desc: "Clubcard is Tesco’s loyalty program. Clubcard pricing requires extra legal text and an end date." },
  { id: "9", title: "Clubcard Mandatory Disclaimer", desc: "Any Clubcard tile must include exact text: 'Available in selected stores. Clubcard/app required. Ends DD/MM'." },
  { id: "10", title: "Date Format Rule", desc: "All end dates must be in DD/MM format only. Missing or wrong format causes rejection." },
  { id: "11", title: "Tesco Tags", desc: "Tesco tags indicate availability or exclusivity. They are mandatory when linking to Tesco or using Pinterest format." },
  { id: "12", title: "Allowed Tesco Tag Text", desc: "Only these are allowed: 'Only at Tesco', 'Available at Tesco', 'Selected stores. While stocks last.'. Any variation is illegal." },
  { id: "13", title: "Logo Rules", desc: "A logo must appear on all creatives. It can be uploaded or selected from the brand library." },
  { id: "14", title: "Packshot Rules", desc: "Maximum 3 packshots allowed. One clear lead product must always be present." },
  { id: "15", title: "Packshot Priority", desc: "Packshot must be the closest visual element to the CTA (if CTA exists). This ensures correct visual hierarchy." },
  { id: "16", title: "Background Rules", desc: "Only one background is allowed. Either a flat color OR a single image — never multiple." },
  { id: "17", title: "Low Everyday Price (LEP) Template", desc: "LEP is a locked template mode, not a style choice. It enforces white background, Tesco blue text, left alignment, and LEP logo usage." },
  { id: "18", title: "LEP Restrictions", desc: "In LEP mode, no branded elements are allowed except the logo. Tag text is mandatory and layout is fully locked." },
  { id: "19", title: "Alcohol Category Detection", desc: "Alcohol must be detected before generation begins. This activates mandatory Drinkaware rules." },
  { id: "20", title: "Drinkaware Lock-up (Structural)", desc: "Alcohol creatives must reserve space for Drinkaware. This applies to all formats and sizes." },
  { id: "21", title: "Drinkaware Design Rules", desc: "Drinkaware must be black or white only, readable, and visible. Minimum size and contrast are mandatory." },
  { id: "22", title: "No Price Language", desc: "Text must not mention prices, discounts, savings, or percentages. Even implied pricing causes a hard fail." },
  { id: "23", title: "No Claims", desc: "Claims like 'best', 'No.1', 'proven', or comparisons are forbidden. Asterisks pointing to explanations are also not allowed." },
  { id: "24", title: "No Competitions or Giveaways", desc: "No 'win', 'enter', 'contest', or reward-based language. Tesco self-serve does not allow competitions." },
  { id: "25", title: "No Sustainability or Green Claims", desc: "No eco, green, carbon, ethical, or environmental claims. Even vague sustainability hints are rejected." },
  { id: "26", title: "No Charity or Partnerships", desc: "No charity mentions, donations, or partner logos. These are not allowed in retail creatives." },
  { id: "27", title: "No Money-Back Guarantees", desc: "No refunds, guarantees, or 'risk-free' wording. Financial assurances are forbidden." },
  { id: "28", title: "No Terms & Conditions", desc: "No 'T&Cs apply', footnotes, or asterisks. All required info must be upfront or not shown at all." },
  { id: "29", title: "Social Safe Zones (9:16)", desc: "For Instagram/Facebook Stories: Top 200px must be empty, Bottom 250px must be empty. Prevents UI overlap." },
  { id: "30", title: "Collision Rules", desc: "Text, tiles, tags, logos, and CTA must never overlap. Any overlap is an automatic failure." },
  { id: "31", title: "Accessibility — Font Size", desc: "Minimum font sizes: 20px (Brand, Social, Checkout Double Density), 10px (Checkout Single Density), 12px (SAYS)." },
  { id: "32", title: "Accessibility — Contrast", desc: "All text and CTA must meet WCAG AA contrast standards. Low contrast = illegal creative." },
  { id: "33", title: "People-in-Image Rule", desc: "If people are detected, user confirmation is required. System must pause — not auto-approve or auto-fail." },
  { id: "34", title: "Format-Aware Rules", desc: "Rules change by format (social, checkout, brand). Safe zones, font sizes, and layout adapt accordingly." },
  { id: "35", title: "Fail-Fast Enforcement", desc: "Any rule violation causes immediate rejection. No auto-fixing, no silent correction, no fallback generation." },
  { id: "36", title: "Error Taxonomy", desc: "Each failure must return a specific error code. This makes compliance auditable and explainable." }
];

const docStyles = {
  container: {
    maxWidth: '1400px',
    margin: '0 auto',
    padding: '0',
    display: 'grid',
    gridTemplateColumns: '280px 1fr',
    minHeight: '100vh',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif',
    color: '#24292f',
    backgroundColor: '#fff',
  },
  sidebar: {
    position: 'sticky',
    top: '0',
    height: '100vh',
    overflowY: 'auto',
    borderRight: '1px solid #d0d7de',
    padding: '24px',
    backgroundColor: '#f6f8fa',
  },
  content: {
    padding: '48px 64px',
    maxWidth: '960px',
  },
  sidebarSection: {
    marginBottom: '24px',
  },
  sidebarHeader: {
    fontSize: '11px',
    fontWeight: '600',
    color: '#57606a',
    textTransform: 'uppercase',
    marginBottom: '8px',
    letterSpacing: '0.5px'
  },
  link: {
    display: 'block',
    padding: '6px 0',
    color: '#24292f',
    textDecoration: 'none',
    fontSize: '14px',
    cursor: 'pointer',
    '&:hover': {
      color: '#0969da',
    }
  },
  searchBox: {
    width: '100%',
    padding: '8px 12px',
    fontSize: '14px',
    border: '1px solid #d0d7de',
    borderRadius: '6px',
    marginBottom: '20px',
    backgroundColor: '#fff'
  },
  h1: {
    fontSize: '32px',
    fontWeight: '600',
    marginBottom: '16px',
    paddingBottom: '8px',
    borderBottom: '1px solid #d0d7de',
  },
  h2: {
    fontSize: '24px',
    fontWeight: '600',
    marginTop: '48px',
    marginBottom: '16px',
    paddingBottom: '0.3em',
    borderBottom: '1px solid #eaecef',
  },
  ruleBox: {
    marginBottom: '24px',
    border: '1px solid #d0d7de',
    borderRadius: '6px',
    overflow: 'hidden',
  },
  ruleHeader: {
    backgroundColor: '#f6f8fa',
    padding: '12px 16px',
    borderBottom: '1px solid #d0d7de',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  ruleId: {
    fontFamily: 'ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace',
    fontSize: '12px',
    backgroundColor: 'rgba(175, 184, 193, 0.2)',
    padding: '2px 6px',
    borderRadius: '4px',
    color: '#24292f',
  },
  ruleContent: {
    padding: '16px',
    lineHeight: '1.6',
    fontSize: '15px',
  }
};

export default function Docs() {
  const [search, setSearch] = useState("");

  const filteredRules = COMPLIANCE_RULES.filter(r =>
    r.title.toLowerCase().includes(search.toLowerCase()) ||
    r.desc.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={docStyles.container}>
      <nav style={docStyles.sidebar}>
        <div style={{ marginBottom: '25px', fontWeight: 'bold', fontSize: '18px' }}>
          Compliance Docs
        </div>

        <input
          type="text"
          placeholder="Search rules..."
          style={docStyles.searchBox}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <div style={docStyles.sidebarSection}>
          <div style={docStyles.sidebarHeader}>Core Principles</div>
          <a style={docStyles.link}>Mandatory Elements</a>
          <a style={docStyles.link}>Safe Zones</a>
          <a style={docStyles.link}>Accessibility</a>
        </div>

        <div style={docStyles.sidebarSection}>
          <div style={docStyles.sidebarHeader}>Restricted Categories</div>
          <a style={docStyles.link}>Alcohol & Drinkaware</a>
          <a style={docStyles.link}>Competitions</a>
          <a style={docStyles.link}>Sustainability Claims</a>
        </div>
      </nav>

      <div style={docStyles.content}>
        <h1 style={docStyles.h1}>Compliance & Validation Rules</h1>
        <p style={{ fontSize: '18px', color: '#57606a', marginBottom: '40px', lineHeight: '1.5' }}>
          The Retail Creative Studio operates on a strict "Zero Tolerance" policy.
          Use this reference to understand the 36 core validation rules enforced by the backend engine.
        </p>

        {filteredRules.length === 0 && (
          <div style={{ padding: '20px', textAlign: 'center', color: '#666' }}>No rules found matching "{search}"</div>
        )}

        {filteredRules.map(rule => (
          <div key={rule.id} style={docStyles.ruleBox}>
            <div style={docStyles.ruleHeader}>
              <span style={{ fontWeight: '600' }}>{rule.title}</span>
              <span style={docStyles.ruleId}>Rule #{rule.id}</span>
            </div>
            <div style={docStyles.ruleContent}>
              {rule.desc}
            </div>
          </div>
        ))}

      </div>
    </div>
  );
}