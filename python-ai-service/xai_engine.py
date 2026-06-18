import joblib
import pandas as pd
import shap
import os
import numpy as np

# Load model and background data
model_path = os.path.join(os.path.dirname(__file__), 'fraud_model.pkl')
bg_data_path = os.path.join(os.path.dirname(__file__), 'background_data.csv')

if not os.path.exists(model_path):
    print("Model not found. Please run model_trainer.py first.")
else:
    model = joblib.load(model_path)
    bg_data = pd.read_csv(bg_data_path)
    explainer = shap.TreeExplainer(model, bg_data)

def evaluate_transaction(amount, distance_to_previous):
    features = pd.DataFrame([[amount, distance_to_previous]], columns=['amount', 'distanceToPrevious'])
    
    # Predict
    is_fraud_pred = model.predict(features)[0]
    
    # Explain
    shap_values = explainer(features)
    
    # We want explanation for class 1 (fraud) if the model predicted fraud, otherwise class 0
    # Actually TreeExplainer with RF returns values for both classes (shape: [n_samples, n_features, n_classes])
    # Let's extract values for class 1 (Fraud)
    
    # Check shape of shap_values
    if len(shap_values.shape) == 3:
        sv = shap_values.values[0, :, 1] # shape [n_samples, n_features, n_classes], grab sample 0, all features, class 1
    else:
        # Some versions/models return just [n_samples, n_features]
        sv = shap_values.values[0]

    feature_names = features.columns
    
    explanation = []
    if is_fraud_pred:
        explanation.append("Transaction flagged as FRAUD.")
        for name, val in zip(feature_names, sv):
            if val > 0:
                explanation.append(f"High {name} contributed to this decision (SHAP impact: {val:.2f}).")
    else:
        explanation.append("Transaction is considered SAFE.")
        for name, val in zip(feature_names, sv):
            if val < 0:
                explanation.append(f"Normal {name} lowered the risk (SHAP impact: {val:.2f}).")
                
    return {
        "isFraud": bool(is_fraud_pred),
        "explanation": " ".join(explanation)
    }
