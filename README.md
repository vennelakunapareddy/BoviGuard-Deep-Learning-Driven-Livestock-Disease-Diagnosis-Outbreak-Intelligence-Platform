# BoviGuard: Deep Learning-Driven Livestock Disease Diagnosis & Outbreak Intelligence

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org/)
[![React](https://img.shields.io/badge/React-18-cyan.svg)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal.svg)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red.svg)](https://pytorch.org/)

Production-ready, multi-tier AI platform for **bovine and buffalo disease visual image classification & symptom corroboration**, digital animal health record management (EHR), geospatial red alert outbreak tracking with automated 10km quarantine zoning, verified emergency assistance, and nearby veterinary hospital discovery.

---

## 🌟 Key Features

1. **Dual-Stage Out-of-Distribution (OOD) Validation Gate**:
   - Stage 1: Fast image quality inspection (resolution, blur, corruption).
   - Stage 2: Bovine / Non-Bovine filter rejecting non-target uploads (dogs, cats, humans, vehicles, textures) with descriptive guidance.

2. **Multimodal Disease Diagnosis & Symptom Corroboration**:
   - Deep Learning classifier trained on real bovine/buffalo pathology datasets (`MobileNetV2` + `EfficientNet-B0`).
   - Diagnostic targets:
     - **Foot-and-Mouth Disease (FMD)** *(Critical — Epidemic Vector)*
     - **Lumpy Skin Disease (LSD)** *(High — Vector-Borne Outbreak Risk)*
     - **Clinical Mastitis** *(Medium — Localized Udder Infection)*
     - **Multiple Disease Diagnosis** *(Differential Lab Confirmation Required)*
     - **Healthy Buffalo** *(Low — Baseline Healthy Animal)*
   - Cross-validates CNN visual confidence against clinical symptoms checklist.

3. **Geospatial Surveillance & Emergency Quarantine Clusters**:
   - Interactive GIS map powered by Leaflet & React-Leaflet with real-time incident heatmap.
   - Spatial clustering triggering **10km Emergency Quarantine Zones** when $\ge 3$ infectious cases (FMD / LSD) emerge within a localized region.

4. **Digital Animal Health Records (EHR)**:
   - Full case lifecycle tracking (`Open`, `Under Treatment`, `Recovered`, `Closed`, `Emergency`) with MongoDB persistence and local JSON fallback.



---

## 📂 Repository Structure

All project assets are organized cleanly into dedicated top-level folders:

```
BoviGuard/
├── backend/                       # Node.js + Express.js + Socket.IO API server
│   ├── constants/                 # Epidemiological rules, disease info & guidance
│   ├── data/                      # Local JSON fallback store (issues.json, users.json)
│   ├── middleware/                # JWT authentication & request validation
│   ├── models/                    # Mongoose schemas (Animal, Case, Alert, Hospital)
│   ├── routes/                    # REST API endpoints (cases, alerts, auth, hospitals)
│   ├── services/                  # Image analysis bridge, email alerts & clustering
│   ├── uploads/                   # Upload storage & sample buffalo images
│   ├── seed.js                    # Database seeder script
│   └── server.js                  # Backend API gateway entry point
│
├── frontend/                      # React 18 + Vite + TailwindCSS Web UI
│   ├── dist/                      # Pre-built production bundle for instant startup
│   ├── public/                    # Static web assets & icons
│   ├── src/                       # React components, pages, context, and hooks
│   ├── package.json               # Frontend dependencies & scripts
│   └── vite.config.js             # Vite build pipeline
│
├── ml-service/                    # Python FastAPI + PyTorch Inference Microservice
│   ├── buffalo_effnet_b0.pth      # EfficientNet-B0 trained weights
│   ├── buffalo_model.pth          # Primary CNN classifier weights
│   ├── exemplar_bank.pt           # Feature embeddings bank for OOD distance
│   ├── centroids.pt               # Class centroid vectors
│   ├── classes.json               # Class index mapping
│   ├── app.py                     # FastAPI application endpoints (/predict, /health)
│   ├── model.py                   # PyTorch neural network architectures
│   ├── grad_cam.py                # Grad-CAM explainability heatmaps
│   ├── requirements.txt           # Python dependency specifications
│   ├── buffalo_dataset/           # Training, validation & test splits
│   └── real_world_holdout/        # Rigorous holdout evaluation dataset
│
├── tests/                         # Centralized Test Suite & Verification Assets
│   ├── run_final_verification_suite.py # End-to-end multi-case diagnostic test
│   ├── test_rejection_suite.py    # Out-of-Distribution rejection benchmark
│   ├── run_full_api_audit.py      # Complete REST API audit
│   ├── test_dog.jpg, test_cat.jpg # OOD negative benchmark images
│   ├── test_hen.jpg, test_car.jpg # OOD rejection images
│   ├── unseen_healthy_buffalo.jpg # Authentic positive benchmark images
│   ├── corrupted_blur.jpg         # Quality rejection sample
│   ├── scratch/                   # Experimental diagnostics & verification tools
│   └── README.md                  # Test suite documentation & image catalog
│
├── run_project.js                 # Universal cross-platform orchestrator
├── start.bat                      # One-click Windows startup script
├── start_all_servers.py           # Multi-process Python service launcher
├── package.json                   # Root orchestrator & backend dependencies
├── .env.example                   # Environment configuration template
└── .gitignore                     # Production Git ignore rules
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Node.js**: v18.0.0 or higher
- **Python**: v3.10 or higher
- **MongoDB** *(Optional)*: Local or Atlas instance (system automatically falls back to local JSON persistence if MongoDB is absent).

---

### Method 1: One-Click Startup (Windows)

1. Double-click **`start.bat`** (or open PowerShell in the project root and run `.\start.bat`).
2. The script automatically:
   - Starts the **ML FastAPI Microservice** on `http://127.0.0.1:5000`
   - Performs a health-check poll until ready
   - Starts the **Node.js Backend & Web App** on `http://localhost:3000`
3. Open **`http://localhost:3000`** in your browser.

---

### Method 2: Universal Node Runner

From the project root:
```bash
# 1. Install root dependencies
npm install

# 2. Run the orchestrator
node run_project.js
```

---

### Method 3: Manual Terminal Startup

**Terminal 1 — Python ML Microservice**:
```bash
cd ml-service
python -m venv venv
# On Windows:
.\venv\Scripts\pip install -r requirements.txt
# On Linux/macOS:
source venv/bin/activate && pip install -r requirements.txt

python -m uvicorn app:app --host 127.0.0.1 --port 5000
```

**Terminal 2 — Node.js Backend API Server**:
```bash
npm install
npm start
# Server listens on http://localhost:3000 and serves frontend/dist
```

**Terminal 3 (Optional) — Frontend Vite Development Server**:
```bash
cd frontend
npm install
npm run dev
# Live reloading dev server runs on http://localhost:5173
```

---

## 🧪 Testing & Verification

All test suites and benchmark images are inside the [`tests/`](./tests) folder:

```bash
cd tests

# End-to-end multi-case diagnostic test
python run_final_verification_suite.py

# Out-of-Distribution rejection suite (dogs, cats, cars, humans)
python test_rejection_suite.py

# Full API health audit
python run_full_api_audit.py
```

---

## 📤 Pushing This Repository to GitHub

This repository is ready to push:

```bash
# 1. Navigate into this folder in your terminal:
cd C:\Users\venne\Downloads\BoviGuard

# 2. Add your GitHub remote repository URL (replace with your repo link):
git remote add origin https://github.com/vennelakunapareddy/<your-repo-name>.git

# 3. Ensure your branch is named main:
git branch -M main

# 4. Push to GitHub:
git push -u origin main
```

*(If pushing to an existing remote repository with history, use `git push -u origin main --force`).*

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
