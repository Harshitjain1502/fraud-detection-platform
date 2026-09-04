import joblib
import pandas as pd
import numpy as np
import shap
import os

class FraudExplainer:
    def __init__(self, models_dir="ml_pipeline/models"):
        self.models_dir = models_dir
        self.model = joblib.load(os.path.join(models_dir, "xgboost_model.pkl"))
        self.scaler = joblib.load(os.path.join(models_dir, "scaler.pkl"))
        self.label_encoders = joblib.load(os.path.join(models_dir, "label_encoders.pkl"))
        self.feature_names = joblib.load(os.path.join(models_dir, "feature_names.pkl"))
        
        # Initialize SHAP TreeExplainer for Tree-based models (XGBoost)
        self.explainer = shap.TreeExplainer(self.model)

    def explain_transaction(self, transaction_df: pd.DataFrame):
        """
        Takes a single preprocessed transaction DataFrame row and returns 
        top feature contributions to the fraud risk score.
        """
        # Calculate SHAP values for the given instance
        shap_values = self.explainer.shap_values(transaction_df)
        
        # If binary classification returns list or array shape
        if isinstance(shap_values, list):
            vals = shap_values[1][0]
        elif len(shap_values.shape) == 2:
            vals = shap_values[0]
        else:
            vals = shap_values

        # Pair features with their SHAP values
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'shap_value': vals,
            'feature_value': transaction_df.iloc[0].values
        })

        # Sort by absolute impact on risk score
        feature_importance['abs_impact'] = feature_importance['shap_value'].abs()
        feature_importance = feature_importance.sort_values(by='abs_impact', ascending=False)

        # Build readable explanation list
        explanations = []
        for _, row in feature_importance.head(4).iterrows():
            direction = "increased risk" if row['shap_value'] > 0 else "decreased risk"
            explanations.append({
                "feature": row['feature'],
                "impact": round(float(row['shap_value']), 4),
                "description": f"Feature '{row['feature']}' ({row['feature_value']}) {direction}."
            })

        return {
            "top_risk_factors": explanations,
            "raw_shap_values": dict(zip(self.feature_names, [round(float(v), 4) for v in vals]))
        }

if __name__ == "__main__":
    from preprocess import DataPreprocessor

    data_path = "ml_pipeline/data/transactions.csv"
    if os.path.exists(data_path):
        raw_df = pd.read_csv(data_path)
        
        # Pick 1 sample fraudulent transaction for testing explanation
        fraud_sample = raw_df[raw_df['is_fraud'] == 1].head(1)
        
        preprocessor = DataPreprocessor()
        X, _, _ = preprocessor.fit_transform(raw_df)
        
        # Select corresponding preprocessed row
        sample_index = fraud_sample.index[0]
        X_sample = X.iloc[[sample_index]]

        explainer = FraudExplainer()
        explanation = explainer.explain_transaction(X_sample)

        print("\n--- Real-Time Transaction Explanation ---")
        print(f"Transaction ID: {fraud_sample['transaction_id'].values[0]}")
        print("Top Risk Factors Identified by SHAP Engine:")
        for factor in explanation["top_risk_factors"]:
            print(f" -> {factor['description']} (SHAP Score: {factor['impact']})")
    else:
        print(f"Error: {data_path} not found.")