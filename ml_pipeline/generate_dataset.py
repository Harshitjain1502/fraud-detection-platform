import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_synthetic_transactions(num_records=100000, fraud_ratio=0.015):
    """
    Generates synthetic banking transaction data with realistic fraud patterns.
    
    Parameters:
    - num_records: Total number of transactions
    - fraud_ratio: Percentage of fraudulent transactions (e.g., 0.015 = 1.5%)
    """
    print(f"Generating {num_records} transaction records...")

    num_fraud = int(num_records * fraud_ratio)
    num_normal = num_records - num_fraud

    # 1. Base Details
    customer_ids = [f"CUST_{i:05d}" for i in range(1, 2001)] # 2,000 unique customers
    merchants = ["Amazon", "Walmart", "Uber", "Apple", "Netflix", "Gas Station", "Luxury Store", "Crypto Exchange"]
    categories = ["retail", "groceries", "travel", "entertainment", "electronics", "utilities"]
    locations = ["New York, US", "London, UK", "Mumbai, IN", "Tokyo, JP", "Berlin, DE", "Toronto, CA"]

    # 2. Normal Transactions Generation
    normal_data = {
        "transaction_id": [f"TXN_{i:07d}" for i in range(1, num_normal + 1)],
        "customer_id": np.random.choice(customer_ids, num_normal),
        "amount": np.round(np.random.exponential(scale=50, size=num_normal) + 5, 2), # Typical small daily purchases
        "timestamp": [
            datetime(2026, 1, 1) + timedelta(
                days=int(np.random.randint(0, 60)),
                hours=int(np.random.choice(range(6, 23))), # Mostly active during day hours
                minutes=int(np.random.randint(0, 60)),
                seconds=int(np.random.randint(0, 60))
            ) for _ in range(num_normal)
        ],
        "merchant": np.random.choice(merchants[:6], num_normal),
        "category": np.random.choice(categories[:4], num_normal),
        "location": np.random.choice(locations[:3], num_normal),
        "device_type": np.random.choice(["mobile", "desktop", "pos_terminal"], num_normal, p=[0.6, 0.3, 0.1]),
        "is_fraud": 0
    }

    # 3. Fraudulent Transactions Generation (Simulating Anomaly Patterns)
    fraud_data = {
        "transaction_id": [f"TXN_{i:07d}" for i in range(num_normal + 1, num_records + 1)],
        "customer_id": np.random.choice(customer_ids, num_fraud),
        "amount": np.round(np.random.uniform(500, 5000, size=num_fraud), 2), # High amounts
        "timestamp": [
            datetime(2026, 1, 1) + timedelta(
                days=int(np.random.randint(0, 60)),
                hours=int(np.random.choice([0, 1, 2, 3, 4])), # Late midnight transactions
                minutes=int(np.random.randint(0, 60)),
                seconds=int(np.random.randint(0, 60))
            ) for _ in range(num_fraud)
        ],
        "merchant": np.random.choice(["Luxury Store", "Crypto Exchange", "Apple"], num_fraud),
        "category": np.random.choice(["electronics", "travel"], num_fraud),
        "location": np.random.choice(locations[3:], num_fraud), # Foreign location anomaly
        "device_type": np.random.choice(["mobile", "desktop"], num_fraud, p=[0.2, 0.8]),
        "is_fraud": 1
    }

    # Convert to DataFrames
    df_normal = pd.DataFrame(normal_data)
    df_fraud = pd.DataFrame(fraud_data)

    # Combine & Shuffle Dataset
    df = pd.concat([df_normal, df_fraud], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Output directory check
    os.makedirs("ml_pipeline/data", exist_ok=True)
    output_path = "ml_pipeline/data/transactions.csv"
    df.to_csv(output_path, index=False)

    print(f"Dataset generated successfully and saved to: {output_path}")
    print(f"Total Records: {len(df)} | Fraud Records: {df['is_fraud'].sum()} ({df['is_fraud'].mean()*100:.2f}%)")

if __name__ == "__main__":
    generate_synthetic_transactions()