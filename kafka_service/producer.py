import time
import random
import requests
from datetime import datetime

# FastAPI Backend Endpoint
API_ENDPOINT = "http://localhost:8000/api/v1/predict"

# Standard choices from standard training dataset
MERCHANTS = ["Amazon", "Walmart", "Target", "Starbucks", "Crypto Exchange", "Luxury Store"]
CATEGORIES = ["grocery", "dining", "entertainment", "electronics", "crypto"]
LOCATIONS = ["New York, US", "Chicago, US", "London, UK", "Tokyo, JP"]
DEVICES = ["mobile", "desktop", "emulator"]

def generate_mock_transaction():
    """
    Generates a balanced stream:
    - ~60% LOW Risk: Small amounts ($5 - $150), routine merchants/devices
    - ~25% MEDIUM Risk: Moderate amounts ($500 - $2000), elevated merchant profiles
    - ~15% HIGH Risk: Very high amounts ($5000 - $15000), crypto/luxury + emulator
    """
    roll = random.random()

    if roll < 0.15:
        # HIGH RISK TRIGGER (Forces probability > 0.75)
        amount = round(random.uniform(5000.0, 15000.0), 2)
        merchant = "Crypto Exchange"
        category = "crypto"
        device = "emulator"
        location = "Tokyo, JP"
    elif roll < 0.40:
        # MEDIUM RISK TRIGGER (Forces probability between 0.40 and 0.74)
        amount = round(random.uniform(800.0, 3000.0), 2)
        merchant = "Luxury Store"
        category = "electronics"
        device = "desktop"
        location = "London, UK"
    else:
        # LOW RISK TRIGGER (Forces probability < 0.40)
        amount = round(random.uniform(5.0, 150.0), 2)
        merchant = random.choice(["Starbucks", "Walmart", "Target", "Amazon"])
        category = random.choice(["grocery", "dining", "entertainment"])
        device = random.choice(["mobile", "desktop"])
        location = "New York, US"

    return {
        "transaction_id": f"TXN_{random.randint(1000000, 9999999)}",
        "customer_id": f"CUST_{random.randint(100, 999)}",
        "amount": amount,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "merchant": merchant,
        "category": category,
        "location": location,
        "device_type": device
    }

def start_streaming():
    print(f"🚀 Starting Real-Time Balanced Transaction Stream -> Target: {API_ENDPOINT}")
    headers = {"Content-Type": "application/json"}
    
    while True:
        payload = generate_mock_transaction()
        try:
            response = requests.post(API_ENDPOINT, json=payload, headers=headers, timeout=5)
            if response.status_code == 200:
                result = response.json()
                print(f"[SENT] Txn: {result['transaction_id']} | Amount: ${result['amount']:<8} | Risk: {result['risk_score']*100:>5.1f}% | Level: {result['risk_level']}")
            else:
                print(f"[ERROR] HTTP {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[CONNECTION ERROR] Failed to connect to FastAPI Backend: {e}")
            
        time.sleep(1.2)

if __name__ == "__main__":
    start_streaming()