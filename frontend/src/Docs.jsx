import { useState } from "react";

// --- CONTENT DATABASES ---

const WORKFLOW_STEPS = [
  {
    step: "1. Prepare",
    title: "Gather Your Assets",
    desc: "Before you start, ensure you have a high-res product image (PNG/JPG) with a clean background if possible, and your brand logo. Decide on your main message vs. sub-message."
  },
  {
    step: "2. Input",
    title: "Enter Campaign Data",
    desc: "Fill in the headline, subhead, and choose your settings. Select a Value Tile if you have a price offer. The system will automatically detect if you are promoting alcohol."
  },
  {
    step: "3. Analyze",
    title: "AI Compliance Check",
    desc: "The 'Limitless' engine scans your text and images. It looks for banned words, human faces, alcohol, and checks against 36 strict retail rules. If it finds issues, it stops."
  },
  {
    step: "4. Create",
    title: "Auto-Composition",
    desc: "If valid, the system builds the creative. It places the logo, product, and text in mathematically perfect 'Safe Zones' for Facebook, Instagram, and Pinterest."
  }
];

const SIMPLE_RULES_LIST = [
  { category: "Mandatory", rules: ["Headline & Subhead required", "Logo & Product required", "Correct Tesco Tag for Pinterest"] },
  { category: "Value Tiles", rules: ["Do not edit 'New' tile", "Clubcard requires Date & Price", "White Tile is for Price only"] },
  { category: "Forbidden", rules: ["No 'Best', 'Cheapest', 'Win'", "No Money-Back Guarantees", "No Sustainability Claims (Eco/Green)"] },
  { category: "Alcohol", rules: ["Drinkaware Lock-up is Mandatory", "No people interacting with alcohol", "Age gating applies"] }
];

