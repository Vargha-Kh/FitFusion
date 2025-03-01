import streamlit as st
import json
from pathlib import Path
from main import FitFusion

# --- Model Initialization ---
directory, model_type, vectorstore, file_formats = './diet', 'gpt-4o-mini', 'chroma', ['txt']
fitfusion_model = FitFusion(llm_model=model_type, vectorstore_name=vectorstore)
fitfusion_model.model_chain_init(directory, data_types=file_formats)

# --- Streamlit Page Settings ---
st.set_page_config(
    page_title="FitFusion",
    page_icon=":apple:",
    layout="centered",
)

st.title("FitFusion")
st.markdown("##### A diet and workout planning coach")


# --- Utility Functions ---
def load_default_data() -> dict:
    """Load the default user data from a JSON file."""
    default_file = Path(__file__).parent / "default_user_data.json"
    with open(default_file, "r") as f:
        return json.load(f)


def restart_agent():
    """Clears the session state and restarts the app."""
    keys_to_delete = ["stage", "fit_fusion_agent", "messages", "user_data", "pending_query"]
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()


# --- Main Application Logic ---
def main() -> None:
    # Initialize session state variables
    if "stage" not in st.session_state:
        st.session_state["stage"] = "initial"
    if "user_data" not in st.session_state:
        st.session_state["user_data"] = load_default_data()
    if "fit_fusion_agent" not in st.session_state:
        st.session_state["fit_fusion_agent"] = fitfusion_model
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # --- Initial Stage: User Data Input ---
    if st.session_state["stage"] == "initial":
        with st.form("initial_user_data_form"):
            st.write("### Personal Information")
            age = st.number_input("Age", min_value=1, max_value=120, value=st.session_state["user_data"].get("Age", 30))
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(
                st.session_state["user_data"].get("Gender", "Male")))
            height = st.text_input("Height (e.g., 170 cm)", value=st.session_state["user_data"].get("Height", "170 cm"))
            weight = st.text_input("Weight (e.g., 70 kg)", value=st.session_state["user_data"].get("Weight", "70 kg"))

            st.write("### Goals")
            primary_goal = st.text_input("Primary Goal (e.g., Lose weight)",
                                         value=st.session_state["user_data"].get("Primary Goal", "Lose weight"))
            target_weight = st.text_input("Target Weight (e.g., 65 kg)",
                                          value=st.session_state["user_data"].get("Target Weight", "65 kg"))
            timeframe = st.text_input("Timeframe (e.g., 3 months)",
                                      value=st.session_state["user_data"].get("Timeframe", "3 months"))

            st.write("### Activity Levels")
            current_physical_activity = st.text_input("Current Physical Activity (e.g., Sedentary)",
                                                      value=st.session_state["user_data"].get(
                                                          "Current Physical Activity", "Sedentary"))

            st.write("### Medical and Health Information")
            existing_medical_conditions = st.text_input("Existing Medical Conditions (e.g., None)",
                                                        value=st.session_state["user_data"].get(
                                                            "Existing Medical Conditions", "None"))
            food_allergies = st.text_input("Food Allergies (e.g., None)",
                                           value=st.session_state["user_data"].get("Food Allergies", "None"))

            st.write("### Dietary Preferences")
            diet_type = st.selectbox("Diet Type",
                                     ["Vegetarian", "Traditional", "Keto", "Mediterranean", "High-protein", "Paleo",
                                      "Omnivore"],
                                     index=["Vegetarian", "Traditional", "Keto", "Mediterranean", "High-protein",
                                            "Paleo", "Omnivore"].index(
                                         st.session_state["user_data"].get("Diet Type", "Traditional")))
            meal_frequency_preferences = st.text_input("Meal Frequency Preferences (e.g., 3 meals per day)",
                                                       value=st.session_state["user_data"].get(
                                                           "Meal Frequency Preferences", "3 meals per day"))

            st.write("### Workout Preferences")
            preferred_workout_types = st.text_input("Preferred Workout Types (e.g., Cardio, Strength)",
                                                    value=st.session_state["user_data"].get("Preferred Workout Types",
                                                                                            "Cardio, Strength"))
            current_fitness_level = st.text_input("Current Fitness Level (e.g., Beginner)",
                                                  value=st.session_state["user_data"].get("Current Fitness Level",
                                                                                          "Beginner"))
            workout_frequency = st.text_input("Workout Frequency (e.g., 3 times a week)",
                                              value=st.session_state["user_data"].get("Workout Frequency",
                                                                                      "3 times a week"))
            workout_duration = st.text_input("Workout Duration (e.g., 30 minutes)",
                                             value=st.session_state["user_data"].get("Workout Duration", "30 minutes"))

            st.write("### Lifestyle and Habits")
            sleep_patterns = st.text_input("Sleep Patterns (e.g., 7 hours per night)",
                                           value=st.session_state["user_data"].get("Sleep Patterns",
                                                                                   "7 hours per night"))
            stress_levels = st.text_input("Stress Levels (e.g., Moderate)",
                                          value=st.session_state["user_data"].get("Stress Levels", "Moderate"))
            hydration_habits = st.text_input("Hydration Habits (e.g., 2 liters per day)",
                                             value=st.session_state["user_data"].get("Hydration Habits",
                                                                                     "2 liters per day"))

            st.write("### Behavioral Insights")
            motivators = st.text_input("Motivators (e.g., Health improvement)",
                                       value=st.session_state["user_data"].get("Motivators", "Health improvement"))
            barriers = st.text_input("Barriers (e.g., Lack of time)",
                                     value=st.session_state["user_data"].get("Barriers", "Lack of time"))

            st.write("### Feedback and Customization")
            adjustability = st.text_input("Adjustability (e.g., Flexible)",
                                          value=st.session_state["user_data"].get("Adjustability", "Flexible"))
            feedback_loop = st.text_input("Feedback Loop (e.g., Weekly check-ins)",
                                          value=st.session_state["user_data"].get("Feedback Loop", "Weekly check-ins"))

            submitted = st.form_submit_button("Generate")
            if submitted:
                # Save all user data to session state
                st.session_state["user_data"] = {
                    "Age": age,
                    "Gender": gender,
                    "Height": height,
                    "Weight": weight,
                    "Primary Goal": primary_goal,
                    "Target Weight": target_weight,
                    "Timeframe": timeframe,
                    "Current Physical Activity": current_physical_activity,
                    "Existing Medical Conditions": existing_medical_conditions,
                    "Food Allergies": food_allergies,
                    "Diet Type": diet_type,
                    "Meal Frequency Preferences": meal_frequency_preferences,
                    "Preferred Workout Types": preferred_workout_types,
                    "Current Fitness Level": current_fitness_level,
                    "Workout Frequency": workout_frequency,
                    "Workout Duration": workout_duration,
                    "Sleep Patterns": sleep_patterns,
                    "Stress Levels": stress_levels,
                    "Hydration Habits": hydration_habits,
                    "Motivators": motivators,
                    "Barriers": barriers,
                    "Adjustability": adjustability,
                    "Feedback Loop": feedback_loop
                }
                # Prepare user info text for the LLM query
                data = st.session_state["user_data"]
                user_info_text = f"""
                Age: {data["Age"]}
                Gender: {data["Gender"]}
                Height: {data["Height"]}
                Weight: {data["Weight"]}
                Primary Goal: {data["Primary Goal"]}
                Target Weight: {data["Target Weight"]}
                Timeframe: {data["Timeframe"]}
                Current Physical Activity: {data["Current Physical Activity"]}
                Existing Medical Conditions: {data["Existing Medical Conditions"]}
                Food Allergies: {data["Food Allergies"]}
                Diet Type: {data["Diet Type"]}
                Meal Frequency Preferences: {data["Meal Frequency Preferences"]}
                Preferred Workout Types: {data["Preferred Workout Types"]}
                Current Fitness Level: {data["Current Fitness Level"]}
                Workout Frequency: {data["Workout Frequency"]}
                Workout Duration: {data["Workout Duration"]}
                Sleep Patterns: {data["Sleep Patterns"]}
                Stress Levels: {data["Stress Levels"]}
                Hydration Habits: {data["Hydration Habits"]}
                Motivators: {data["Motivators"]}
                Barriers: {data["Barriers"]}
                Adjustability: {data["Adjustability"]}
                Feedback Loop: {data["Feedback Loop"]}
                """
                st.session_state["pending_query"] = user_info_text
                st.session_state["stage"] = "chat"
                st.experimental_rerun()

    else:  # stage == "chat"
        # Sidebar controls
        with st.sidebar:
            st.header("Controls")
            if st.button("New Chat Session"):
                restart_agent()

            # User Information form with all fields
            with st.form("user_data_form", clear_on_submit=False):
                st.write("### Update Your Information")
                age = st.number_input("Age", min_value=1, max_value=120,
                                      value=st.session_state["user_data"].get("Age", 30))
                gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(
                    st.session_state["user_data"].get("Gender", "Male")))
                height = st.text_input("Height (e.g., 170 cm)",
                                       value=st.session_state["user_data"].get("Height", "170 cm"))
                weight = st.text_input("Weight (e.g., 70 kg)",
                                       value=st.session_state["user_data"].get("Weight", "70 kg"))

                st.write("### Goals")
                primary_goal = st.text_input("Primary Goal (e.g., Lose weight)",
                                             value=st.session_state["user_data"].get("Primary Goal", "Lose weight"))
                target_weight = st.text_input("Target Weight (e.g., 65 kg)",
                                              value=st.session_state["user_data"].get("Target Weight", "65 kg"))
                timeframe = st.text_input("Timeframe (e.g., 3 months)",
                                          value=st.session_state["user_data"].get("Timeframe", "3 months"))

                st.write("### Activity Levels")
                current_physical_activity = st.text_input("Current Physical Activity (e.g., Sedentary)",
                                                          value=st.session_state["user_data"].get(
                                                              "Current Physical Activity", "Sedentary"))

                st.write("### Medical and Health Information")
                existing_medical_conditions = st.text_input("Existing Medical Conditions (e.g., None)",
                                                            value=st.session_state["user_data"].get(
                                                                "Existing Medical Conditions", "None"))
                food_allergies = st.text_input("Food Allergies (e.g., None)",
                                               value=st.session_state["user_data"].get("Food Allergies", "None"))

                st.write("### Dietary Preferences")
                diet_type = st.selectbox("Diet Type",
                                         ["Vegetarian", "Traditional", "Keto", "Mediterranean", "High-protein", "Paleo",
                                          "Omnivore"],
                                         index=["Vegetarian", "Traditional", "Keto", "Mediterranean", "High-protein",
                                                "Paleo", "Omnivore"].index(
                                             st.session_state["user_data"].get("Diet Type", "Traditional")))
                meal_frequency_preferences = st.text_input("Meal Frequency Preferences (e.g., 3 meals per day)",
                                                           value=st.session_state["user_data"].get(
                                                               "Meal Frequency Preferences", "3 meals per day"))

                st.write("### Workout Preferences")
                preferred_workout_types = st.text_input("Preferred Workout Types (e.g., Cardio, Strength)",
                                                        value=st.session_state["user_data"].get(
                                                            "Preferred Workout Types", "Cardio, Strength"))
                current_fitness_level = st.text_input("Current Fitness Level (e.g., Beginner)",
                                                      value=st.session_state["user_data"].get("Current Fitness Level",
                                                                                              "Beginner"))
                workout_frequency = st.text_input("Workout Frequency (e.g., 3 times a week)",
                                                  value=st.session_state["user_data"].get("Workout Frequency",
                                                                                          "3 times a week"))
                workout_duration = st.text_input("Workout Duration (e.g., 30 minutes)",
                                                 value=st.session_state["user_data"].get("Workout Duration",
                                                                                         "30 minutes"))

                st.write("### Lifestyle and Habits")
                sleep_patterns = st.text_input("Sleep Patterns (e.g., 7 hours per night)",
                                               value=st.session_state["user_data"].get("Sleep Patterns",
                                                                                       "7 hours per night"))
                stress_levels = st.text_input("Stress Levels (e.g., Moderate)",
                                              value=st.session_state["user_data"].get("Stress Levels", "Moderate"))
                hydration_habits = st.text_input("Hydration Habits (e.g., 2 liters per day)",
                                                 value=st.session_state["user_data"].get("Hydration Habits",
                                                                                         "2 liters per day"))

                st.write("### Behavioral Insights")
                motivators = st.text_input("Motivators (e.g., Health improvement)",
                                           value=st.session_state["user_data"].get("Motivators", "Health improvement"))
                barriers = st.text_input("Barriers (e.g., Lack of time)",
                                         value=st.session_state["user_data"].get("Barriers", "Lack of time"))

                st.write("### Feedback and Customization")
                adjustability = st.text_input("Adjustability (e.g., Flexible)",
                                              value=st.session_state["user_data"].get("Adjustability", "Flexible"))
                feedback_loop = st.text_input("Feedback Loop (e.g., Weekly check-ins)",
                                              value=st.session_state["user_data"].get("Feedback Loop",
                                                                                      "Weekly check-ins"))

                submitted = st.form_submit_button("Update Data")
                if submitted:
                    # Update all fields in session state
                    st.session_state["user_data"].update({
                        "Age": age,
                        "Gender": gender,
                        "Height": height,
                        "Weight": weight,
                        "Primary Goal": primary_goal,
                        "Target Weight": target_weight,
                        "Timeframe": timeframe,
                        "Current Physical Activity": current_physical_activity,
                        "Existing Medical Conditions": existing_medical_conditions,
                        "Food Allergies": food_allergies,
                        "Diet Type": diet_type,
                        "Meal Frequency Preferences": meal_frequency_preferences,
                        "Preferred Workout Types": preferred_workout_types,
                        "Current Fitness Level": current_fitness_level,
                        "Workout Frequency": workout_frequency,
                        "Workout Duration": workout_duration,
                        "Sleep Patterns": sleep_patterns,
                        "Stress Levels": stress_levels,
                        "Hydration Habits": hydration_habits,
                        "Motivators": motivators,
                        "Barriers": barriers,
                        "Adjustability": adjustability,
                        "Feedback Loop": feedback_loop
                    })
                    data = st.session_state["user_data"]
                    user_info_text = f"""
                                        Generate a comprehensive 7-day diet plan and workout schedule based on the following details:
                                        ### Personal Information
                                        Age: {data["Age"]}
                                        Gender: {data["Gender"]}
                                        Height: {data["Height"]}
                                        Weight: {data["Weight"]}
                                        ### Goals
                                        Primary Goal: {data["Primary Goal"]}
                                        Target Weight: {data["Target Weight"]}
                                        Timeframe: {data["Timeframe"]}
                                        ### Activity Levels
                                        Current Physical Activity: {data["Current Physical Activity"]}
                                        ### Medical and Health Information
                                        Existing Medical Conditions: {data["Existing Medical Conditions"]}
                                        Food Allergies: {data["Food Allergies"]}
                                        ### Dietary Preferences
                                        Diet Type: {data["Diet Type"]}
                                        Meal Frequency Preferences: {data["Meal Frequency Preferences"]}
                                        ### Workout Preferences
                                        Preferred Workout Types: {data["Preferred Workout Types"]}
                                        Current Fitness Level: {data["Current Fitness Level"]}
                                        Workout Frequency: {data["Workout Frequency"]}
                                        Workout Duration: {data["Workout Duration"]}
                                        ### Lifestyle and Habits
                                        Sleep Patterns: {data["Sleep Patterns"]}
                                        Stress Levels: {data["Stress Levels"]}
                                        Hydration Habits: {data["Hydration Habits"]}
                                        ### Behavioral Insights
                                        Motivators: {data["Motivators"]}
                                        Barriers: {data["Barriers"]}
                                        ### Feedback and Customization
                                        Adjustability: {data["Adjustability"]}
                                        Feedback Loop: {data["Feedback Loop"]}
                                        """
                    st.session_state["pending_query"] = user_info_text
                    st.success("Data updated!")

        # Main area: Chat interface
        if "pending_query" in st.session_state and st.session_state["pending_query"] is not None:
            # Append the user's query to the chat messages
            st.session_state["messages"].append({"role": "user", "content": "Generate my diet and workout plan."})

            # Save the original query text to filter it out from reasoning logs
            pending_query_text = st.session_state["pending_query"]

            # List to store each reasoning step (excluding the user info text)
            steps = []

            # Create an expandable section for reasoning steps with a scrollable container
            reasoning_expander = st.expander("Reasoning Steps", expanded=True)
            reasoning_placeholder = reasoning_expander.empty()

            with st.spinner("Thinking..."):
                # query_inferences now returns a generator that yields each reasoning step
                response_gen = st.session_state["fit_fusion_agent"].query_inferences(pending_query_text)
                for step in response_gen:
                    # Skip the user_info_text if it appears in the output
                    if step.strip() == pending_query_text.strip():
                        continue

                    steps.append(step)
                    # Display all reasoning steps except the final answer inside a scrollable container
                    if len(steps) > 1:
                        reasoning_text = "\n".join(steps[:-1])
                    else:
                        reasoning_text = ""
                    scrollable_div = (
                        f'<div style="max-height:300px; overflow-y:auto; padding:10px; border:1px solid #ccc;">'
                        f'{reasoning_text}</div>'
                    )
                    reasoning_placeholder.markdown(scrollable_div, unsafe_allow_html=True)

            # The final answer is the last step (if available)
            final_answer = steps[-1] if steps else ""
            st.session_state["messages"].append({"role": "assistant", "content": final_answer})
            st.session_state["pending_query"] = None

        # Display chat messages
        for msg in st.session_state["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input for follow-up questions
        user_input = st.chat_input("Ask more questions or refine your plan...")
        if user_input:
            st.session_state["messages"].append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                response = st.session_state["fit_fusion_agent"].query_inferences(user_input)
            st.session_state["messages"].append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
