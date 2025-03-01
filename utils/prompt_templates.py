

multi_query = """You are an AI language model assistant. Your task is to generate five 
            different versions of the given user question to retrieve relevant documents from a vector 
            database. By generating multiple perspectives on the user question, your goal is to help
            the user overcome some of the limitations of the distance-based similarity search. 
            Provide these alternative questions separated by newlines.
            Original question: {input}"""

condense_question_system_template = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

planner_prompt_template = """
        You are tasked with creating a step-by-step plan to develop a diet and workout routine. This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
        The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

        The user asked:
        {question}

        Relevant documents and knowledge:
        {documents}

        Please provide a detailed and actionable plan that considers user goals, medical constraints, preferences, and any other important factors.
        """

reflection_prompt_template = """
You are an expert in diet and workout planning. Reflect on the provided plan. 
Critique the plan based on the following factors:
- Does the plan provide a clear and detailed meal schedule for one week?
- Are the meal ingredients mentioned and are they feasible?
- Does the plan meet any stated medical constraints or preferences?
- Are there any missing details or superfluous information?
- Are the plan is complete for full 7 days?
- Are there different meals for each day?
- Are enough specific detail for meals and their ingredient?

Plan:
{plan}

Please provide a reflection with critiques and suggestions for improvement. If necessary, revise the plan to include missing details and remove unnecessary information.
"""

generation_prompt_template = """
        شما یک متخصص در برنامه ریزی رژیم غذایی و تمرینات ورزشی هستید.

        سوال کاربر:
        {question}

        مراحل برنامه ریزی:
        {plan}

        دانش و اسناد مرتبط:
        {documents}

        بر اساس برنامه، یک پاسخ جامع ارائه دهید که شامل موارد زیر باشد:

        🍽️ برنامه رژیم غذایی:
        ---------------------
        • وعده های غذایی روزانه
        • مواد غذایی و میزان مصرف
        • زمان بندی وعده ها

        💪 برنامه تمرینات ورزشی:
        -----------------------
        • تمرینات روزانه 
        • تعداد ست و تکرار
        • مدت زمان هر تمرین

        ⚕️ ملاحظات پزشکی:
        ----------------
        • محدودیت های پزشکی
        • توصیه های ایمنی

        ❓ سوالات تکمیلی:
        ---------------
        • هرگونه سوال برای شفاف سازی بیشتر
        """

generation_prompt_template = """
        You are an expert diet and workout planner.

        User Question:
        {question}

        Planning steps:
        {plan}

        Relevant knowledge/documents:
        {documents}

        Based on the plan, provide a comprehensive answer that includes:
         - A practical diet plan,
         - A detailed workout routine,
         - Medical constraints or considerations,
         - Any clarifying questions if necessary.
         - Response must be Persian
        """

prompts_dictionary = {
    "multi_query": multi_query,
    "condense_question": condense_question_system_template,
    "planning": planner_prompt_template,
    "reflection": reflection_prompt_template,
    "generation": generation_prompt_template

}


# Function to call a prompt by name
def get_prompt(prompt_name):
    """Retrieve and execute a prompt function by name."""
    if prompt_name in prompts_dictionary:
        return prompts_dictionary[prompt_name]
    else:
        return "Prompt not found."