const ERROR_DATABASE = [
  // --- CORE & STRUCTURE (E001 - E010) ---
  {
    code: "E001",
    title: "Alcohol Lockup Missing",
    desc: "We detected alcohol keywords (e.g., 'wine', 'beer') or bottles in your image, but the mandatory Drinkaware warning was not applied.",
    fix: "The system will show a 'Confirm Compliance' button. Click it to automatically add the legally required Drinkaware lock-up to the bottom of your creative.",
    rule: "Rule #19, #20: Alcohol requires Drinkaware."
  },
  {
    code: "E002",
    title: "Forbidden Term Detected",
    desc: "Your text contains words that Tesco strictly bans. This includes subjective claims ('Best', 'Delicious'), competitive claims ('Cheaper than'), or promotional fluff.",
    fix: "Rewrite your text to be factual and neutral. Remove words like: best, perfect, win, winner, guarantee, free, gift.",
    rule: "Rule #2, #23: No claims or subjective language."
  },
  {
    code: "E003",
    title: "Structure Missing",
    desc: "The unique 'Limitless' ID for this creative layout is broken because a core element is missing. We cannot generate a partial ad.",
    fix: "Check that you have uploaded a Product Image AND a Logo. Ensure both Headline and Subhead fields have text.",
    rule: "Rule #1: All core elements are mandatory."
  },
  {
    code: "E004",
    title: "Value Tile Violation",
    desc: "You selected a Value Tile (e.g., 'New') but tried to change its text, or selected a tile type that doesn't exist.",
    fix: "If you use the 'New' tile, leave the text field empty or type 'New'. Do not try to write 'New Arrival'. Limitless locks these components strictly.",
    rule: "Rule #6, #7: Value Tiles are locked components."
  },
  {
    code: "E005",
    title: "LEP Violation",
    desc: "Low Everyday Price (LEP) is a strict template. You likely used a colored background or improper logo placement.",
    fix: "Change Background Color to White (#FFFFFF). Remove any extra slogans. LEP must look exactly like the standard template.",
    rule: "Rule #17: LEP requires white background."
  },
  {
    code: "E006",
    title: "Safe Zone Violation",
    desc: "Your content is pushing into the 'Safe Zones'. On Instagram Stories, the top 200px and bottom 250px are reserved for UI elements.",
    fix: "Shorten your headline or subhead. The system is trying to prevent your text from being covered by the Instagram interface.",
    rule: "Rule #29: Respect 9:16 safe zones."
  },
  {
    code: "E009",
    title: "Tag Invalid",
    desc: "You typed a Tesco Tag manually that isn't on the approved legal list.",
    fix: "Do not type manually. Select exactly one of these: 'Only at Tesco', 'Available at Tesco', or 'Selected stores. While stocks last.'",
    rule: "Rule #12: Exact tag wording required."
  },
  {
    code: "E010",
    title: "Tag Missing",
    desc: "This format (e.g., Pinterest) or placement requires a Tesco Tag by law/policy, but none was selected.",
    fix: "Go to the 'Tesco Tag' dropdown and select 'Available at Tesco' (or appropriate option). It cannot be 'None'.",
    rule: "Rule #11: Tags are mandatory for this format."
  },
  {
    code: "E012",
    title: "CTA Not Allowed",
    desc: "You added a Call-to-Action like 'Shop Now', but the current template (Clubcard or LEP) is for information only.",
    fix: "Clear the 'CTA Text' field. Clubcard and LEP creatives are not designed for direct response clicks.",
    rule: "Rule #3: CTA not allowed in this context."
  },
  {
    code: "E013",
    title: "Clubcard Date Missing",
    desc: "A Clubcard Value Tile was selected, but the 'Ends' date is missing or formatted wrong.",
    fix: "Enter the end date strictly as DD/MM (e.g., 25/12). Do not use 'Dec 25' or '25th'.",
    rule: "Rule #10: Date format must be DD/MM."
  },
  {
    code: "E014",
    title: "Clubcard Price Missing",
    desc: "You selected a Clubcard Tile but didn't provide the Clubcard Price.",
    fix: "Enter the price (e.g. £3.50). The tile cannot display without a specific price.",
    rule: "Rule #7: Clubcard prices are mandatory."
  },
  {
    code: "E021",
    title: "Price Language in Text",
    desc: "You mentioned a price (e.g., '£5') or discount ('50% off') in the main Headline or Subhead.",
    fix: "Remove pricing from the text. Prices belong ONLY inside Value Tiles. The main message must be about the product benefit.",
    rule: "Rule #22: No pricing in headlines."
  },
  {
    code: "E022",
    title: "Sustainability Claim",
    desc: "We detected words like 'Eco', 'Green', 'Sustainable', or 'Carbon'. These are high-risk claims.",
    fix: "Remove these words entirely. Retail compliance blocks vague environmental claims to prevent greenwashing.",
    rule: "Rule #25: No green claims."
  },
  {
    code: "E023",
    title: "Competition/Win",
    desc: "Words like 'Win', 'Enter', 'Prize', or 'Giveaway' were detected.",
    fix: "Remove them. This tool creates standard retail assets, not competition headers.",
    rule: "Rule #24: No competitions."
  },
  {
    code: "W001",
    title: "People Detected",
    desc: "Our AI sees a human face or body in your product image.",
    fix: "If this is a model you have rights to use, click 'Confirm Human'. If it's a mistake or a crowd background, try a cleaner product shot.",
    rule: "Rule #33: Human validation required."
  }
];

