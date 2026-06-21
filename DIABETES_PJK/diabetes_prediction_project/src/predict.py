import pandas as pd
import joblib
import os

COLUMNS = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

def load_pipeline(model_path='models/diabetes_model.pkl', scaler_path='models/scaler.pkl'):
    """Loads the trained model and scaler"""
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def predict_single_patient(patient_data: dict, model_path='models/diabetes_model.pkl', scaler_path='models/scaler.pkl'):
    """
    1. Loads model/scaler
    2. Converts dict to DataFrame
    3. Triggers inference
    4. Returns proba & prediction tag
    """
    try:
        model, scaler = load_pipeline(model_path, scaler_path)
    except Exception as e:
        return {"error": f"Failed to load model pipeline: {str(e)}"}
        
    df = pd.DataFrame([patient_data], columns=COLUMNS)
    X_scaled = scaler.transform(df)
    
    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0][1] if hasattr(model, 'predict_proba') else None
    
    risk_label = "High Risk of Diabetes" if prediction == 1 else "Low Risk of Diabetes"
    
    return {
        "prediction": risk_label,
        "probability": probability,
        "class": int(prediction)
    }

if __name__ == "__main__":
    # Test execution
    test_patient = {
        'Pregnancies': 2,
        'Glucose': 150,
        'BloodPressure': 70,
        'SkinThickness': 30,
        'Insulin': 100,
        'BMI': 35.0,
        'DiabetesPedigreeFunction': 0.5,
        'Age': 45
    }
    
    m_path = 'models/diabetes_model.pkl' if os.path.exists('models/diabetes_model.pkl') else '../models/diabetes_model.pkl'
    s_path = 'models/scaler.pkl' if os.path.exists('models/scaler.pkl') else '../models/scaler.pkl'
    
    result = predict_single_patient(test_patient, model_path=m_path, scaler_path=s_path)
    
    print("User Input:")
    for k, v in test_patient.items():
        print(f"{k}: {v}")
    
    print("\nSystem Output:")
    print(f"Prediction: {result.get('prediction')}")
    if result.get('probability') is not None:
         print(f"Probability: {result.get('probability'):.2f}")
