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

🚀 Getting StartedPrerequisitesPython 3.11+Node.js 18+ & npmDocker Desktop (Optional, for containerized run)Local Development Setup (Manual)1. Clone the RepositoryBashgit clone [https://github.com/Harshitjain1502/fraud-detection-platform.git](https://github.com/Harshitjain1502/fraud-detection-platform.git)
cd fraud-detection-platform
2. Backend SetupBash# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
Swagger API Documentation: http://localhost:8000/docs3. Frontend SetupOpen a new terminal tab:Bashcd frontend
npm install
npm run dev
Dashboard Access: http://localhost:51734. Launch Live Event ProducerOpen a third terminal tab:Bashpython kafka_service/producer.py
Production Deployment via Docker ComposeTo build and run the entire platform with container orchestration:Bashdocker-compose up --build
Frontend Production Dashboard: http://localhostFastAPI Backend Services: http://localhost:8000📊 Analytics API EndpointsMethodEndpointDescriptionGET/Service health status checkPOST/api/v1/predictAnalyzes transaction, returns risk score & triggers background alertsGET/api/v1/recent-transactionsFetches historical transactions from databaseWS/ws/transactionsReal-time WebSocket connection for live UI stream🛠️ Testing & VerificationStart all three components (Backend, Frontend, and Producer).Open http://localhost:5173 in your browser.Confirm that the top bar shows LIVE STREAM ACTIVE (green badge).Verify that transaction logs appear in real time and the Risk Volatility Chart dynamically plots scores across LOW, MEDIUM, and HIGH levels.