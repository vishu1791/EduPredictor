import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# --------------------------- 
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Student Performance AI", 
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------- 
# Custom CSS Styling
# ---------------------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit Elements */
    /* #MainMenu {visibility: hidden;} */
    /* header {visibility: hidden;} */
    footer {visibility: hidden;}
    
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Main Container */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Header Styling */
    .header-container {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .header-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 1s ease-out;
    }
    
    .header-subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        opacity: 0.9;
        animation: fadeInUp 1s ease-out 0.3s both;
    }
    
    /* Individual Prediction Header */
    .individual-header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
    }
    
    .individual-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .individual-subtitle {
        font-size: 1.1rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Upload Section */
    .upload-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
    }
    
    .upload-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        animation: bounce 2s infinite;
    }
    
    /* Form Styling */
    .form-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .form-section {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 20px rgba(67, 233, 123, 0.3);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Prediction Result Card */
    .prediction-card {
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        color: white;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        animation: slideInUp 0.6s ease-out;
    }
    
    .prediction-pass {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        box-shadow: 0 15px 35px rgba(67, 233, 123, 0.4);
    }
    
    .prediction-fail {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.4);
    }
    
    .prediction-result {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .prediction-confidence {
        font-size: 1.5rem;
        font-weight: 300;
        opacity: 0.9;
        margin-bottom: 1rem;
    }
    
    /* Success/Error Messages */
    .success-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        animation: slideInRight 0.5s ease-out;
    }
    
    .error-message {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #d63384;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        animation: shake 0.5s ease-out;
    }
    
    /* Feedback Section */
    .feedback-container {
        background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(161, 140, 209, 0.3);
    }
    
    .feedback-title {
        color: white;
        font-size: 2rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .feedback-content {
        color: white;
        font-size: 1.1rem;
        line-height: 1.6;
        text-align: center;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Navigation Buttons */
    .nav-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        margin: 0.5rem 0;
        width: 100%;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .nav-button.active {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        box-shadow: 0 8px 25px rgba(67, 233, 123, 0.4);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes shake {
        0%, 100% {
            transform: translateX(0);
        }
        10%, 30%, 50%, 70%, 90% {
            transform: translateX(-5px);
        }
        20%, 40%, 60%, 80% {
            transform: translateX(5px);
        }
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* DataFrames */
    .stDataFrame {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Feature Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #666;
        line-height: 1.6;
    }
    
    /* Input Field Styling */
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    /* Responsive Design */
    @media (max-width: 1200px) {
        .main-container, .header-container, .form-container, .upload-section, .feedback-container, .feature-card {
            padding: 1.2rem;
            margin: 0.5rem;
        }
        .header-title {
            font-size: 2.5rem;
        }
        .individual-title {
            font-size: 1.7rem;
        }
    }
    @media (max-width: 900px) {
        .main-container, .header-container, .form-container, .upload-section, .feedback-container, .feature-card {
            padding: 1rem;
            margin: 0.3rem;
        }
        .header-title {
            font-size: 2rem;
        }
        .individual-title {
            font-size: 1.3rem;
        }
        .metric-card {
            font-size: 0.95rem;
            padding: 1rem;
        }
        .feature-title {
            font-size: 1rem;
        }
    }
    @media (max-width: 600px) {
        .main-container, .header-container, .form-container, .upload-section, .feedback-container, .feature-card {
            padding: 0.5rem;
            margin: 0.1rem;
            border-radius: 10px;
        }
        .header-title {
            font-size: 1.3rem;
        }
        .header-subtitle, .individual-subtitle, .feature-desc, .feedback-content {
            font-size: 0.9rem;
        }
        .individual-title {
            font-size: 1rem;
        }
        .metric-card {
            font-size: 0.85rem;
            padding: 0.7rem;
            border-radius: 8px;
        }
        .prediction-result {
            font-size: 1.5rem;
        }
        .prediction-confidence {
            font-size: 1rem;
        }
        .feature-title {
            font-size: 0.95rem;
        }
        .feature-icon {
            font-size: 1.5rem;
        }
        .stButton > button, .stDownloadButton > button, .nav-button {
            padding: 0.5rem 1rem;
            font-size: 0.95rem;
        }
        .stDataFrame {
            font-size: 0.85rem;
        }
    }
    /* Stack columns vertically on small screens */
    @media (max-width: 900px) {
        .block-container .css-1lcbmhc, /* Streamlit columns class (may change in future versions) */
        .block-container .stColumns {
            flex-direction: column !important;
        }
        .stColumn {
            width: 100% !important;
            min-width: 0 !important;
        }
    }
    /* Make dataframes and charts scrollable on small screens */
    @media (max-width: 600px) {
        .stDataFrame, .stTable, .stPlotlyChart, .stAltairChart, .stVegaLiteChart {
            overflow-x: auto !important;
            max-width: 100vw !important;
        }
    }
    /* Hide the Streamlit Deploy button */
    [data-testid="stDeployButton"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------- 
# Load Model and Scaler
# ---------------------------
@st.cache_resource
def load_models():
    try:
        model = joblib.load("student_model.pkl")
        scaler = joblib.load("scaler.pkl")
        return model, scaler
    except FileNotFoundError:
        st.error("⚠️ Model files not found. Please ensure 'student_model.pkl' and 'scaler.pkl' are in the same directory.")
        return None, None

model, scaler = load_models()

# --------------------------- 
# Helper Functions
# ---------------------------
def generate_feedback(attendance, internal_marks, study_hours, participation, extracurricular):
    feedback = []
    
    if attendance < 75:
        feedback.append("🎯 Your attendance is below average. Try to attend more classes regularly.")
    elif attendance >= 90:
        feedback.append("⭐ Excellent attendance! Keep it up.")
    else:
        feedback.append("👍 Good attendance. Try to maintain consistency.")
    
    if internal_marks < 60:
        feedback.append("📚 Work on improving your internal scores through assignments and tests.")
    elif internal_marks >= 85:
        feedback.append("🏆 Outstanding internal performance!")
    else:
        feedback.append("📈 Good internal marks. Keep pushing for excellence.")
    
    if study_hours < 5:
        feedback.append("⏰ Consider increasing your weekly study hours to better understand the concepts.")
    elif study_hours > 12:
        feedback.append("💪 You're studying well. Ensure you're also taking breaks and staying healthy!")
    else:
        feedback.append("⚖️ Good balance in study hours. Maintain this consistency.")
    
    if participation == 0:
        feedback.append("🗣️ Try to engage more in class discussions to improve your understanding.")
    else:
        feedback.append("👏 Great participation in class! This helps reinforce learning.")
    
    if extracurricular == 1:
        feedback.append("🎨 Excellent job managing studies with extracurricular activities! This shows good time management.")
    else:
        feedback.append("🌟 Consider joining some extracurricular activities for holistic development.")
    
    return " ".join(feedback)

def create_performance_chart(df):
    """Create a beautiful performance visualization"""
    fig = go.Figure()
    
    # Add Pass/Fail distribution
    pass_count = len(df[df['Prediction'] == 'Pass'])
    fail_count = len(df[df['Prediction'] == 'Fail'])
    
    fig.add_trace(go.Bar(
        x=['Pass', 'Fail'],
        y=[pass_count, fail_count],
        marker_color=['#43e97b', '#ff6b6b'],
        text=[pass_count, fail_count],
        textposition='auto',
        name='Students'
    ))
    
    fig.update_layout(
        title={
            'text': 'Student Performance Distribution',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#333'}
        },
        xaxis_title='Result',
        yaxis_title='Number of Students',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif"),
        height=400
    )
    
    return fig

def create_metrics_dashboard(df):
    """Create metrics dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{len(df)}</div>
            <div class="metric-label">Total Students</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pass_rate = (len(df[df['Prediction'] == 'Pass']) / len(df) * 100)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{pass_rate:.1f}%</div>
            <div class="metric-label">Pass Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_attendance = df['Attendance'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{avg_attendance:.1f}%</div>
            <div class="metric-label">Avg Attendance</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_internal = df['InternalMarks'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{avg_internal:.1f}</div>
            <div class="metric-label">Avg Internal Marks</div>
        </div>
        """, unsafe_allow_html=True)

def create_individual_visualization(attendance, internal_marks, study_hours, participation, extracurricular, prediction, confidence):
    """Create visualization for individual student"""
    
    # Create radar chart for student profile
    categories = ['Attendance', 'Internal Marks', 'Study Hours', 'Participation', 'Extracurricular']
    
    # Normalize values for radar chart
    values = [
        attendance,
        internal_marks,
        study_hours * 10,  # Scale study hours
        participation * 100,  # Scale participation
        extracurricular * 100  # Scale extracurricular
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Profile',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title={
            'text': 'Your Academic Profile',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#333'}
        },
        font=dict(family="Poppins, sans-serif"),
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# --------------------------- 
# Navigation Setup
# ---------------------------
def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'batch_prediction'

# --------------------------- 
# Individual Prediction Page
# ---------------------------
def individual_prediction_page():
    # Header for individual prediction
    st.markdown("""
    <div class="individual-header">
        <div class="individual-title">👤 Individual Prediction</div>
        <div class="individual-subtitle">Get personalized performance prediction and feedback</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if models are loaded
    if model is None or scaler is None:
        st.stop()
    
    # Create form container
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    # Input form
    with st.form("student_form"):
        st.markdown("### 📝 Enter Your Academic Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            attendance = st.number_input(
                "📊 Attendance Percentage",
                min_value=0.0,
                max_value=100.0,
                value=80.0,
                step=0.1,
                help="Enter your overall attendance percentage"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            internal_marks = st.number_input(
                "📚 Internal Assessment Marks",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                step=0.1,
                help="Enter your internal assessment marks"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            study_hours = st.number_input(
                "⏰ Study Hours Per Week",
                min_value=0.0,
                max_value=40.0,
                value=8.0,
                step=0.5,
                help="Enter your weekly study hours"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            participation = st.selectbox(
                "🗣️ Class Participation",
                options=["No", "Yes"],
                index=1,
                help="Do you actively participate in class discussions?"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            extracurricular = st.selectbox(
                "🎨 Extracurricular Activities",
                options=["No", "Yes"],
                index=0,
                help="Are you involved in extracurricular activities?"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        st.markdown('<br>', unsafe_allow_html=True)
        submitted = st.form_submit_button("🔮 Get My Prediction", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process prediction
    if submitted:
        with st.spinner("🔄 Analyzing your academic profile..."):
            # Prepare data
            participation_val = 1 if participation == "Yes" else 0
            extracurricular_val = 1 if extracurricular == "Yes" else 0
            
            # Create feature array
            X = [[attendance, internal_marks, study_hours, participation_val, extracurricular_val]]
            X_scaled = scaler.transform(X)
            
            # Make prediction
            prediction = model.predict(X_scaled)[0]
            probability = model.predict_proba(X_scaled)[0]
            confidence = max(probability) * 100
            
            # Generate feedback
            feedback = generate_feedback(attendance, internal_marks, study_hours, participation_val, extracurricular_val)
            
            # Display results
            prediction_text = "Pass" if prediction == 1 else "Fail"
            prediction_class = "prediction-pass" if prediction == 1 else "prediction-fail"
            prediction_emoji = "🎉" if prediction == 1 else "⚠️"
            
            # Prediction result card
            st.markdown(f"""
            <div class="prediction-card {prediction_class}">
                <div class="prediction-result">{prediction_emoji} {prediction_text}</div>
                <div class="prediction-confidence">Confidence: {confidence:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Feedback section
            st.markdown(f"""
            <div class="feedback-container">
                <div class="feedback-title">💡 Personalized Feedback</div>
                <div class="feedback-content">{feedback}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Visualization
            col1, col2 = st.columns(2)
            
            with col1:
                # Individual radar chart
                fig = create_individual_visualization(
                    attendance, internal_marks, study_hours, 
                    participation_val, extracurricular_val, 
                    prediction_text, confidence
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Performance metrics
                st.markdown("### 📊 Your Academic Metrics")
                
                metrics_data = {
                    'Metric': ['Attendance', 'Internal Marks', 'Study Hours/Week', 'Participation', 'Extracurricular'],
                    'Your Score': [f"{attendance}%", f"{internal_marks}", f"{study_hours}h", participation, extracurricular],
                    'Status': [
                        "✅ Good" if attendance >= 75 else "❌ Needs Improvement",
                        "✅ Good" if internal_marks >= 60 else "❌ Needs Improvement",
                        "✅ Good" if study_hours >= 5 else "❌ Needs Improvement",
                        "✅ Good" if participation == "Yes" else "❌ Needs Improvement",
                        "✅ Good" if extracurricular == "Yes" else "⚪ Optional"
                    ]
                }
                
                metrics_df = pd.DataFrame(metrics_data)
                st.dataframe(metrics_df, use_container_width=True, hide_index=True)
            
            # Improvement suggestions
            st.markdown("### 🚀 Improvement Suggestions")
            
            suggestions = []
            if attendance < 75:
                suggestions.append("📈 **Improve Attendance**: Aim for at least 80% attendance for better performance")
            if internal_marks < 60:
                suggestions.append("📚 **Focus on Internal Assessments**: Complete assignments on time and prepare well for internal tests")
            if study_hours < 5:
                suggestions.append("⏰ **Increase Study Time**: Dedicate at least 5-8 hours per week for effective learning")
            if participation == "No":
                suggestions.append("🗣️ **Participate More**: Engage actively in class discussions and ask questions")
            if extracurricular == "No":
                suggestions.append("🎨 **Consider Extracurricular**: Join clubs or activities for holistic development")
            
            if suggestions:
                for suggestion in suggestions:
                    st.markdown(f"- {suggestion}")
            else:
                st.markdown("🌟 **Great job!** You're doing well in all areas. Keep up the excellent work!")

# --------------------------- 
# Batch Prediction Page (Original)
# ---------------------------
def batch_prediction_page():
    # Header Section
    st.markdown("""
    <div class="header-container">
        <div class="header-title">🎓 Student Performance AI</div>
        <div class="header-subtitle">Predict academic outcomes with AI-powered insights and personalized feedback</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if models are loaded
    if model is None or scaler is None:
        st.stop()
    
    # Features Section
    st.markdown("## ✨ Key Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Prediction</div>
            <div class="feature-desc">Advanced machine learning algorithms predict student performance with high accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Visual Analytics</div>
            <div class="feature-desc">Beautiful charts and dashboards provide insights into student performance trends</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Smart Feedback</div>
            <div class="feature-desc">Personalized recommendations help students improve their academic performance</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Upload Section
    st.markdown("""
    <div class="upload-section">
        <div class="upload-icon">📁</div>
        <h2>Upload Student Dataset</h2>
        <p>Upload a CSV file containing student data to get started with predictions</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file", 
        type=["csv"],
        help="Upload a CSV file with columns: Attendance, InternalMarks, StudyHoursPerWeek, Participation, Extracurricular"
    )
    
    if uploaded_file:
        with st.spinner("🔄 Processing your data..."):
            try:
                # Load and validate data
                df = pd.read_csv(uploaded_file)
                
                required_columns = {"Attendance", "InternalMarks", "StudyHoursPerWeek", "Participation", "Extracurricular"}
                
                if not required_columns.issubset(df.columns):
                    st.markdown("""
                    <div class="error-message">
                        ❌ Upload failed! Your file must contain these columns: Attendance, InternalMarks, StudyHoursPerWeek, Participation, Extracurricular
                    </div>
                    """, unsafe_allow_html=True)
                    return
                
                # Data preprocessing
                df_processed = df.copy()
                
                # Handle different formats for Participation and Extracurricular
                if df_processed['Participation'].dtype == 'object':
                    df_processed['Participation'] = df_processed['Participation'].map({'Yes': 1, 'No': 0})
                
                if df_processed['Extracurricular'].dtype == 'object':
                    df_processed['Extracurricular'] = df_processed['Extracurricular'].map({'Yes': 1, 'No': 0})
                
                # Prepare features
                X = df_processed[["Attendance", "InternalMarks", "StudyHoursPerWeek", "Participation", "Extracurricular"]]
                X_scaled = scaler.transform(X)
                
                # Make predictions
                predictions = model.predict(X_scaled)
                probabilities = model.predict_proba(X_scaled)
                
                df_processed["Prediction"] = ["Pass" if p == 1 else "Fail" for p in predictions]
                df_processed["Confidence"] = [max(prob) * 100 for prob in probabilities]
                
                # Generate feedback for each student
                feedback_list = []
                for _, row in df_processed.iterrows():
                    feedback = generate_feedback(
                        row['Attendance'], row['InternalMarks'], row['StudyHoursPerWeek'],
                        row['Participation'], row['Extracurricular']
                    )
                    feedback_list.append(feedback)
                
                df_processed["Feedback"] = feedback_list
                
                # Success message
                st.markdown("""
                <div class="success-message">
                    ✅ Predictions completed successfully! Check out the results below.
                </div>
                """, unsafe_allow_html=True)
                
                # Metrics Dashboard
                st.markdown("## 📊 Performance Dashboard")
                create_metrics_dashboard(df_processed)
                
                # Visualization
                st.markdown("## 📈 Visual Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = create_performance_chart(df_processed)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Attendance vs Internal Marks scatter plot
                    fig2 = px.scatter(
                        df_processed, 
                        x='Attendance', 
                        y='InternalMarks',
                        color='Prediction',
                        size='StudyHoursPerWeek',
                        hover_data=['Confidence'],
                        title='Attendance vs Internal Marks',
                        color_discrete_map={'Pass': '#43e97b', 'Fail': '#ff6b6b'}
                    )
                    fig2.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Poppins, sans-serif")
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Results Table
                st.markdown("## 📋 Detailed Results")
                
                # Add color coding for predictions
                def color_predictions(val):
                    if val == 'Pass':
                        return 'background-color: #43e97b; color: white; font-weight: bold'
                    else:
                        return 'background-color: #ff6b6b; color: white; font-weight: bold'
                
                styled_df = df_processed[["Attendance", "InternalMarks", "StudyHoursPerWeek", 
                                        "Participation", "Extracurricular", "Prediction", 
                                        "Confidence", "Feedback"]].style.applymap(
                    color_predictions, subset=['Prediction']
                ).format({
                    'Confidence': '{:.1f}%',
                    'Attendance': '{:.1f}%',
                    'InternalMarks': '{:.1f}'
                })
                
                st.dataframe(styled_df, use_container_width=True, height=400)
                
                # Feedback Section
                st.markdown("""
                <div class="feedback-container">
                    <div class="feedback-title">💡 AI-Generated Insights</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show individual feedback for first 5 students
                for i in range(min(5, len(df_processed))):
                    student = df_processed.iloc[i]
                    prediction_color = "#43e97b" if student['Prediction'] == 'Pass' else "#ff6b6b"
                    
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, {prediction_color}20, {prediction_color}10);
                        padding: 1rem;
                        border-radius: 10px;
                        margin: 1rem 0;
                        border-left: 4px solid {prediction_color};
                    ">
                        <h4>Student {i+1} - {student['Prediction']} ({student['Confidence']:.1f}% confidence)</h4>
                        <p>{student['Feedback']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Download section
                st.markdown("## 📥 Download Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    csv_data = df_processed.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📊 Download Full Results (CSV)",
                        data=csv_data,
                        file_name=f"student_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime='text/csv',
                        use_container_width=True
                    )
                
                with col2:
                    # Create summary report
                    summary_report = f"""
Student Performance Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY STATISTICS:
- Total Students Analyzed: {len(df_processed)}
- Students Predicted to Pass: {len(df_processed[df_processed['Prediction'] == 'Pass'])}
- Students Predicted to Fail: {len(df_processed[df_processed['Prediction'] == 'Fail'])}
- Overall Pass Rate: {(len(df_processed[df_processed['Prediction'] == 'Pass']) / len(df_processed) * 100):.1f}%

AVERAGE METRICS:
- Average Attendance: {df_processed['Attendance'].mean():.1f}%
- Average Internal Marks: {df_processed['InternalMarks'].mean():.1f}
- Average Study Hours/Week: {df_processed['StudyHoursPerWeek'].mean():.1f}
- Students with Active Participation: {df_processed['Participation'].sum()}
- Students in Extracurricular: {df_processed['Extracurricular'].sum()}

RECOMMENDATIONS:
- Focus on improving attendance rates
- Provide additional support for students with low internal marks
- Encourage more class participation
- Promote balanced approach to studies and extracurricular activities
                    """
                    
                    st.download_button(
                        label="📄 Download Summary Report",
                        data=summary_report,
                        file_name=f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime='text/plain',
                        use_container_width=True
                    )
                
            except Exception as e:
                st.markdown(f"""
                <div class="error-message">
                    ❌ Error processing file: {str(e)}
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # Show sample data format
        st.markdown("## 📋 Sample Data Format")
        sample_data = pd.DataFrame({
            'Attendance': [85.5, 92.0, 78.5, 95.0, 67.5],
            'InternalMarks': [78, 85, 65, 92, 58],
            'StudyHoursPerWeek': [6, 8, 4, 10, 3],
            'Participation': ['Yes', 'Yes', 'No', 'Yes', 'No'],
            'Extracurricular': ['Yes', 'No', 'Yes', 'Yes', 'No']
        })
        
        st.dataframe(sample_data, use_container_width=True)
        st.info("💡 Your CSV file should have columns exactly like the sample above.")

# --------------------------- 
# Main App with Navigation
# ---------------------------
def main():
    init_session_state()
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; margin-bottom: 2rem;">
            <h2 style="color: white; margin: 0;">🎓 Navigation</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation buttons
        if st.button("👤 Individual Prediction", key="nav_individual", use_container_width=True):
            st.session_state.page = 'individual_prediction'
        
        if st.button("📊 Batch Prediction", key="nav_batch", use_container_width=True):
            st.session_state.page = 'batch_prediction'
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Info section
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
        ">
            <h4>ℹ️ How to Use</h4>
            <p><strong>Individual:</strong> Fill out the form to get your personal prediction</p>
            <p><strong>Batch:</strong> Upload a CSV file to analyze multiple students</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content based on selected page
    if st.session_state.page == 'individual_prediction':
        individual_prediction_page()
    else:
        batch_prediction_page()

if __name__ == "__main__":
    main()
