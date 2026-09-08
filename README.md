# 🛡️ Real-Time AI Financial Fraud Analytics Platform

A production-grade, end-to-end financial anomaly detection and real-time risk scoring platform. Built using a modular FastAPI backend, XGBoost inference pipeline, WebSockets, persistent SQLite storage, and a Vite/React analytics dashboard.

---

## 🌟 Key Features

* **Multi-Model Inference Engine:** XGBoost model integrated with rule-based heuristic fallbacks for dynamic risk scoring (0.0 to 1.0).
* **Real-Time Stream Processing:** Asynchronous event broadcasting via WebSockets to feed transaction streams live to connected UI clients.
* **Operations Dashboard:** Built with React, Vite, and Recharts—featuring real-time risk volatility graphs, live event logs, and status badges (`CLEARED`, `MEDIUM RISK`, `HIGH RISK`).
* **Non-Blocking Alert System:** Background worker pipeline triggers non-blocking email/Slack alerts for transactions flagged with high risk scores.
* **Persistent Analytics Database:** SQLAlchemy ORM integration with SQLite to store historical records and support analytical queries.
* **Containerized Architecture:** Fully dockerized stack orchestrated via Docker Compose for easy production deployment.

---

## 🏗️ Architecture & Tech Stack

* **Backend:** Python 3.11, FastAPI, Uvicorn, SQLAlchemy, Pydantic v2
* **Frontend:** React 18, Vite, TailwindCSS, Recharts, Lucide Icons
* **Machine Learning:** XGBoost, Scikit-Learn, TensorFlow/Keras, Pandas, NumPy
* **Infrastructure & Tooling:** Docker, Docker Compose, Git

---

## Getting Started

### Prerequisites
* **Python 3.11**
* **Node.js 18 & npm**
* **Docker Desktop** (Optional for containerized run)

---

## Local Development Setup (Manual)

### 1. Clone the Repository
```bash
git clone https://github.com
cd fraud-detection-platform
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
* **Swagger API Documentation:** `http://localhost:8000/docs`

### 3. Frontend Setup
Open a new terminal tab:
```bash
cd frontend
npm install
npm run dev
```
* **Dashboard Access:** `http://localhost:5173`

### 4. Launch Live Event Producer
Open a third terminal tab:
```bash
python kafka_service/producer.py
```

---

## Production Deployment via Docker Compose

To build and run the entire platform with container orchestration:
```bash
docker compose up --build
```
* **Frontend Production Dashboard:** `http://localhost`
* **FastAPI Backend Services:** `http://localhost:8000`

---

## Analytics API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/` | Service health status check |
| **POST** | `/api/v1/predict` | Analyzes transaction, returns risk score, and triggers background alerts |
| **GET** | `/api/v1/recent-transactions` | Fetches historical transactions from the database |
| **WS** | `/ws/transactions` | Real-time WebSocket connection for live UI stream |

---

## Testing & Verification

1. Start all three components (**Backend**, **Frontend**, and **Producer**).
2. Open `http://localhost:5173` in your browser.
3. Confirm that the top bar shows the **"LIVE STREAM ACTIVE"** green badge.
4. Verify that transaction logs appear in real time and the **Risk Volatility Chart** dynamically plots scores across `LOW`, `MEDIUM`, and `HIGH` levels


## 📁 Repository Structure

```text
fraud-detection-platform/
├── backend/
│   ├── app/
│   │   ├── core/           # Database setup and connection engine
│   │   ├── models/         # SQLAlchemy ORM transaction schema
│   │   └── services/       # ML Inference, Alerting, & WebSocket managers
│   ├── Dockerfile
│   └── main.py             # FastAPI entry point & API endpoints
├── frontend/
│   ├── src/                # React components & dashboard layout
│   ├── Dockerfile
│   └── package.json
├── kafka_service/
│   ├── producer.py         # Synthetic streaming transaction generator
│   └── consumer.py
├── ml_pipeline/
│   └── models/             # Trained XGBoost models, scalers, encoders
├── docker-compose.yml      # Multi-container orchestration config
├── requirements.txt        # Python backend dependencies
└── README.md
