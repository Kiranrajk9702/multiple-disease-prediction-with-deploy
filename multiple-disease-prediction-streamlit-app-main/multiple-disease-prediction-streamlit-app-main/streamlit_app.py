import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="Health Assistant", layout="wide", page_icon="🧑‍⚕️")

# Get the working directory of the main script
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load the saved models
diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))

# Function to authenticate user
def authenticate_user(username, password):
    stored_users = {
        "Kiran k": "73380"  # Add more users if needed
    }
    return stored_users.get(username) == password

# Function for login page
def login_page():
    st.title("Login Page")

    menu = ["Sign In", "Sign Up"]
    choice = st.radio("Select Action", menu)

    if choice == "Sign Up":
        st.subheader("Create a New Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if password == confirm_password:
            if st.button("Sign Up"):
                st.success("Account Created Successfully!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "main"  # Redirect to main app
                st.rerun()
        else:
            st.error("Passwords do not match")

    elif choice == "Sign In":
        st.subheader("Sign In to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign In"):
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {username}!")
                st.session_state.page = "main"  # Redirect to main app
                st.rerun()
            else:
                st.error("Invalid username or password")

# Function for main page after login
def main_app():
    st.title("Health Assistant")
    st.write("Welcome to the Health Assistant app!")

    with st.sidebar:
        selected = option_menu(
            'Multiple Disease Prediction System',
            ['Diabetes Prediction', 'Heart Disease Prediction', "Parkinson's Prediction"],
            menu_icon='hospital-fill',
            icons=['activity', 'heart', 'person'],
            default_index=0
        )

# Diabetes Prediction Page
    if selected == 'Diabetes Prediction':
        st.title('Diabetes Prediction using ML')

    # Collect user input
        col1, col2, col3 = st.columns(3)

        with col1:
            Pregnancies = st.text_input('Number of Pregnancies')
        with col2:
            Glucose = st.text_input('Glucose Level')
        with col3:
            BloodPressure = st.text_input('Blood Pressure value')
        with col1:
            SkinThickness = st.text_input('Skin Thickness value')
        with col2:
            Insulin = st.text_input('Insulin Level')
        with col3:
          BMI = st.text_input('BMI value')
        with col1:
            DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
        with col2:
            Age = st.text_input('Age of the Person')

        diab_diagnosis = ''
        is_diabetic = False

    # Button for Diabetes Prediction
        if st.button('Diabetes Test Result'):
            try:
                user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
                user_input = [float(x) for x in user_input]
                diab_prediction = diabetes_model.predict([user_input])

                if diab_prediction[0] == 1:
                    st.success("**The person is diabetic.**")
                    is_diabetic = True
                else:
                    st.success("**The person is not diabetic.**")
            except ValueError:
                st.error("**Error:** Please enter valid numeric inputs.")

    # Button for Diabetes Precautions
        if st.button('Diabetes Precautions'):
            if is_diabetic:
                st.markdown("""
                                **Precautions:**
                                - Maintain a balanced diet low in sugar and carbs.
                             - Exercise regularly (e.g., yoga, walking).
                             - Monitor blood sugar levels frequently.
                             - Avoid alcohol and smoking.
                                 """)
            else:
                st.warning(
                             "**Precautions:**\n"
                             "- Maintain a balanced diet low in sugar and carbs.\n"
                             " - Exercise regularly (e.g., yoga, walking).\n"
                             "- Monitor blood sugar levels frequently.\n"
                             " - Avoid alcohol and smoking.\n")

    # Button for Diabetes Doctor Recommendations
        if st.button('Diabetes Doctor Recommendations'):
             if is_diabetic:
                st.markdown("""
                            **Doctor Contact Details:**
                            - **Dr. A. Kumar** (Diabetologist) - Ph: +91-9876543210
                            - **Dr. S. Gupta** (Endocrinologist) - Ph: +91-87654367
                             """)
             else:
                st.warning(
                            "**Doctor Contact Details:**\n"
                            "- **Dr. K. Kiran** (Diabetologist) - Ph: +91-8088005364\n"
                            "- **Dr. S. Gupta** (Endocrinologist) - Ph: +91-87654367\n")

# Heart Disease Prediction Page
    if selected == 'Heart Disease Prediction':
        st.title('Heart Disease Prediction using ML')

    # Collect user input
        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.text_input('Age')
        with col2:
            sex = st.text_input('Sex')
        with col3:
            cp = st.text_input('Chest Pain types')
        with col1:
            trestbps = st.text_input('Resting Blood Pressure')
        with col2:
            chol = st.text_input('Serum Cholestoral in mg/dl')
        with col3:
            fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
        with col1:
             restecg = st.text_input('Resting Electrocardiographic results')
        with col2:
             thalach = st.text_input('Maximum Heart Rate achieved')
        with col3:
             exang = st.text_input('Exercise Induced Angina')
        with col1:
             oldpeak = st.text_input('ST depression induced by exercise')
        with col2:
             slope = st.text_input('Slope of the peak exercise ST segment')
        with col3:
             ca = st.text_input('Major vessels colored by fluoroscopy')
        with col1:
             thal = st.text_input('Thal: 0 = normal; 1 = fixed defect; 2 = reversible defect')

        heart_diagnosis = ''
        has_heart_disease = False

    # Button for Heart Disease Prediction
        if st.button(' Heart Disease Test Result'):
            try:
                user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
                user_input = [float(x) for x in user_input]
                heart_prediction = heart_disease_model.predict([user_input])

                if heart_prediction[0] == 1:
                    st.success("**The person has heart disease.**")
                    has_heart_disease = True
                else:
                    st.success("**The person does not have any heart disease.**")
            except ValueError:
                st.error("**Error:** Please enter valid numeric inputs.")

    # Button for Heart Disease Precautions
        if st.button(' Heart Disease Precautions'):
            if has_heart_disease:
                st.markdown("""
                                **Precautions:**
                                 - Follow a heart-healthy diet (low in salt, sugar, and saturated fats).
                                 - Exercise regularly (e.g., walking, swimming).
                                 - Manage stress through yoga or meditation.
                                 - Avoid smoking and alcohol consumption.
                                 - Monitor blood pressure and cholesterol levels regularly.
                                 """)
            else:
                st.warning(
                              "**Precautions:**\n"
                              "- Follow a heart-healthy diet (low in salt, sugar, and saturated fats).\n"
                              "- Exercise regularly (e.g., walking, swimming).\n"
                              "- Manage stress through yoga or meditation.\n"
                              "- Avoid smoking and alcohol consumption.\n"
                              "- Monitor blood pressure and cholesterol levels regularly.)\n")

# Button for Heart Disease Doctor Recommendations
        if st.button('Heart Disease Doctor Recommendations'):
            if has_heart_disease:
                 st.markdown("""
                                **Doctor Contact Details:**
                                - **Dr. R. Sharma** (Cardiologist) - Ph: +91-9876543210
                                 - **Dr. P. Verma** (Cardiac Specialist) - Ph: +91-8765432109
                                 """)
            else:
                st.warning("""
                            **Doctor Contact Details:**
                             - **Dr. R. Sharma** (Cardiologist) - Ph: +91-9876543210
                             - **Dr. P. Verma** (Cardiac Specialist) - Ph: +91-8765432109
                             """)

# Parkinson's Prediction Page
    if selected == "Parkinson's Prediction":
        st.title("Parkinson's Disease Prediction using ML")

    # Collect user input
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
             fo = st.text_input('MDVP:Fo(Hz)')
        with col2:
            fhi = st.text_input('MDVP:Fhi(Hz)')
        with col3:
            flo = st.text_input('MDVP:Flo(Hz)')
        with col4:
            Jitter_percent = st.text_input('MDVP:Jitter(%)')
        with col5:
            Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')
        with col1:
            RAP = st.text_input('MDVP:RAP')
        with col2:
            PPQ = st.text_input('MDVP:PPQ')
        with col3:
            DDP = st.text_input('Jitter:DDP')
        with col4:
            Shimmer = st.text_input('MDVP:Shimmer')
        with col5:
            Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')
        with col1:
            APQ3 = st.text_input('Shimmer:APQ3')
        with col2:
            APQ5 = st.text_input('Shimmer:APQ5')
        with col3:
            APQ = st.text_input('MDVP:APQ')
        with col4:
            DDA = st.text_input('Shimmer:DDA')
        with col5:
            NHR = st.text_input('NHR')
        with col1:
            HNR = st.text_input('HNR')
        with col2:
            RPDE = st.text_input('RPDE')
        with col3:
            DFA = st.text_input('DFA')
        with col4:
            spread1 = st.text_input('spread1')
        with col5:
            spread2 = st.text_input('spread2')
        with col1:
            D2 = st.text_input('D2')
        with col2:
            PPE = st.text_input('PPE')

        parkinsons_diagnosis = ''
        has_parkinsons = False

    # Button for Parkinson's Prediction
        if st.button("Parkinson's Test Result"):
            try:
                user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5,
                          APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
                user_input = [float(x) for x in user_input]
                parkinsons_prediction = parkinsons_model.predict([user_input])

                if parkinsons_prediction[0] == 1:
                    st.success("**The person has Parkinson's disease.**")
                    has_parkinsons = True
                else:
                    st.success("**The person does not have Parkinson's disease.**")
            except ValueError:
                st.error("**Error:** Please enter valid numeric inputs.")

    # Button for Parkinson's Precautions
        if st.button("Parkinson's Precautions"):
            if has_parkinsons:
                st.markdown("""
                                **Precautions:**
                                - Follow a high-fiber and nutritious diet.
                                - Engage in physiotherapy and regular exercise.
                                - Take medications as prescribed by the doctor.
                                - Practice speech therapy if necessary.
                                    """)
            else:
                st.warning(
                                "**Precautions:**\n"
                                "- Follow a high-fiber and nutritious diet.\n"
                                "- Engage in physiotherapy and regular exercise.\n"
                                "- Take medications as prescribed by the doctor.\n"
                                "- Practice speech therapy if necessary.\n")

    # Button for Parkinson's Doctor Recommendations
        if st.button("Parkinson's Doctor Recommendations"):
            if has_parkinsons:
                st.markdown("""
                                **Doctor Contact Details:**
                                - **Dr. S. Nair** (Neurologist) - Ph: +91-9876543210
                                - **Dr. V. Reddy** (Parkinson's Specialist) - Ph: +91-8765432109
                                """)
            else:
                st.warning(
                                "**Doctor Contact Details:**\n"
                                "- **Dr. S. Nair** (Neurologist) - Ph: +91-9876543210\n"
                                "- **Dr. V. Reddy** (Parkinson's Specialist) - Ph: +91-8765432109)\n")

# Ensure session state exists
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"  # Default to login page

# Navigation Logic
if st.session_state.page == "main":
    main_app()
else:
    login_page()


