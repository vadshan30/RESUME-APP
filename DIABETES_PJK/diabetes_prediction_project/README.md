# Diabetes Risk Prediction System using Machine Learning 🩺

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)

## 📖 Project Description
The **Diabetes Risk Prediction System** is a complete, end-to-end Machine Learning web application designed to predict whether a patient is at risk of developing diabetes based on specific medical diagnostic measurements. 

By taking in patient vitals (like Glucose, BMI, Age, and Insulin levels), the underlying classification algorithm computes a probability percentage mapping to either a "High Risk" or "Low Risk" outcome. This helps surface diagnostic insights interactively using a modern web interface.

---

## ✨ Project Features
- **Data preprocessing**: Standardized scaling and median substitution for robust datasets.
- **Multiple ML models**: Automated training across Logistic Regression, Random Forest, Decision Tree, and Support Vector Machine. 
- **Model comparison**: Dynamically picks the best model based on generalized hold-out accuracy scoring.
- **Probability prediction**: Outputs distinct percentage values, not just binary classifications.
- **Interactive Streamlit UI**: A clean, modern, wide-layout interface presenting instantaneous results.
- **Data visualization**: Seaborn and MatPlotlib integration allowing the patient metric to be plotted contextually against historical diagnostic datasets.

---

## 5. Model Performance
The standard pipeline trains and evaluates four primary algorithms. The best performing model is dynamically picked based on its Evaluation Accuracy and saved to `models/diabetes_model.pkl`.

### 🏆 Model Comparison Table
| Model | Accuracy Score |
| :--- | :--- |
| **Logistic Regression (Best)** | **0.75** |
| Random Forest | 0.73 |
| Support Vector Machine (SVM) | 0.74 |
| Decision Tree | 0.71 |

- **Best Model Picked:** Logistic Regression
- Detailed Evaluation metrics (Accuracy, F1, Precision, Recall, Confusion Matrix) are displayed when running `python src/evaluate_model.py`.

---

## 📊 Dataset Information
The model is trained utilizing the **[Pima Indians Diabetes Dataset](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database)** originally from the National Institute of Diabetes and Digestive and Kidney Diseases. All patients in this database are females at least 21 years old of Pima Indian heritage.

### Features
| Input Parameter | Description |
| :--- | :--- |
| **Pregnancies** | Number of times pregnant |
| **Glucose** | Plasma glucose concentration a 2 hours in an oral glucose tolerance test |
| **BloodPressure** | Diastolic blood pressure (mm Hg) |
| **SkinThickness** | Triceps skin fold thickness (mm) |
| **Insulin** | 2-Hour serum insulin (mu U/ml) |
| **BMI** | Body mass index (weight in kg/(height in m)^2) |
| **DiabetesPedigreeFunction** | Diabetes pedigree function (genetic risk measurement) |
| **Age** | Age (in years) |
| **Outcome (Target)** | Class variable (0: Non-Diabetic / Low Risk, 1: Diabetic / High Risk) |

---

## 🚀 Installation Guide

Run the following commands to install and start the web application on your local machine:

1. **Clone the repository:**
```bash
git clone <repository-url>
cd diabetes_prediction_project
```

2. **Install all required dependencies:**
```bash
pip install -r requirements.txt
```

---

## ⚡ Run Instructions

To boot up the Streamlit User Interface, execute either of the following commands from the project root:

```bash
python main.py
```
**or**
```bash
streamlit run app/app.py
```

*The application will automatically launch on your `localhost:8501` network.*

---

## 🔬 Example Prediction

| Input Matrix | Output Result |
| :--- | :--- |
| **Pregnancies:** 2<br>**Glucose:** 150<br>**BMI:** 35<br>**Age:** 45 | **Prediction:** High Risk of Diabetes<br>**Probability Score:** 0.82 |

---

## 📷 Screenshots Section

*Below are UI visualizations representing data logic & results.*

### 🖥️ Streamlit UI
![Streamlit Application Interface Placeholder](docs/ui_placeholder.png)

### 📈 Analytical Charts
![Visual Correlation Data Placeholder](docs/chart_placeholder.png)

### ✅ Prediction Results
![Probability Score Output Placeholder](docs/prediction_placeholder.png)

---
> *Built for rapid medical insights using Python & Streamlit.*
