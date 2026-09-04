import json
import time
import requests
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'financial_transactions'
FASTAPI_INFERENCE_URL = 'http://localhost:8000/api/v1/predict'

def start_consumer():
    """
    Subscribes to Kafka transaction stream and forwards payloads
    to FastAPI Inference Pipeline in real-time.
    """
    print("Initializing Kafka Consumer Engine...")
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=[KAFKA_BROKER],
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='fraud-analysis-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        print(f"Subscribed to topic '{TOPIC_NAME}'. Waiting for live transactions...")

        for message in consumer:
            txn_data = message.value
            print(f"\n[Kafka Stream Received]: Txn ID: {txn_data['transaction_id']} | Amount: ${txn_data['amount']}")
            
            # Send to FastAPI ML Engine
            try:
                response = requests.post(FASTAPI_INFERENCE_URL, json=txn_data, timeout=2.0)
                if response.status_code == 200:
                    result = response.json()
                    print(f" -> ML Decision: Risk Score: {result.get('risk_score')} | Risk Level: {result.get('risk_level')}")
                else:
                    print(f" -> API Error Response: {response.status_code}")
            except requests.exceptions.ConnectionError:
                print(" -> Warning: FastAPI Server unavailable on http://localhost:8000. Make sure Step 7 API is running.")

    except NoBrokersAvailable:
        print(f"Error: Could not connect to Kafka Broker at {KAFKA_BROKER}.")
        print("Fallback Mode: Ensure Apache Kafka service is running via Docker / Local server.")

if __name__ == "__main__":
    start_consumer()