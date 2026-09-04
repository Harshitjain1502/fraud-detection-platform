
# Project Title

A brief description of what this project does and who it's for

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

 
## 1. Getting Started

## Prerequisites

Before running the project, make sure you have the following installed:

- **Python 3.11+**
- **Node.js 18+ & npm**
- **Docker Desktop** *(Optional — required only for containerized deployment)*

---

## 🛠️ Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Harshitjain1502/fraud-detection-platform.git
cd fraud-detection-platform
## 2. Backend Setup

Create and activate a Python virtual environment:

python -m venv venv

Windows:

venv\Scripts\activate

macOS/Linux:

source venv/bin/activate

Install the required dependencies:

pip install -r requirements.txt

Start the FastAPI backend server:

python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
📚 Swagger API Documentation

Once the backend is running, access the interactive API documentation at:

http://localhost:8000/docs
## 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

cd frontend
npm install
npm run dev

The frontend will be available at:

http://localhost:5173
## 4. Launch Live Event Producer

Open a third terminal and run the Kafka transaction producer:

python kafka_service/producer.py

This will generate and stream transaction events to the backend in real time.
## 🐳 Production Deployment via Docker Compose

To build and run the complete platform using Docker Compose:

docker-compose up --build

Once the containers are running:

Frontend Dashboard: http://localhost
FastAPI Backend: http://localhost:8000
FastAPI Swagger Docs: http://localhost:8000/docs

To stop the containers:

docker-compose down
## 📊 Analytics API Endpoints

| Method | Endpoint                      | Description                                                                  |
| ------ | ----------------------------- | ---------------------------------------------------------------------------- |
| `GET`  | `/`                           | Service health status check                                                  |
| `POST` | `/api/v1/predict`             | Analyzes a transaction, returns a risk score, and triggers background alerts |
| `GET`  | `/api/v1/recent-transactions` | Fetches recent/historical transactions from the database                     |
| `WS`   | `/ws/transactions`            | Real-time WebSocket connection for the live dashboard transaction stream     |

## 🧪 Testing & Verification

Follow these steps to verify that the platform is working correctly.

Step 1: Start All Components

Start the following three components:

FastAPI Backend
React Frontend
Kafka Event Producer
Step 2: Open the Dashboard

Open the frontend in your browser:

http://localhost:5173

Step 3: Verify Live Streaming

Confirm that the top navigation bar displays:

🟢 LIVE STREAM ACTIVE

This indicates that the frontend has successfully established a real-time connection with the backend.

Step 4: Verify Transaction Logs

Transaction events should begin appearing in the dashboard automatically.

Verify that:

New transactions appear in real time.
Transaction risk scores are displayed.
Transaction status is updated dynamically.
No manual page refresh is required.
Step 5: Verify Risk Volatility Chart

Check the Risk Volatility Chart on the dashboard.

The chart should dynamically plot transaction risk scores across:

🟢 LOW
🟡 MEDIUM
🔴 HIGH

As new transactions are generated by the Kafka producer, the chart should continuously update with the latest risk scores.
## ✅ Expected Result

If everything is configured correctly, the dashboard should provide:

⚡ Real-time transaction streaming
📊 Dynamic risk visualization
🤖 ML-powered fraud risk scoring
🔔 Background fraud alerts
🔄 WebSocket-based live updates
🗄️ Historical transaction data
📈 Risk volatility monitoring