
# AI Retail Creative Studio

**Strict Compliance Generation Engine for Enterprise Retail Assets**

The AI Retail Creative Studio is a state-of-the-art automated design system built to generate localized, brand-compliant retail marketing assets at scale. Unlike standard generative tools, this system is built on a "Compliance-First" architecture that strictly strictly enforces brand guidelines, legal requirements, and layout safety zones before any content is created.

---

## 🚀 Key Features

### 🛡️ Strict Compliance Engine
*   **Zero Tolerance Policy**: Hard-coded rejection of forbidden content (Financial claims, Competitions, Sustainability assertions).
*   **Alcohol & Age Gating**: Semantic analysis detects alcohol-related copy and automatically injects mandatory, high-contrast "Drinkaware" lock-ups.
*   **Accessibility Gates**: Enforces WCAG AA contrast ratios and minimum font sizes (20px Brand / 12px SAYS / 10px Checkout).

### 🎨 Dynamic Template System
*   **LEP Mode (Low Everyday Price)**: Restrictive template enforcing White Backgrounds, Tesco Blue typography, and specific layout rules.
*   **Social Safe Zones**: 9:16 "Stories" format enforcement with rigid 200px Top / 250px Bottom exclusion zones.
*   **Value Tiles**: Immutable, schema-driven components ("New", "Clubcard Price", "White Value Tile") that resist tampering.

### 👁️ Computer Vision Integration
*   **People Detection**: OpenCV-based filtering scans product imagery for human faces.
*   **Verification Loop**: Triggers a "Confirmation Required" workflow if talent is detected, ensuring usage rights compliance.

### 📐 Geometric Layout Solver
*   **Collision Avoidance**: Physics-based layout ensures Packshots, Logos, and CTAs never overlap text or safe zones.
*   **Visual Priority**: Mathematical enforcement of "Packshot needs to be the closest element to the CTA".

---

## 🏗️ Architecture

The solution uses a decoupled **React + FastAPI** architecture, containerized for rapid deployment.

```
├── backend/             # Python FastAPI Service
│   ├── composer.py      # Core Layout & Rendering Engine
│   ├── validator.py     # Compliance Logic Gate (Text & Image)
│   ├── compliance_rules.py # Central Rules Dictionary
│   └── ...
├── frontend/            # React Vite Application
│   ├── src/Chat.jsx     # Main Creative Interface
│   ├── src/Docs.jsx     # Technical Documentation Portal
│   └── ...
└── docker-compose.yml   # Orchestration
```

---

## 🛠️ Installation & Deployment

### Prerequisites
*   Docker & Docker Compose
*   (Or) Python 3.10+ & Node.js 18+

### 🐳 Docker Deployment (Recommended)
This will spin up both the Backend API and Frontend Client in isolated containers.

```bash
# 1. Clone the repository
git clone <repo-url>
cd retail-creative-studio

# 2. Build and Run
docker-compose up --build
```

*   **Frontend**: http://localhost:3000
*   **Backend Docs**: http://localhost:8000/docs
*   **Application Docs**: http://localhost:3000/docs

### 💻 Local Development
If you prefer running locally without Docker:

**Backend:**
```bash
cd backend
pip install -r req.txt
python -m uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 📖 Usage Guide

1.  **Ingest**: Upload a high-res Product Packshot and Brand Logo. The system automatically removes the product background.
2.  **Configure**:
    *   **Headline/Subhead**: Enter your localized copy.
    *   **Template**: Choose 'Standard' or 'LEP' (Low Everyday Price).
    *   **Tiles**: Optionally add 'New' or 'Clubcard' value tiles.
3.  **Validate**: Click "Generate". The system runs `validator.py`:
    *   *Scan Copy*: For banned keywords ("best", "win", "green").
    *   *Scan Image*: For people (requires manual confirm if found).
    *   *Check Structure*: Ensures mandatory headline/subhead presence.
4.  **Result**: If compliant, the system generates assets in:
    *   9:16 (Story)
    *   1:1 (Feed)
    *   16:9 (Landscape)

---

## 📚 Documentation
Full technical documentation is available within the application at the `/docs` route.

---
**Authored by Antigravity Agent**