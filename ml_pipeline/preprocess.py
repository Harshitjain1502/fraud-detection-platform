import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.categorical_cols = ['merchant', 'category', 'location', 'device_type']
        self.numeric_cols = ['amount', 'hour_of_day', 'day_of_week', 'amount_ratio_to_avg', 'customer_txn_count']

    def create_engineered_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts temporal and behavioral velocity features.
        """
        df = df.copy()
        
        # Ensure timestamp is datetime type
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 1. Temporal Features
        df['hour_of_day'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_night'] = df['hour_of_day'].apply(lambda x: 1 if (x >= 0 and x <= 5) else 0)

        # 2. Velocity & Behavioral Aggregations
        # Customer historical spending average
        customer_avg = df.groupby('customer_id')['amount'].transform('mean')
        df['customer_avg_amount'] = customer_avg
        
        # Amount ratio: Spikes in spending behavior (e.g., usually spends $10, now spending $1000 -> ratio = 100)
        df['amount_ratio_to_avg'] = df['amount'] / (df['customer_avg_amount'] + 1e-5)
        
        # Customer transaction velocity count
        df['customer_txn_count'] = df.groupby('customer_id')['transaction_id'].transform('count')

        return df

    def fit_transform(self, df: pd.DataFrame):
        """
        Fits preprocessors on training data and returns transformed feature matrix (X) and targets (y).
        """
        print("Starting Data Preprocessing & Feature Engineering...")
        
        # 1. Extract Engineered Features
        df_processed = self.create_engineered_features(df)

        # 2. Encode Categorical Columns
        for col in self.categorical_cols:
            le = LabelEncoder()
            df_processed[col] = le.fit_transform(df_processed[col].astype(str))
            self.label_encoders[col] = le

        # 3. Select Features for ML
        feature_columns = self.categorical_cols + self.numeric_cols + ['is_night']
        X = df_processed[feature_columns]
        y = df_processed['is_fraud'] if 'is_fraud' in df_processed.columns else None

        # 4. Scale Numeric Features
        X_scaled = X.copy()
        X_scaled[self.numeric_cols] = self.scaler.fit_transform(X_scaled[self.numeric_cols])

        # 5. Save Scaler and Label Encoders for Real-time Inference Pipeline
        os.makedirs("ml_pipeline/models", exist_ok=True)
        joblib.dump(self.scaler, "ml_pipeline/models/scaler.pkl")
        joblib.dump(self.label_encoders, "ml_pipeline/models/label_encoders.pkl")
        
        print("Preprocessing successfully completed. Scaler & Encoders saved.")
        return X_scaled, y, feature_columns

if __name__ == "__main__":
    data_path = "ml_pipeline/data/transactions.csv"
    if os.path.exists(data_path):
        raw_df = pd.read_csv(data_path)
        preprocessor = DataPreprocessor()
        X, y, feature_names = preprocessor.fit_transform(raw_df)
        
        print(f"\nEngineered Dataset Shape: {X.shape}")
        print(f"Features List: {feature_names}")
        print("\nSample Preprocessed Data (First 3 Rows):")
        print(X.head(3))
    else:
        print(f"Error: {data_path} not found. Run Step 2 (generate_dataset.py) first.")