import streamlit as st
import pandas as pd
import joblib

# Load model and scaler
model = joblib.load("student_model.pkl")
scaler = joblib.load("scaler.pkl")

# Feedback function
def generate_feedback(row):
    feedback = []

    if row['Attendance'] < 75:
        feedback.append("Your attendance is below average. Try to attend more classes.")
    if row['InternalMarks'] < 60:
        feedback.append("Work on improving your internal scores through assignments and tests.")
    if row['StudyHoursPerWeek'] < 5:
        feedback.append("Increase your weekly study hours to better understand the concepts.")
    elif row['StudyHoursPerWeek'] > 12:
        feedback.append("You're studying well. Keep up the consistency!")
    if row['Participation'] == 0:
        feedback.append("Engage more in class discussions to improve your understanding.")
    if row['Extracurricular'] == 1:
        feedback.append("Great job managing studies with extracurricular activities!")

    return " ".join(feedback)

# Streamlit UI
st.title("🧍 Individual Student Prediction")

st.markdown("Enter a student's details to predict their academic result and receive personalized feedback.")

col1, col2 = st.columns(2)
with col1:
    attendance = st.slider("Attendance (%)", 0, 100, 75)
    internal = st.slider("Internal Marks (%)", 0, 100, 60)
    study_hours = st.slider("Study Hours per Week", 0, 20, 5)

with col2:
    participation = st.radio("Class Participation", ["Yes", "No"])
    extracurricular = st.radio("Extracurricular Involvement", ["Yes", "No"])

if st.button("🔍 Predict"):
    input_data = pd.DataFrame([{
        "Attendance": attendance,
        "InternalMarks": internal,
        "StudyHoursPerWeek": study_hours,
        "Participation": 1 if participation == "Yes" else 0,
        "Extracurricular": 1 if extracurricular == "Yes" else 0
    }])

    scaled_input = scaler.transform(input_data)
    prediction = model.predict(scaled_input)[0]
    result = "Pass" if prediction == 1 else "Fail"
    feedback = generate_feedback(input_data.iloc[0])

    st.success(f"🎯 Predicted Result: **{result}**")
    st.info(f"💡 Feedback: {feedback}")
