import streamlit as st
import json
from pathlib import Path
from main import FitFusion
import time
from datetime import datetime

# --- Custom CSS for Modern UI ---
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root Variables */
    :root {
        --primary-color: #00C851;
        --secondary-color: #FF6B35;
        --accent-color: #4A90E2;
        --background-color: #F8FAFC;
        --card-background: #FFFFFF;
        --text-primary: #1A202C;
        --text-secondary: #718096;
        --border-color: #E2E8F0;
        --success-color: #38A169;
        --warning-color: #ED8936;
        --error-color: #E53E3E;
    }
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-container {
        background: var(--card-background);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        margin: 20px;
        padding: 30px;
        min-height: 80vh;
    }
    
    /* Header Styles */
    .app-header {
        text-align: center;
        margin-bottom: 40px;
        padding: 30px 0;
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        border-radius: 15px;
        color: white;
    }
    
    .app-title {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        margin: 10px 0 0 0;
        opacity: 0.9;
    }
    
    /* Form Styles */
    .form-container {
        background: var(--card-background);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border-color);
    }
    
    .form-section {
        margin-bottom: 30px;
    }
    
    .form-section h3 {
        color: var(--text-primary);
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--primary-color);
    }
    
    /* Input Styles */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid var(--border-color);
        padding: 12px 16px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(0, 200, 81, 0.1);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 200, 81, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 200, 81, 0.4);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--card-background), #F1F5F9);
    }
    
    .sidebar .sidebar-content {
        background: var(--card-background);
        border-radius: 15px;
        margin: 10px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat Styles */
    .chat-container {
        background: var(--card-background);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        min-height: 400px;
    }
    
    .message-user {
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(0, 200, 81, 0.3);
        font-weight: 500;
    }
    
    .message-assistant {
        background: linear-gradient(135deg, #F7FAFC, #EDF2F7);
        color: var(--text-primary);
        padding: 20px 25px;
        border-radius: 20px 20px 20px 5px;
        margin: 15px 0;
        max-width: 85%;
        border-left: 4px solid var(--primary-color);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        line-height: 1.6;
        direction: rtl;
        text-align: right;
        font-family: 'Tahoma', 'Arial', sans-serif;
    }
    
    .message-assistant h1, .message-assistant h2, .message-assistant h3 {
        color: var(--primary-color);
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    .message-assistant ul, .message-assistant ol {
        margin: 10px 0;
        padding-left: 20px;
    }
    
    .message-assistant li {
        margin: 5px 0;
    }
    
    .message-assistant strong {
        color: var(--accent-color);
    }
    
    .message-assistant table {
        direction: rtl;
        text-align: right;
        font-family: 'Tahoma', 'Arial', sans-serif;
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .message-assistant th, .message-assistant td {
        border: 1px solid #ddd;
        padding: 12px 8px;
        text-align: right;
        direction: rtl;
        font-size: 14px;
        vertical-align: top;
    }
    
    .message-assistant th {
        background-color: #f8f9fa;
        font-weight: bold;
        color: var(--text-primary);
        text-align: center;
    }
    
    .message-assistant tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    .message-assistant tr:hover {
        background-color: #e3f2fd;
    }
    
    /* Streamlit markdown table styling */
    .message-assistant .dataframe {
        direction: rtl;
        text-align: right;
        font-family: 'Tahoma', 'Arial', sans-serif;
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .message-assistant .dataframe th, .message-assistant .dataframe td {
        border: 1px solid #ddd;
        padding: 12px 8px;
        text-align: right;
        direction: rtl;
        font-size: 14px;
        vertical-align: top;
    }
    
    .message-assistant .dataframe th {
        background-color: #f8f9fa;
        font-weight: bold;
        color: var(--text-primary);
        text-align: center;
    }
    
    .message-assistant .dataframe tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    .message-assistant .dataframe tr:hover {
        background-color: #e3f2fd;
    }
    
    .chat-input-container {
        background: var(--card-background);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    
    /* Progress Bar */
    .progress-container {
        background: var(--card-background);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border: 2px solid var(--border-color);
    }
    
    .progress-container h3 {
        color: var(--primary-color);
        margin-bottom: 20px;
        font-size: 1.4rem;
        font-weight: 600;
        text-align: center;
    }
    
    .progress-step {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        padding: 12px 18px;
        border-radius: 10px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .progress-step.active {
        color: var(--primary-color);
        font-weight: 600;
        background: rgba(0, 200, 81, 0.1);
        border: 2px solid var(--primary-color);
    }
    
    .progress-step.completed {
        color: var(--success-color);
        background: rgba(56, 161, 105, 0.1);
        border: 2px solid var(--success-color);
    }
    
    .progress-step.pending {
        color: var(--text-secondary);
        background: rgba(113, 128, 150, 0.1);
        border: 2px solid var(--border-color);
    }
    
    /* Stats Cards */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .stat-card {
        background: var(--card-background);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border-color);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 5px;
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Quick Actions */
    .quick-actions {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin: 20px 0;
    }
    
    .quick-action-btn {
        background: var(--card-background);
        border: 2px solid var(--border-color);
        border-radius: 25px;
        padding: 8px 16px;
        font-size: 0.9rem;
        color: var(--text-primary);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-action-btn:hover {
        border-color: var(--primary-color);
        color: var(--primary-color);
        transform: translateY(-1px);
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid var(--primary-color);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-container {
            margin: 10px;
            padding: 20px;
        }
        
        .app-title {
            font-size: 2rem;
        }
        
        .stats-container {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# --- Model Initialization ---
directory, model_type, vectorstore, file_formats = './diet', 'gpt-4.1-mini', 'chroma', ['txt']

# Initialize FitFusion with error handling for ChromaDB schema issues
try:
    fitfusion_model = FitFusion(llm_model=model_type, vectorstore_name=vectorstore)
    fitfusion_model.model_chain_init(directory, data_types=file_formats)
except Exception as e:
    if "no such column: collections.topic" in str(e) or "OperationalError" in str(e):
        # Clear corrupted ChromaDB database and recreate
        import shutil
        import os
        chroma_files = ['chroma.sqlite3', '74cd7b16-00dd-4b6a-b1ae-7f82165cde1c']
        for file in chroma_files:
            file_path = os.path.join(directory, file)
            if os.path.exists(file_path):
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
        
        # Recreate the model
        fitfusion_model = FitFusion(llm_model=model_type, vectorstore_name=vectorstore)
        fitfusion_model.model_chain_init(directory, data_types=file_formats)
    elif "AuthenticationError" in str(e) or "invalid_api_key" in str(e):
        # Handle API key issues
        print(f"❌ API Authentication Error: {e}")
        print("Please check your OpenAI API key in main.py")
        fitfusion_model = None
    else:
        print(f"❌ Unexpected error during model initialization: {e}")
        fitfusion_model = None

# --- Streamlit Page Settings ---
st.set_page_config(
    page_title="FitFusion - Your AI Fitness Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_custom_css()

# --- Utility Functions ---
def load_default_data() -> dict:
    """Load the default user data from a JSON file."""
    default_file = Path(__file__).parent / "default_user_data.json"
    with open(default_file, "r") as f:
        return json.load(f)

def calculate_bmi(height_str, weight_str):
    """Calculate BMI from height and weight strings."""
    try:
        height_cm = float(height_str.replace('cm', '').strip())
        weight_kg = float(weight_str.replace('kg', '').strip())
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 1)
    except:
        return None

def get_bmi_category(bmi):
    """Get BMI category."""
    if bmi < 18.5:
        return "Underweight", "🔵"
    elif bmi < 25:
        return "Normal", "🟢"
    elif bmi < 30:
        return "Overweight", "🟡"
    else:
        return "Obese", "🔴"

def restart_agent():
    """Clears the session state and restarts the app."""
    keys_to_delete = ["stage", "fit_fusion_agent", "messages", "user_data", "pending_query", "current_step"]
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def save_user_data():
    """Save user data to a file."""
    if "user_data" in st.session_state:
        data_file = Path(__file__).parent / "user_data_backup.json"
        with open(data_file, "w") as f:
            json.dump(st.session_state["user_data"], f, indent=2)

def load_user_data():
    """Load user data from backup file."""
    data_file = Path(__file__).parent / "user_data_backup.json"
    if data_file.exists():
        with open(data_file, "r") as f:
            return json.load(f)
    return load_default_data()

# --- Main Application Logic ---
def main() -> None:
    # Initialize session state variables
    if "stage" not in st.session_state:
        st.session_state["stage"] = "initial"
    if "user_data" not in st.session_state:
        st.session_state["user_data"] = load_user_data()
    if "fit_fusion_agent" not in st.session_state:
        try:
            st.session_state["fit_fusion_agent"] = fitfusion_model
        except NameError:
            # If fitfusion_model failed to initialize, create a placeholder
            st.session_state["fit_fusion_agent"] = None
            st.error("⚠️ Model initialization failed. Please check the console for details.")
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "current_step" not in st.session_state:
        st.session_state["current_step"] = 1

    # --- Header ---
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">💪 FitFusion</h1>
        <p class="app-subtitle">Your Personal AI Fitness & Nutrition Coach</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Initial Stage: Enhanced User Data Input ---
    if st.session_state["stage"] == "initial":
        # Progress indicator
        steps = ["Personal Info", "Goals & Preferences", "Health Details", "Lifestyle", "Generate Plan"]
        current_step = st.session_state["current_step"]
        
        # Progress indicator
        progress_html = '<div class="progress-container"><h3>Setup Progress</h3>'
        for i, step in enumerate(steps, 1):
            status = "active" if i == current_step else ("completed" if i < current_step else "pending")
            progress_html += f'<div class="progress-step {status}">{"✅" if i < current_step else "🔄" if i == current_step else "⏳"} {step}</div>'
        progress_html += '</div>'
        st.markdown(progress_html, unsafe_allow_html=True)
        
        # Multi-step form
        with st.form("enhanced_user_data_form"):
            if current_step == 1:  # Personal Information
                st.markdown("### 👤 Personal Information")
                col1, col2 = st.columns(2)
                
                with col1:
                    age = st.number_input("Age", min_value=1, max_value=120, 
                                        value=st.session_state["user_data"].get("Age", 30),
                                        help="Your current age")
                    gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                                        index=["Male", "Female", "Other"].index(st.session_state["user_data"].get("Gender", "Male")))
                
                with col2:
                    height = st.text_input("Height", value=st.session_state["user_data"].get("Height", "170 cm"),
                                         placeholder="e.g., 170 cm", help="Enter your height in cm")
                    weight = st.text_input("Weight", value=st.session_state["user_data"].get("Weight", "70 kg"),
                                         placeholder="e.g., 70 kg", help="Enter your weight in kg")
                
                # BMI Calculator
                if height and weight:
                    bmi = calculate_bmi(height, weight)
                    if bmi:
                        category, emoji = get_bmi_category(bmi)
                        st.info(f"📊 Your BMI: {bmi} ({category} {emoji})")
                
                if st.form_submit_button("Next Step ➡️", use_container_width=True):
                    st.session_state["user_data"].update({
                        "Age": age, "Gender": gender, "Height": height, "Weight": weight
                    })
                    st.session_state["current_step"] = 2
                    st.rerun()
            
            elif current_step == 2:  # Goals & Preferences
                st.markdown("### 🎯 Goals & Preferences")
                
                goal_options = ["Lose Weight", "Muscle Gain", "Maintain Weight", "Improve Fitness", "General Health"]
                current_goal = st.session_state["user_data"].get("Primary Goal", "Muscle Gain")
                try:
                    goal_index = goal_options.index(current_goal)
                except ValueError:
                    goal_index = 1  # Default to "Muscle Gain"
                primary_goal = st.selectbox("Primary Goal", goal_options, index=goal_index)
                
                diet_options = ["Traditional", "Vegetarian", "Vegan", "Keto", "Mediterranean", "High-protein", "Paleo", "Omnivore"]
                current_diet = st.session_state["user_data"].get("Diet Type", "Traditional")
                try:
                    diet_index = diet_options.index(current_diet)
                except ValueError:
                    diet_index = 0  # Default to "Traditional"
                diet_type = st.selectbox("Diet Type", diet_options, index=diet_index)
                
                workout_options = ["Cardio", "Strength training", "Yoga", "Pilates", "Swimming", "Running", "Cycling", "Dancing", "Martial Arts"]
                current_workouts = st.session_state["user_data"].get("Preferred Workout Types", "Cardio, Strength training")
                # Parse the current workouts and filter to only include valid options
                try:
                    default_workouts = [w.strip() for w in current_workouts.split(",") if w.strip() in workout_options]
                    if not default_workouts:
                        default_workouts = ["Cardio", "Strength training"]  # Fallback defaults
                except:
                    default_workouts = ["Cardio", "Strength training"]  # Fallback defaults
                
                workout_types = st.multiselect("Preferred Workout Types", workout_options, default=default_workouts)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("⬅️ Previous", use_container_width=True):
                        st.session_state["current_step"] = 1
                        st.rerun()
                with col2:
                    if st.form_submit_button("Next Step ➡️", use_container_width=True):
                        st.session_state["user_data"].update({
                            "Primary Goal": primary_goal,
                            "Diet Type": diet_type,
                            "Preferred Workout Types": ", ".join(workout_types)
                        })
                        st.session_state["current_step"] = 3
                        st.rerun()
            
            elif current_step == 3:  # Health Details
                st.markdown("### 🏥 Health Information")
                
                col1, col2 = st.columns(2)
                with col1:
                    medical_conditions = st.text_area("Medical Conditions", 
                        value=st.session_state["user_data"].get("Existing Medical Conditions", "None"),
                        placeholder="List any medical conditions or leave as 'None'")
                    food_allergies = st.text_area("Food Allergies", 
                        value=st.session_state["user_data"].get("Food Allergies", "None"),
                        placeholder="List any food allergies or leave as 'None'")
                
                with col2:
                    fitness_options = ["Beginner", "Intermediate", "Advanced"]
                    current_fitness = st.session_state["user_data"].get("Current Fitness Level", "Beginner")
                    try:
                        fitness_index = fitness_options.index(current_fitness)
                    except ValueError:
                        fitness_index = 0  # Default to "Beginner"
                    fitness_level = st.selectbox("Current Fitness Level", fitness_options, index=fitness_index)
                    frequency_options = ["1-2 days/week", "3 days/week", "4-5 days/week", "6+ days/week", "Daily"]
                    current_frequency = st.session_state["user_data"].get("Workout Frequency", "3 days/week")
                    try:
                        frequency_index = frequency_options.index(current_frequency)
                    except ValueError:
                        frequency_index = 1  # Default to "3 days/week"
                    workout_frequency = st.selectbox("Workout Frequency", frequency_options, index=frequency_index)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("⬅️ Previous", use_container_width=True):
                        st.session_state["current_step"] = 2
                        st.rerun()
                with col2:
                    if st.form_submit_button("Next Step ➡️", use_container_width=True):
                        st.session_state["user_data"].update({
                            "Existing Medical Conditions": medical_conditions,
                            "Food Allergies": food_allergies,
                            "Current Fitness Level": fitness_level,
                            "Workout Frequency": workout_frequency
                        })
                        st.session_state["current_step"] = 4
                        st.rerun()
            
            elif current_step == 4:  # Lifestyle
                st.markdown("### 🏠 Lifestyle & Habits")
                
                col1, col2 = st.columns(2)
                with col1:
                    sleep_text = st.session_state["user_data"].get("Sleep Patterns", "~8 hours")
                    # Extract number from sleep text (e.g., "~8 hours" -> 8)
                    try:
                        import re
                        sleep_match = re.search(r'(\d+)', sleep_text)
                        sleep_value = int(sleep_match.group(1)) if sleep_match else 8
                    except:
                        sleep_value = 8
                    sleep_hours = st.slider("Sleep Hours per Night", 4, 12, value=sleep_value)
                    stress_options = ["Low", "Moderate", "High"]
                    current_stress = st.session_state["user_data"].get("Stress Levels", "low").title()
                    try:
                        stress_index = stress_options.index(current_stress)
                    except ValueError:
                        stress_index = 0  # Default to "Low"
                    stress_level = st.selectbox("Stress Level", stress_options, index=stress_index)
                
                with col2:
                    hydration_text = st.session_state["user_data"].get("Hydration Habits", "~3L water/day")
                    # Extract number from hydration text (e.g., "~3L water/day" -> 3)
                    try:
                        import re
                        hydration_match = re.search(r'(\d+)', hydration_text)
                        hydration_value = int(hydration_match.group(1)) if hydration_match else 3
                    except:
                        hydration_value = 3
                    hydration = st.slider("Daily Water Intake (L)", 1, 6, value=hydration_value)
                    meal_options = ["2 meals", "3 meals", "3 meals + 1 snack", "3 meals + 2 snacks", "4+ meals", "5+ meals"]
                    current_meals = st.session_state["user_data"].get("Meal Frequency Preferences", "3 meals + 2 snacks")
                    try:
                        meal_index = meal_options.index(current_meals)
                    except ValueError:
                        meal_index = 3  # Default to "3 meals + 2 snacks"
                    meal_frequency = st.selectbox("Meal Frequency", meal_options, index=meal_index)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("⬅️ Previous", use_container_width=True):
                        st.session_state["current_step"] = 3
                        st.rerun()
                with col2:
                    if st.form_submit_button("Generate My Plan! 🚀", use_container_width=True):
                        st.session_state["user_data"].update({
                            "Sleep Patterns": f"~{sleep_hours} hours",
                            "Stress Levels": stress_level.lower(),
                            "Hydration Habits": f"~{hydration}L water/day",
                            "Meal Frequency Preferences": meal_frequency
                        })
                        st.session_state["current_step"] = 5
                        st.session_state["stage"] = "chat"
                        save_user_data()
                        
                        # Automatically generate the plan
                        user_data = st.session_state["user_data"]
                        user_info_text = f"""
                        Generate a comprehensive 7-day diet plan and workout schedule based on the following details:
                        Age: {user_data.get("Age", "N/A")}
                        Gender: {user_data.get("Gender", "N/A")}
                        Height: {user_data.get("Height", "N/A")}
                        Weight: {user_data.get("Weight", "N/A")}
                        Primary Goal: {user_data.get("Primary Goal", "N/A")}
                        Diet Type: {user_data.get("Diet Type", "N/A")}
                        Preferred Workout Types: {user_data.get("Preferred Workout Types", "N/A")}
                        Current Fitness Level: {user_data.get("Current Fitness Level", "N/A")}
                        Workout Frequency: {user_data.get("Workout Frequency", "N/A")}
                        Medical Conditions: {user_data.get("Existing Medical Conditions", "None")}
                        Food Allergies: {user_data.get("Food Allergies", "None")}
                        Sleep Patterns: {user_data.get("Sleep Patterns", "N/A")}
                        Stress Levels: {user_data.get("Stress Levels", "N/A")}
                        Hydration Habits: {user_data.get("Hydration Habits", "N/A")}
                        Meal Frequency: {user_data.get("Meal Frequency Preferences", "N/A")}
                        """
                        st.session_state["pending_query"] = user_info_text
                        st.rerun()

    else:  # stage == "chat"
        # Enhanced Sidebar
        with st.sidebar:
            st.markdown("### 🎛️ Control Panel")
            
            # Quick actions
            st.markdown("#### Quick Actions")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 New Chat", use_container_width=True):
                    restart_agent()
            with col2:
                if st.button("💾 Save Data", use_container_width=True):
                    save_user_data()
                    st.success("Data saved!")
            
            # User stats
            st.markdown("#### 📊 Your Stats")
            user_data = st.session_state["user_data"]
            bmi = calculate_bmi(user_data.get("Height", "170 cm"), user_data.get("Weight", "70 kg"))
            
            if bmi:
                category, emoji = get_bmi_category(bmi)
                st.metric("BMI", f"{bmi} {emoji}", category)
            
            st.metric("Age", user_data.get("Age", "N/A"))
            st.metric("Goal", user_data.get("Primary Goal", "N/A"))
            st.metric("Diet", user_data.get("Diet Type", "N/A"))
            
            # Quick action buttons
            st.markdown("#### 💬 Quick Questions")
            quick_questions = [
                "Show me today's meal plan",
                "What's my workout for today?",
                "Adjust my calorie intake",
                "Suggest healthy snacks",
                "How's my progress?",
                "Give me a shopping list",
                "What should I eat for breakfast?",
                "Show me this week's workout schedule"
            ]
            
            for question in quick_questions:
                if st.button(question, use_container_width=True):
                    if st.session_state["fit_fusion_agent"] is not None:
                        st.session_state["messages"].append({"role": "user", "content": question})
                        # Generate response immediately
                        with st.spinner("🤔 Thinking..."):
                            response_gen = st.session_state["fit_fusion_agent"].query_inferences(question)
                            response_steps = []
                            for step in response_gen:
                                response_steps.append(step)
                            final_response = response_steps[-1] if response_steps else "I couldn't generate a response. Please try again."
                        st.session_state["messages"].append({"role": "assistant", "content": final_response})
                        st.rerun()
                    else:
                        st.error("❌ Model not available. Please refresh the page.")
            
            # User data update form (simplified)
            with st.expander("⚙️ Update Profile", expanded=False):
                with st.form("quick_update_form"):
                    age = st.number_input("Age", min_value=1, max_value=120, value=user_data.get("Age", 30))
                    weight = st.text_input("Weight", value=user_data.get("Weight", "70 kg"))
                    goal_options = ["Lose Weight", "Muscle Gain", "Maintain Weight", "Improve Fitness", "General Health"]
                    current_goal = user_data.get("Primary Goal", "Muscle Gain")
                    try:
                        goal_index = goal_options.index(current_goal)
                    except ValueError:
                        goal_index = 1  # Default to "Muscle Gain"
                    goal = st.selectbox("Goal", goal_options, index=goal_index)
                    
                    if st.form_submit_button("Update", use_container_width=True):
                        st.session_state["user_data"].update({
                            "Age": age, "Weight": weight, "Primary Goal": goal
                        })
                        st.success("Profile updated!")

        # Main chat area with better framing
        st.markdown("### 💬 Chat with Your AI Coach")
        
        # Chat container with better styling
        chat_container = st.container()
        with chat_container:
            if st.session_state["messages"]:
                # Display conversation in a styled container
                for msg in st.session_state["messages"]:
                    with st.chat_message(msg["role"]):
                        if msg["role"] == "user":
                            st.markdown(f"**You:** {msg['content']}")
                        else:
                            st.markdown(msg["content"])
            else:
                # Welcome message when no conversation yet
                st.markdown("""
                <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 15px; margin: 20px 0;">
                    <h4 style="color: #495057; margin-bottom: 15px;">🤖 Your AI Fitness Coach is Ready!</h4>
                    <p style="color: #6c757d; margin-bottom: 20px;">I've analyzed your profile and created a personalized plan. You can now:</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Handle pending query
        if "pending_query" in st.session_state and st.session_state["pending_query"] is not None:
            # Add the user request to the chat
            st.session_state["messages"].append({"role": "user", "content": "Generate my personalized diet and workout plan."})
            pending_query_text = st.session_state["pending_query"]
            
            # Prepare user info text
            user_data = st.session_state["user_data"]
            user_info_text = f"""
            لطفاً یک برنامه غذایی و ورزشی ۷ روزه جامع به زبان فارسی بر اساس جزئیات زیر ایجاد کنید:
            
            سن: {user_data.get("Age", "N/A")}
            جنسیت: {user_data.get("Gender", "N/A")}
            قد: {user_data.get("Height", "N/A")}
            وزن: {user_data.get("Weight", "N/A")}
            هدف اصلی: {user_data.get("Primary Goal", "N/A")}
            نوع رژیم: {user_data.get("Diet Type", "N/A")}
            انواع تمرینات مورد علاقه: {user_data.get("Preferred Workout Types", "N/A")}
            سطح آمادگی جسمانی فعلی: {user_data.get("Current Fitness Level", "N/A")}
            دفعات تمرین: {user_data.get("Workout Frequency", "N/A")}
            شرایط پزشکی: {user_data.get("Existing Medical Conditions", "هیچ")}
            آلرژی‌های غذایی: {user_data.get("Food Allergies", "هیچ")}
            الگوی خواب: {user_data.get("Sleep Patterns", "N/A")}
            سطح استرس: {user_data.get("Stress Levels", "N/A")}
            عادات آبرسانی: {user_data.get("Hydration Habits", "N/A")}
            دفعات وعده غذایی: {user_data.get("Meal Frequency Preferences", "N/A")}
            
            لطفاً پاسخ خود را به صورت زیر ارائه دهید:
            1. مقدمه‌ای کوتاه درباره برنامه
            2. جدول برنامه غذایی ۷ روزه با ستون‌های: روز، صبحانه، میان‌وعده ۱، ناهار، میان‌وعده ۲، شام
            3. برنامه ورزشی هفتگی
            4. نکات مهم و توصیه‌ها
            
            حتماً از جدول Markdown با ساختار زیر استفاده کنید:
            | روز | صبحانه | میان‌وعده ۱ | ناهار | میان‌وعده ۲ | شام |
            |-----|---------|-------------|-------|-------------|-----|
            | شنبه | ... | ... | ... | ... | ... |
            | یکشنبه | ... | ... | ... | ... | ... |
            و همینطور برای بقیه روزها...
            """
            
            steps = []
            reasoning_expander = st.expander("🧠 AI Reasoning Process", expanded=True)
            reasoning_placeholder = reasoning_expander.empty()
            
            with st.spinner("🤔 Analyzing your profile and generating personalized recommendations..."):
                if st.session_state["fit_fusion_agent"] is None:
                    st.error("❌ Model not available. Please refresh the page or check the console for errors.")
                    return
                response_gen = st.session_state["fit_fusion_agent"].query_inferences(user_info_text)
                for step in response_gen:
                    if step.strip() == user_info_text.strip():
                        continue
                    
                    steps.append(step)
                    if len(steps) > 1:
                        reasoning_text = "\n".join(steps[:-1])
                    else:
                        reasoning_text = ""
                    
                    scrollable_div = (
                        f'<div style="max-height:300px; overflow-y:auto; padding:15px; border:1px solid #E2E8F0; border-radius:10px; background:#F7FAFC;">'
                        f'{reasoning_text}</div>'
                    )
                    reasoning_placeholder.markdown(scrollable_div, unsafe_allow_html=True)
            
            # The final answer is the last step
            final_answer = steps[-1] if steps else "I apologize, but I couldn't generate a response. Please try again."
            st.session_state["messages"].append({"role": "assistant", "content": final_answer})
            st.session_state["pending_query"] = None
            st.rerun()  # Force refresh to show the response
        
        # Enhanced chat input with better styling
        st.markdown("---")
        
        # Chat input container with styling
        with st.container():
            st.markdown("""
            <div class="chat-input-container">
                <h3 style="color: var(--primary-color); margin-bottom: 15px;">💬 Ask Your AI Coach</h3>
            </div>
            """, unsafe_allow_html=True)
            
            user_input = st.chat_input("Ask me anything about your fitness journey... 💪", key="main_chat_input")
            if user_input:
                if st.session_state["fit_fusion_agent"] is not None:
                    st.session_state["messages"].append({"role": "user", "content": user_input})
                    with st.spinner("🤔 Your AI coach is thinking..."):
                        response = st.session_state["fit_fusion_agent"].query_inferences(user_input)
                    st.session_state["messages"].append({"role": "assistant", "content": response})
                    st.rerun()
                else:
                    st.error("❌ Model not available. Please refresh the page or check the console for errors.")
        
        # Show Quick Actions after first response
        if len(st.session_state["messages"]) > 0:
            st.markdown("---")
            st.markdown("#### 🚀 Quick Actions")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("🍎 Today's Meals", use_container_width=True, key="quick_meals"):
                    if st.session_state["fit_fusion_agent"] is not None:
                        question = "What should I eat today? Show me specific meals with portions."
                        st.session_state["messages"].append({"role": "user", "content": question})
                        with st.spinner("🤔 Thinking..."):
                            response_gen = st.session_state["fit_fusion_agent"].query_inferences(question)
                            response_steps = []
                            for step in response_gen:
                                response_steps.append(step)
                            final_response = response_steps[-1] if response_steps else "I couldn't generate a response. Please try again."
                        st.session_state["messages"].append({"role": "assistant", "content": final_response})
                        st.rerun()
            
            with col2:
                if st.button("🏋️ Today's Workout", use_container_width=True, key="quick_workout"):
                    if st.session_state["fit_fusion_agent"] is not None:
                        question = "Show me my workout for today with specific exercises, sets, and reps."
                        st.session_state["messages"].append({"role": "user", "content": question})
                        with st.spinner("🤔 Thinking..."):
                            response_gen = st.session_state["fit_fusion_agent"].query_inferences(question)
                            response_steps = []
                            for step in response_gen:
                                response_steps.append(step)
                            final_response = response_steps[-1] if response_steps else "I couldn't generate a response. Please try again."
                        st.session_state["messages"].append({"role": "assistant", "content": final_response})
                        st.rerun()
            
            with col3:
                if st.button("📋 Shopping List", use_container_width=True, key="quick_shopping"):
                    if st.session_state["fit_fusion_agent"] is not None:
                        question = "Give me a shopping list for this week's meals."
                        st.session_state["messages"].append({"role": "user", "content": question})
                        with st.spinner("🤔 Thinking..."):
                            response_gen = st.session_state["fit_fusion_agent"].query_inferences(question)
                            response_steps = []
                            for step in response_gen:
                                response_steps.append(step)
                            final_response = response_steps[-1] if response_steps else "I couldn't generate a response. Please try again."
                        st.session_state["messages"].append({"role": "assistant", "content": final_response})
                        st.rerun()
            
            with col4:
                if st.button("📊 Progress Tips", use_container_width=True, key="quick_progress"):
                    if st.session_state["fit_fusion_agent"] is not None:
                        question = "How can I track my progress and stay motivated?"
                        st.session_state["messages"].append({"role": "user", "content": question})
                        with st.spinner("🤔 Thinking..."):
                            response_gen = st.session_state["fit_fusion_agent"].query_inferences(question)
                            response_steps = []
                            for step in response_gen:
                                response_steps.append(step)
                            final_response = response_steps[-1] if response_steps else "I couldn't generate a response. Please try again."
                        st.session_state["messages"].append({"role": "assistant", "content": final_response})
                        st.rerun()
        
        # Show chat input only when there are no messages (minimal interface)
        if not st.session_state["messages"]:
            # Quick suggestion chips for initial interaction
            st.markdown("#### 💡 Try asking:")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🍎 What should I eat today?", use_container_width=True, key="suggest_meals"):
                    if st.session_state["fit_fusion_agent"] is not None:
                        question = "What should I eat today?"
                        st.session_state["messages"].append({"role": "user", "content": question})
                        with st.spinner("🤔 Thinking..."):
                            response = st.session_state["fit_fusion_agent"].query_inferences(question)
                        st.session_state["messages"].append({"role": "assistant", "content": response})
                        st.rerun()
            with col2:
                if st.button("🏋️ Show my workout", use_container_width=True, key="suggest_workout"):
                    if st.session_state["fit_fusion_agent"] is not None:
                        question = "Show me my workout for today"
                        st.session_state["messages"].append({"role": "user", "content": question})
                        with st.spinner("🤔 Thinking..."):
                            response = st.session_state["fit_fusion_agent"].query_inferences(question)
                        st.session_state["messages"].append({"role": "assistant", "content": response})
                        st.rerun()
            with col3:
                if st.button("📊 Track progress", use_container_width=True, key="suggest_progress"):
                    if st.session_state["fit_fusion_agent"] is not None:
                        question = "How can I track my progress?"
                        st.session_state["messages"].append({"role": "user", "content": question})
                        with st.spinner("🤔 Thinking..."):
                            response = st.session_state["fit_fusion_agent"].query_inferences(question)
                        st.session_state["messages"].append({"role": "assistant", "content": response})
                        st.rerun()

if __name__ == "__main__":
    main()