export default function Docs() {
  const [search, setSearch] = useState("");
  const [selectedError, setSelectedError] = useState(null);

  const filteredErrors = ERROR_DATABASE.filter(e =>
    e.code.toLowerCase().includes(search.toLowerCase()) ||
    e.title.toLowerCase().includes(search.toLowerCase()) ||
    e.desc.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 20px', fontFamily: '"Segoe UI", sans-serif', color: '#333', lineHeight: '1.6' }}>

      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '60px' }}>
        <h1 style={{ fontSize: '36px', marginBottom: '16px', color: '#111' }}>Reference Guide</h1>
        <p style={{ fontSize: '18px', color: '#666', maxWidth: '700px', margin: '0 auto' }}>
          This system ("Limitless") automates strict retail compliance. Use this guide to understand how it makes decisions and how to fix rejection errors.
        </p>
      </div>

      {/* Workflow Section */}
      <div style={{ marginBottom: '60px' }}>
        <h2 style={{ fontSize: '24px', marginBottom: '24px', borderBottom: '2px solid #eee', paddingBottom: '12px' }}>System Workflow</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
          {WORKFLOW_STEPS.map((s, i) => (
            <div key={i} style={{ padding: '20px', backgroundColor: '#f5f7fa', borderRadius: '8px', border: '1px solid #e1e4e8' }}>
              <div style={{ fontSize: '12px', textTransform: 'uppercase', fontWeight: 'bold', color: '#00539F', marginBottom: '8px' }}>{s.step}</div>
              <h3 style={{ fontSize: '18px', marginBottom: '10px', marginTop: 0 }}>{s.title}</h3>
              <p style={{ fontSize: '14px', color: '#444', margin: 0 }}>{s.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Simple Rules Cheat Sheet */}
      <div style={{ marginBottom: '60px' }}>
        <h2 style={{ fontSize: '24px', marginBottom: '24px', borderBottom: '2px solid #eee', paddingBottom: '12px' }}>Quick Rules Checklist</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
          {SIMPLE_RULES_LIST.map((cat, i) => (
            <div key={i} style={{ border: '1px solid #eee', borderRadius: '8px', padding: '20px' }}>
              <h3 style={{ marginTop: 0, color: '#111', fontSize: '16px' }}>{cat.category}</h3>
              <ul style={{ paddingLeft: '20px', margin: 0 }}>
                {cat.rules.map((r, j) => (
                  <li key={j} style={{ fontSize: '14px', color: '#555', marginBottom: '6px' }}>{r}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* Error Search Section with Interactive Modal */}
      <div>
        <h2 style={{ fontSize: '24px', marginBottom: '24px', borderBottom: '2px solid #eee', paddingBottom: '12px' }}>Error & Fix Library</h2>

        <div style={{ marginBottom: '30px' }}>
          <input
            type="text"
            placeholder="Type an error code (E004) or keyword (e.g. Clubcard)..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{
              width: '100%', padding: '16px', fontSize: '16px', borderRadius: '6px',
              border: '1px solid #ccc', outline: 'none'
            }}
          />
        </div>

        <div style={{ display: 'grid', gap: '12px' }}>
          {filteredErrors.length === 0 ? (
            <div style={{ padding: '20px', textAlign: 'center', color: '#666' }}>No results found.</div>
          ) : (
            filteredErrors.map((err) => (
              <div
                key={err.code}
                onClick={() => setSelectedError(err)}
                style={{
                  display: 'flex', alignItems: 'center', gap: '20px', padding: '16px',
                  backgroundColor: '#fff', border: '1px solid #eee', borderRadius: '8px',
                  cursor: 'pointer', transition: 'background 0.2s'
                }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#fafafa'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#fff'}
              >
                <div style={{
                  fontFamily: 'monospace', fontWeight: 'bold', color: '#d32f2f',
                  backgroundColor: '#ffebee', padding: '6px 10px', borderRadius: '4px'
                }}>
                  {err.code}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: '600', color: '#333' }}>{err.title}</div>
                  <div style={{ fontSize: '13px', color: '#666', marginTop: '2px' }}>{err.rule}</div>
                </div>
                <div style={{ fontSize: '20px', color: '#ccc' }}>→</div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* MODAL */}
      {selectedError && (
        <div
          onClick={() => setSelectedError(null)}
          style={{
            position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center',
            zIndex: 9999
          }}
        >
          <div
            onClick={e => e.stopPropagation()}
            style={{
              backgroundColor: 'white', width: '600px', maxWidth: '90%', borderRadius: '12px',
              padding: '40px', boxShadow: '0 4px 20px rgba(0,0,0,0.15)', position: 'relative'
            }}
          >
            <button
              onClick={() => setSelectedError(null)}
              style={{ position: 'absolute', top: '20px', right: '20px', border: 'none', background: 'none', fontSize: '24px', cursor: 'pointer', color: '#999' }}
            >
              &times;
            </button>

            <div style={{ marginBottom: '20px' }}>
              <span style={{ backgroundColor: '#d32f2f', color: 'white', padding: '6px 12px', borderRadius: '4px', fontWeight: 'bold', fontSize: '14px' }}>
                {selectedError.code}
              </span>
            </div>

            <h2 style={{ marginTop: 0, marginBottom: '10px', fontSize: '28px', color: '#111' }}>{selectedError.title}</h2>

            <div style={{ borderBottom: '1px solid #eee', paddingBottom: '20px', marginBottom: '20px' }}>
              <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#888', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Official Rule</div>
              <div style={{ fontSize: '16px', color: '#333' }}>{selectedError.rule}</div>
            </div>

            <div style={{ marginBottom: '30px' }}>
              <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#888', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '8px' }}>Why this happened</div>
              <p style={{ margin: 0, fontSize: '16px', color: '#444' }}>{selectedError.desc}</p>
            </div>

            <div style={{ backgroundColor: '#f0f9ff', padding: '20px', borderRadius: '8px', borderLeft: '4px solid #00539f' }}>
              <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#00539f', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '8px' }}>How to Fix</div>
              <p style={{ margin: 0, fontSize: '16px', color: '#333' }}><strong>{selectedError.fix}</strong></p>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}