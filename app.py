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

    # --- Initial Stage: Essential User Data Input ---
    if st.session_state["stage"] == "initial":
        with st.form("initial_user_data_form"):
            st.write("### Enter Your Details")
            age = st.number_input("Age", min_value=1, max_value=120, value=st.session_state["user_data"].get("Age", 30))
            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"],
                index=["Male", "Female", "Other"].index(st.session_state["user_data"].get("Gender", "Male"))
            )
            height = st.text_input("Height (e.g., 170 cm)", value=st.session_state["user_data"].get("Height", "170 cm"))
            weight = st.text_input("Weight (e.g., 70 kg)", value=st.session_state["user_data"].get("Weight", "70 kg"))
            primary_goal = st.text_input("Primary Goal (e.g., Lose weight)",
                                         value=st.session_state["user_data"].get("Primary Goal", "Lose weight"))
            diet_type = st.selectbox(
                "Diet Type",
                ["Vegetarian", "Traditional", "Keto", "Mediterranean", "High-protein", "Paleo", "Omnivore"],
                index=["Vegetarian", "Traditional", "Keto", "Mediterranean", "High-protein", "Paleo", "Omnivore"].index(
                    st.session_state["user_data"].get("Diet Type", "Traditional"))
            )
            workout_types = st.text_input("Preferred Workout Types (e.g., Cardio, Strength)",
                                          value=st.session_state["user_data"].get("Preferred Workout Types",
                                                                                  "Cardio, Strength"))
            
            submitted = st.form_submit_button("Generate")
            if submitted:
                # Save essential user data to session state
                st.session_state["user_data"] = {
                    "Age": age,
                    "Gender": gender,
                    "Height": height,
                    "Weight": weight,
                    "Primary Goal": primary_goal,
                    "Diet Type": diet_type,
                    "Preferred Workout Types": workout_types
                }
                # Prepare user info text for the LLM query
                user_info_text = f"""
                Age: {age}
                Gender: {gender}
                Height: {height}
                Weight: {weight}
                Primary Goal: {primary_goal}
                Diet Type: {diet_type}
                Preferred Workout Types: {workout_types}
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

            # User Information update form (simplified or expanded as needed)
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
                primary_goal = st.text_input("Primary Goal (e.g., Lose weight)",
                                             value=st.session_state["user_data"].get("Primary Goal", "Lose weight"))
                diet_type = st.selectbox("Diet Type",
                                         ["Vegetarian", "Traditional", "Keto", "Mediterranean", "High-protein", "Paleo", "Omnivore"],
                                         index=["Vegetarian", "Traditional", "Keto", "Mediterranean", "High-protein", "Paleo", "Omnivore"].index(
                                             st.session_state["user_data"].get("Diet Type", "Traditional")))
                workout_types = st.text_input("Preferred Workout Types (e.g., Cardio, Strength)",
                                              value=st.session_state["user_data"].get("Preferred Workout Types", "Cardio, Strength"))
                submitted = st.form_submit_button("Update Data")
                if submitted:
                    # Update essential fields in session state
                    st.session_state["user_data"].update({
                        "Age": age,
                        "Gender": gender,
                        "Height": height,
                        "Weight": weight,
                        "Primary Goal": primary_goal,
                        "Diet Type": diet_type,
                        "Preferred Workout Types": workout_types
                    })
                    data = st.session_state["user_data"]
                    user_info_text = f"""
                                        Generate a comprehensive 7-day diet plan and workout schedule based on the following details:
                                        Age: {data["Age"]}
                                        Gender: {data["Gender"]}
                                        Height: {data["Height"]}
                                        Weight: {data["Weight"]}
                                        Primary Goal: {data["Primary Goal"]}
                                        Diet Type: {data["Diet Type"]}
                                        Preferred Workout Types: {data["Preferred Workout Types"]}
                                        """
                    st.session_state["pending_query"] = user_info_text
                    st.success("Data updated!")

        # Main area: Chat interface
        if "pending_query" in st.session_state and st.session_state["pending_query"] is not None:
            # Add the user request to the chat
            st.session_state["messages"].append({"role": "user", "content": "Generate my diet and workout plan."})
            pending_query_text = st.session_state["pending_query"]

            steps = []
            reasoning_expander = st.expander("Reasoning Steps", expanded=True)
            reasoning_placeholder = reasoning_expander.empty()

            with st.spinner("Thinking..."):
                response_gen = st.session_state["fit_fusion_agent"].query_inferences(pending_query_text)
                for step in response_gen:
                    # Filter out the entire user prompt (if the agent parrots it)
                    if step.strip() == pending_query_text.strip():
                        continue

                    steps.append(step)
                    # Display intermediate steps in a scrollable container
                    if len(steps) > 1:
                        reasoning_text = "\n".join(steps[:-1])
                    else:
                        reasoning_text = ""
                    scrollable_div = (
                        f'<div style="max-height:300px; overflow-y:auto; padding:10px; border:1px solid #ccc;">'
                        f'{reasoning_text}</div>'
                    )
                    reasoning_placeholder.markdown(scrollable_div, unsafe_allow_html=True)

            # The final answer is the last step
            final_answer = steps[-1] if steps else ""
            st.session_state["messages"].append({"role": "assistant", "content": final_answer})
            st.session_state["pending_query"] = None

        # Display conversation
        for msg in st.session_state["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input for follow-up
        user_input = st.chat_input("Ask more questions or refine your plan...")
        if user_input:
            st.session_state["messages"].append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                response = st.session_state["fit_fusion_agent"].query_inferences(user_input)
            st.session_state["messages"].append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
