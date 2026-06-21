import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib
import os
from data_preprocessing import load_data, preprocess_data

def train_and_compare_models(X_train, X_test, y_train, y_test):
    """
    Train Logistic Regression, Random Forest, Decision Tree, Support Vector Machine.
    Compare using Accuracy to pick the best.
    """
    models = {
        'Logistic Regression': LogisticRegression(random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Support Vector Machine': SVC(probability=True, random_state=42)
    }
    
    best_model = None
    best_accuracy = 0
    best_model_name = ""
    
    results = {}
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        results[name] = acc
        print(f"{name} Accuracy: {acc:.4f}")
        
        if acc > best_accuracy:
            best_accuracy = acc
            best_model = model
            best_model_name = name
            
    print(f"\nBest Model: {best_model_name} with Accuracy: {best_accuracy:.4f}")
    return best_model, best_model_name, results

def save_model(model, filepath='models/diabetes_model.pkl'):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(model, filepath)
    print(f"Model successfully saved to {filepath}")

if __name__ == "__main__":
    # Ensure working directory is correctly handled if executing from 'src'
    dataset_path = 'data/diabetes.csv'
    if not os.path.exists(dataset_path):
        dataset_path = '../data/diabetes.csv'
        
    scaler_path = 'models/scaler.pkl'
    if not os.path.exists('models'):
        scaler_path = '../models/scaler.pkl'
        
    df = load_data(dataset_path)
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df, save_scaler_path=scaler_path)
    
    print("\nTraining Models...")
    best_model, best_name, _ = train_and_compare_models(X_train, X_test, y_train, y_test)
    
    model_path = 'models/diabetes_model.pkl'
    if not os.path.exists('models'):
        model_path = '../models/diabetes_model.pkl'
        
    save_model(best_model, model_path)
