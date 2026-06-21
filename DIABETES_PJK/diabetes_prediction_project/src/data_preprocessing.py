import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

COLUMNS = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']

def load_data(filepath='data/diabetes.csv'):
    """Load dataset from CSV and display basic info"""
    # Dataset doesn't have headers, so we read it by assigning the specific column names
    df = pd.read_csv(filepath, names=COLUMNS)
    print("Dataset Info:")
    print(df.info())
    print("\nDataset Description:")
    print(df.describe())
    return df

def preprocess_data(df, test_size=0.2, random_state=42, save_scaler_path='models/scaler.pkl'):
    """
    Handle missing values, scale features, and split dataset.
    """
    # In Pima Indians dataset, 0 means missing value for certain biological metrics
    columns_with_zero_as_missing = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    for col in columns_with_zero_as_missing:
        df[col] = df[col].replace(0, np.nan)
        # Fill missing values with median of the column
        df[col] = df[col].fillna(df[col].median())
        
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    
    # Split Dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler for inference
    os.makedirs(os.path.dirname(save_scaler_path), exist_ok=True)
    joblib.dump(scaler, save_scaler_path)
    print(f"Scaler saved to {save_scaler_path}")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

if __name__ == "__main__":
    dataset_path = 'data/diabetes.csv' if os.path.exists('data/diabetes.csv') else '../data/diabetes.csv'
    scaler_path = 'models/scaler.pkl' if os.path.exists('models') else '../models/scaler.pkl'
    
    df = load_data(dataset_path)
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df, save_scaler_path=scaler_path)
    print("\\nData Preprocessing Complete.")
    print("X_train shape:", X_train.shape)
    print("X_test shape:", X_test.shape)
