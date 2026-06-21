import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import sys
import time

# Add src to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from predict import predict_single_patient

# Page Configuration
st.set_page_config(
    page_title="Diabetes Risk Prediction System", 
    layout="wide", 
    page_icon="🩺",
    initial_sidebar_state="expanded"
)

# Custom CSS for a professional medical dashboard look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.8rem;
        color: #0f4c81;
        font-weight: 700;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        margin-top: 5px;
        margin-bottom: 2rem;
    }
    
    /* Input Panel styling */
    .css-1d391kg {
        background-color: #f8fafc;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }
    
    /* Result Card Styling */
    .prediction-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin-bottom: 30px;
        border-top: 5px solid #0f4c81;
    }
    
    .prediction-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 10px;
    }
    
    .prediction-high {
        color: #ef4444;
        font-size: 2.2rem;
        font-weight: 700;
    }
    
    .prediction-low {
        color: #10b981;
        font-size: 2.2rem;
        font-weight: 700;
    }
    
    /* Button Styling */
    div[data-testid="stFormSubmitButton"] > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Primary Predict Button */
    div[data-testid="column"]:nth-child(1) div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #0f4c81 0%, #1e3a8a 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 6px rgba(15, 76, 129, 0.3);
    }
    div[data-testid="column"]:nth-child(1) div[data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(15, 76, 129, 0.4);
    }
    
    /* Reset Button */
    div[data-testid="column"]:nth-child(2) div[data-testid="stFormSubmitButton"] > button {
        background-color: transparent;
        color: #64748b;
        border: 1px solid #cbd5e1;
    }
    div[data-testid="column"]:nth-child(2) div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #f1f5f9;
        color: #334155;
    }
    
    /* Ghost Button */
    div[data-testid="column"]:nth-child(3) div[data-testid="stFormSubmitButton"] > button {
        background-color: transparent;
        color: #0f4c81;
        border: none;
    }
    div[data-testid="column"]:nth-child(3) div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #e2e8f0;
    }
    
    /* Metrics Cards */
    .metric-card {
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f4c81;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Circular Gauge CSS */
    .flex-wrapper {
      display: flex;
      justify-content: center;
      margin: 20px 0;
    }
    .single-chart {
      width: 33%;
      justify-content: space-around ;
    }
    .circular-chart {
      display: block;
      margin: 0 auto;
      max-width: 80%;
      max-height: 250px;
    }
    .circle-bg {
      fill: none;
      stroke: #eee;
      stroke-width: 3.8;
    }
    .circle {
      fill: none;
      stroke-width: 2.8;
      stroke-linecap: round;
      animation: progress 1s ease-out forwards;
    }
    @keyframes progress {
      0% {
        stroke-dasharray: 0 100;
      }
    }
    .circular-chart.green .circle {
      stroke: #10b981;
    }
    .circular-chart.orange .circle {
      stroke: #f59e0b;
    }
    .circular-chart.red .circle {
      stroke: #ef4444;
    }
    .percentage {
      fill: #334155;
      font-family: 'Inter', sans-serif;
      font-size: 0.5em;
      text-anchor: middle;
      font-weight: 700;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
        color: #94a3b8;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_data():
    dataset_path = 'data/diabetes.csv' if os.path.exists('data/diabetes.csv') else '../data/diabetes.csv'
    COLUMNS = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    df = pd.read_csv(dataset_path, names=COLUMNS)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    df = None

# Title Section
st.markdown('<p class="main-header">🩺 Diabetes Risk Prediction System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Machine Learning Based Health Risk Prediction</p>', unsafe_allow_html=True)

# Layout Configuration
col1, col2 = st.columns([1.2, 2.0], gap="large")

# ----------------- Left Panel: Inputs -----------------
with col1:
    st.markdown("### 📋 Patient Medical Profile")
    st.markdown("Enter patient metrics below to assess risk.")
    
    with st.form("medical_form"):
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=2, step=1, help="Number of times pregnant.")
        glucose = st.slider("Glucose Level (mg/dL)", min_value=0.0, max_value=300.0, value=150.0, step=1.0, help="Plasma glucose concentration a 2 hours in an oral glucose tolerance test. Normal < 140 mg/dL.")
        blood_pressure = st.slider("Blood Pressure (mm Hg)", min_value=0.0, max_value=200.0, value=70.0, step=1.0, help="Diastolic blood pressure. Normal is typically < 80 mm Hg.")
        skin_thickness = st.slider("Skin Thickness (mm)", min_value=0.0, max_value=100.0, value=30.0, step=1.0, help="Triceps skin fold thickness.")
        insulin = st.slider("Insulin (mu U/ml)", min_value=0.0, max_value=900.0, value=100.0, step=1.0, help="2-Hour serum insulin.")
        bmi = st.slider("BMI (kg/m²)", min_value=10.0, max_value=70.0, value=35.0, step=0.1, help="Body mass index. Normal: 18.5 - 24.9.")
        dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=2.5, value=0.5, step=0.01, help="Genetic risk score based on family history.")
        age = st.slider("Age (years)", min_value=0, max_value=120, value=45, step=1, help="Age of the patient.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Action Buttons
        btn_col1, btn_col2, btn_col3 = st.columns([1.2, 1, 1])
        with btn_col1:
            submit_btn = st.form_submit_button("Predict Diabetes Risk")
        with btn_col2:
            reset_btn = st.form_submit_button("Reset Inputs")
        with btn_col3:
            model_btn = st.form_submit_button("ℹ️ Model Info")

# Helper function to generate SVG circular gauge
def render_circular_gauge(probability):
    prob_percent = probability * 100
    if prob_percent <= 30:
        color_class = "green"
    elif prob_percent <= 60:
        color_class = "orange"
    else:
        color_class = "red"
        
    gauge_html = f'''
    <div class="flex-wrapper">
      <div class="single-chart">
        <svg viewBox="0 0 36 36" class="circular-chart {color_class}">
          <path class="circle-bg"
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
          />
          <path class="circle"
            stroke-dasharray="{prob_percent}, 100"
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
          />
          <text x="18" y="20.35" class="percentage">{prob_percent:.1f}%</text>
        </svg>
      </div>
    </div>
    '''
    return gauge_html

# ----------------- Right Panel: Output & Visuals -----------------
with col2:
    if model_btn:
        st.markdown("### 🤖 Model Information")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown('<div class="metric-card"><div class="metric-label">Algorithm Used</div><div class="metric-value">Logistic Regression</div></div>', unsafe_allow_html=True)
        with m_col2:
            st.markdown('<div class="metric-card"><div class="metric-label">Model Accuracy</div><div class="metric-value">~76%</div></div>', unsafe_allow_html=True)
        with m_col3:
            st.markdown('<div class="metric-card"><div class="metric-label">Dataset Records</div><div class="metric-value">768 Patients</div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("The system selects the best performing model automatically. The Pima Indians Diabetes Dataset was utilized for training and validation.")
        
        with st.expander("📊 Dataset Summary Statistics"):
            st.dataframe(df.describe().T, use_container_width=True)

    elif reset_btn:
        st.info("Input parameters reset. Please enter new patient details.")
        
    elif submit_btn:
        # Prediction Logic payload
        input_data = {
            'Pregnancies': pregnancies,
            'Glucose': glucose,
            'BloodPressure': blood_pressure,
            'SkinThickness': skin_thickness,
            'Insulin': insulin,
            'BMI': bmi,
            'DiabetesPedigreeFunction': dpf,
            'Age': age
        }
        
        m_path = 'models/diabetes_model.pkl' if os.path.exists('models/diabetes_model.pkl') else '../models/diabetes_model.pkl'
        s_path = 'models/scaler.pkl' if os.path.exists('models/scaler.pkl') else '../models/scaler.pkl'
        
        try:
            with st.spinner('Analyzing patient metrics...'):
                time.sleep(1) # Simulated loading animation feel
                results = predict_single_patient(input_data, m_path, s_path)
            
            if "error" in results:
                st.error(f"Prediction System Error: {results['error']}")
            else:
                prob = results["probability"]
                pred_label = results["prediction"]
                prediction_class = "prediction-low" if results["class"] == 0 else "prediction-high"
                
                # Render Prediction Card
                st.markdown(f"""
                <div class="prediction-card">
                    <div class="prediction-title">Prediction Result</div>
                    <div class="{prediction_class}">{pred_label}</div>
                    <div style="font-size: 1.1rem; color: #64748b; margin-top: 15px;">Diabetes Probability Score</div>
                    {render_circular_gauge(prob)}
                </div>
                """, unsafe_allow_html=True)
                
                # --- Visualizations ---
                st.markdown("### 🔬 Data Insights & Context")
                
                sns.set_theme(style="whitegrid")
                
                tab1, tab2, tab3 = st.tabs(["Age vs Diabetes", "Glucose vs Outcome", "Correlation Heatmap"])
                
                with tab1:
                    st.markdown("**Age Distribution of Diabetic vs Non-Diabetic Patients**")
                    fig1, ax1 = plt.subplots(figsize=(10, 4))
                    sns.kdeplot(data=df, x="Age", hue="Outcome", fill=True, common_norm=False, palette=["#10b981", "#ef4444"], alpha=0.5, ax=ax1)
                    ax1.axvline(x=age, color='#334155', linestyle='--', lw=2.5, label=f'Patient Age: {age}')
                    ax1.legend(title='Outcome', labels=['Diabetic', 'Non-Diabetic', f'Patient ({age})'])
                    ax1.set_xlabel('Age (years)')
                    ax1.set_ylabel('Density')
                    st.pyplot(fig1)
                    
                with tab2:
                    st.markdown("**Glucose Levels Distribution by Outcome**")
                    fig2, ax2 = plt.subplots(figsize=(10, 4))
                    sns.boxplot(x="Outcome", y="Glucose", data=df, palette=["#10b981", "#ef4444"], ax=ax2)
                    ax2.scatter(x=results["class"], y=glucose, color='#f59e0b', s=250, marker='*', edgecolor='black', linewidth=1.5, zorder=10, label="Patient")
                    ax2.set_xticklabels(['Low Risk', 'High Risk'])
                    ax2.set_ylabel('Glucose Level (mg/dL)')
                    ax2.legend()
                    st.pyplot(fig2)

                with tab3:
                    st.markdown("**Dataset Feature Correlation Matrix**")
                    fig3, ax3 = plt.subplots(figsize=(10, 6))
                    corr = df.corr()
                    mask = np.triu(np.ones_like(corr, dtype=bool))
                    sns.heatmap(corr, mask=mask, annot=True, cmap="Blues", fmt=".2f", vmin=-1, vmax=1, ax=ax3, square=True, linewidths=.5, cbar_kws={"shrink": .8})
                    st.pyplot(fig3)
                
        except Exception as e:
            st.error(f"System faced a runtime error during prediction: {str(e)}")
            
    else:
        # Default empty state
        st.markdown(f"""
        <div class="prediction-card" style="padding: 50px;">
            <div style="font-size: 4rem; margin-bottom: 20px;">🔬</div>
            <div class="prediction-title">Awaiting Patient Data</div>
            <div style="color: #64748b;">Please enter the patient's medical profile on the left and click "Predict Diabetes Risk" to generate an assessment.</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📊 Dataset Summary Statistics"):
            st.dataframe(df.describe().T, use_container_width=True)

# Footer
st.markdown('<div class="footer">768 patients | Model accuracy ~76% | Built with Python, Scikit-Learn, and Streamlit</div>', unsafe_allow_html=True)

