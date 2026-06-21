import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from data_preprocessing import load_data, preprocess_data

def evaluate_model(model, X_test, y_test):
    """
    Evaluate trained models returning standard classification metrics.
    """
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    metrics = {
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1
    }
    
    print("--- Model Evaluation ---")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")
        
    return metrics, y_pred, y_prob

def plot_confusion_matrix(y_test, y_pred, save_path='notebooks/confusion_matrix.png'):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['No Diabetes', 'Diabetes'], yticklabels=['No Diabetes', 'Diabetes'])
    plt.title('Confusion Matrix')
    plt.ylabel('True Class')
    plt.xlabel('Predicted Class')
    plt.savefig(save_path)
    plt.close()
    
def plot_roc_curve(y_test, y_prob, save_path='notebooks/roc_curve.png'):
    if y_prob is None:
        print("Model doesn't support probability predictions for ROC.")
        return
        
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(6, 4))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.savefig(save_path)
    plt.close()

if __name__ == "__main__":
    dataset_path = 'data/diabetes.csv' if os.path.exists('data/diabetes.csv') else '../data/diabetes.csv'
    model_path = 'models/diabetes_model.pkl' if os.path.exists('models/diabetes_model.pkl') else '../models/diabetes_model.pkl'
    scaler_path = 'models/scaler.pkl' if os.path.exists('models/scaler.pkl') else '../models/scaler.pkl'
    
    df = load_data(dataset_path)
    _, X_test, _, y_test, _ = preprocess_data(df, save_scaler_path=scaler_path)
    
    try:
        model = joblib.load(model_path)
        metrics, y_pred, y_prob = evaluate_model(model, X_test, y_test)
        
        cm_path = 'notebooks/confusion_matrix.png' if os.path.exists('notebooks') else '../notebooks/confusion_matrix.png'
        roc_path = 'notebooks/roc_curve.png' if os.path.exists('notebooks') else '../notebooks/roc_curve.png'
        
        plot_confusion_matrix(y_test, y_pred, save_path=cm_path)
        plot_roc_curve(y_test, y_prob, save_path=roc_path)
        print(f"\nEvaluation plots saved to {os.path.dirname(cm_path)} directory.")
    except Exception as e:
        print(f"Error evaluating model: {e}")
