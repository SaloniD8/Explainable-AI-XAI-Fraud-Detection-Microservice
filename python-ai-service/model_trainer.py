import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

def generate_mock_data(n_samples=5000):
    np.random.seed(42)
    # Features: amount, distance_to_previous
    # Fraud rule: high amount and high distance is more likely fraud
    amounts = np.random.exponential(scale=100, size=n_samples)
    distances = np.random.exponential(scale=50, size=n_samples)
    
    # Let's say if amount > 500 and distance > 200, high chance of fraud
    is_fraud = ((amounts > 400) & (distances > 150)) | (amounts > 1000)
    
    # Add some noise
    noise = np.random.choice([True, False], size=n_samples, p=[0.05, 0.95])
    is_fraud = is_fraud ^ noise
    
    df = pd.DataFrame({
        'amount': amounts,
        'distanceToPrevious': distances,
        'isFraud': is_fraud
    })
    return df

def train_and_save_model():
    df = generate_mock_data()
    X = df[['amount', 'distanceToPrevious']]
    y = df['isFraud']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"Model trained with accuracy: {accuracy:.2f}")
    
    joblib.dump(model, 'fraud_model.pkl')
    # Also save a sample for SHAP background
    X_train.sample(100, random_state=42).to_csv('background_data.csv', index=False)
    print("Model saved to fraud_model.pkl")

if __name__ == "__main__":
    train_and_save_model()
