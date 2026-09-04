import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve, auc
import xgboost as xgb

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

from preprocess import DataPreprocessor

# Set random seeds
np.random.seed(42)
tf.random.set_seed(42)

class ModelTrainer:
    def __init__(self, data_path="ml_pipeline/data/transactions.csv"):
        self.data_path = data_path
        self.models_dir = "ml_pipeline/models"
        os.makedirs(self.models_dir, exist_ok=True)

    def load_and_preprocess_data(self):
        print("Loading raw transaction data...")
        df = pd.read_csv(self.data_path)
        
        preprocessor = DataPreprocessor()
        X, y, feature_names = preprocessor.fit_transform(df)
        
        # Save feature names list
        joblib.dump(feature_names, os.path.join(self.models_dir, "feature_names.pkl"))
        
        return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y), feature_names

    def train_xgboost(self, X_train, y_train, X_test, y_test):
        print("\n--- Training XGBoost Classifier ---")
        
        # Handle Class Imbalance ratio (Legitimate / Fraud)
        ratio = (len(y_train) - sum(y_train)) / sum(y_train)
        
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.05,
            scale_pos_weight=ratio,
            random_state=42,
            eval_metric="logloss"
        )
        
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        
        print("XGBoost Evaluation Metrics:")
        print(classification_report(y_test, y_pred))
        print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")
        
        joblib.dump(model, os.path.join(self.models_dir, "xgboost_model.pkl"))
        return model

    def train_random_forest(self, X_train, y_train, X_test, y_test):
        print("\n--- Training Random Forest Classifier ---")
        
        model = RandomForestClassifier(
            n_estimators=100,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        
        print("Random Forest Evaluation Metrics:")
        print(classification_report(y_test, y_pred))
        print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")
        
        joblib.dump(model, os.path.join(self.models_dir, "random_forest_model.pkl"))
        return model

    def train_isolation_forest(self, X_train, X_test, y_test):
        print("\n--- Training Unsupervised Isolation Forest ---")
        
        # Unsupervised Model: Trained on normal transactions (no target labels used during fit)
        model = IsolationForest(
            n_estimators=100,
            contamination=0.015, # Expected anomaly proportion
            random_state=42
        )
        
        model.fit(X_train)
        
        # Isolation Forest returns -1 for anomaly and 1 for normal
        preds = model.predict(X_test)
        preds_binary = [1 if p == -1 else 0 for p in preds]
        
        print("Isolation Forest Evaluation Metrics:")
        print(classification_report(y_test, preds_binary))
        
        joblib.dump(model, os.path.join(self.models_dir, "isolation_forest.pkl"))
        return model

    def train_autoencoder(self, X_train, X_test, y_train, y_test):
        print("\n--- Training Deep Autoencoder Network ---")
        
        # Filter only NORMAL transactions for Autoencoder training
        X_train_normal = X_train[y_train == 0]
        input_dim = X_train.shape[1]
        
        # Autoencoder Architecture
        input_layer = Input(shape=(input_dim,))
        encoder = Dense(8, activation="relu")(input_layer)
        encoder = Dense(4, activation="relu")(encoder)
        decoder = Dense(8, activation="relu")(encoder)
        decoder = Dense(input_dim, activation="linear")(decoder)
        
        autoencoder = Model(inputs=input_layer, outputs=decoder)
        autoencoder.compile(optimizer="adam", loss="mean_squared_error")
        
        # Train Autoencoder to compress and reconstruct NORMAL data
        autoencoder.fit(
            X_train_normal, X_train_normal,
            epochs=10,
            batch_size=64,
            validation_data=(X_test, X_test),
            verbose=0
        )
        
        # Calculate Reconstruction Error on Test set
        reconstructions = autoencoder.predict(X_test)
        mse = np.mean(np.power(X_test - reconstructions, 2), axis=1)
        
        # Determine threshold for anomaly
        threshold = np.percentile(mse, 98) # Top 2% highest reconstruction error as fraud
        preds_binary = (mse > threshold).astype(int)
        
        print(f"Autoencoder Reconstruction Loss Threshold: {threshold:.4f}")
        print("Autoencoder Evaluation Metrics:")
        print(classification_report(y_test, preds_binary))
        
        autoencoder.save(os.path.join(self.models_dir, "autoencoder_model.keras"))
        return autoencoder

if __name__ == "__main__":
    trainer = ModelTrainer()
    (X_train, X_test, y_train, y_test), feature_names = trainer.load_and_preprocess_data()
    
    # Train Supervised Models
    trainer.train_xgboost(X_train, y_train, X_test, y_test)
    trainer.train_random_forest(X_train, y_train, X_test, y_test)
    
    # Train Unsupervised Anomaly Models
    trainer.train_isolation_forest(X_train, X_test, y_test)
    trainer.train_autoencoder(X_train, X_test, y_train, y_test)
    
    print("\nAll models trained and saved successfully in 'ml_pipeline/models/'!")