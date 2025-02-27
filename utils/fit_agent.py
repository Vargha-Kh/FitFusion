import pprint
from langgraph.types import interrupt
from langchain_core.output_parsers import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI
from langgraph.graph import END, StateGraph
from typing import Annotated, Sequence, TypedDict, List, Literal
from .prompt_templates import get_prompt
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
    """
    question: str
    generation: str
    plan: str
    documents: List[str]


class FitFusionAgent:
    def __init__(self, retriever):
        # Initialize tools and other configurations
        self.retriever = retriever
        self.app = None
        self.memory_config = None
        self.llm_model = "gpt-4o-mini"
        self.output_response = ""
        self.reflection_step = None  # Add a placeholder for the reflection step

    def retrieve(self, state):
        """
        Retrieve documents

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, documents, that contains retrieved documents
        """
        print("---RETRIEVE---")
        question = state["question"]

        # Retrieval
        documents = self.retriever.invoke(question)
        return {"documents": documents, "question": question}

    def planning(self, state):
        """
        Create a step-by-step plan based on the user question and retrieved documents.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, plan, which contains the planning steps
        """
        print("---PLANNING---")
        question = state["question"]
        documents = state["documents"]

        planning_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", get_prompt("planning")),
                ("human", "User question: {question}\nRetrieved documents: {documents}"),
            ]
        )

        # Execute the planning LLM
        llm = ChatOpenAI(model_name=self.llm_model, temperature=0, streaming=True)
        chain = planning_prompt | llm | StrOutputParser()

        plan = chain.invoke({"question": question, "documents": documents})
        return {"documents": documents, "question": question, "plan": plan}

    def reflection(self, state):
        """
        Perform reflection on the generated plan.

        Args:
            state (dict): The current graph state, including generated plan

        Returns:
            state (dict): Refined plan after critique and revision
        """
        print("---REFLECTION---")
        plan = state["plan"]

        reflection_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", get_prompt("reflection")),
                ("human", "Plan: {plan}"),
            ]
        )

        # Execute reflection LLM
        llm = ChatOpenAI(model_name=self.llm_model, temperature=0, streaming=True)
        chain = reflection_prompt | llm | StrOutputParser()

        reflection = chain.invoke({"plan": plan})
        return {"documents": state["documents"], "question": state["question"], "plan": reflection}

    def generate_diet_and_workout(self, state):
        """
        Generate the diet and workout plan based on the planning step.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Includes the final generated plan
        """
        print("---GENERATE DIET AND WORKOUT PLAN---")
        question = state["question"]
        documents = state["documents"]
        plan = state["plan"]
        # Add Persian structure to the generation prompt

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", get_prompt("generation")),
                ("human", "User question: {question}\nPlan: {plan}\nDocuments: {documents}"),
            ]
        )

        llm = ChatOpenAI(model_name=self.llm_model, temperature=0, streaming=True)
        chain = prompt | llm | StrOutputParser()

        generation = chain.invoke({"question": question, "plan": plan, "documents": documents})
        return {"documents": documents, "question": question, "generation": generation}

    def create_graph(self):
        workflow = StateGraph(GraphState)
        # Adding nodes
        workflow.add_node("retrieve", self.retrieve)  # retrieval
        workflow.add_node("planner", self.planning)  # planning step
        workflow.add_node("reflection", self.reflection)  # reflection step
        workflow.add_node("generatePlan", self.generate_diet_and_workout)  # generate step

        # Defining edges
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "planner")
        workflow.add_edge("planner", "reflection")
        workflow.add_edge("reflection", "generatePlan")
        workflow.add_edge("generatePlan", END)

        # Setup checkpoint store
        memory = MemorySaver()
        # Compiling the Agent
        self.app = workflow.compile(checkpointer=memory)
        self.memory_config = {"configurable": {"thread_id": "diet_workout_thread"}}
        self.app.get_state(self.memory_config)


    def invoke(self, input_query: str) -> str:
        """
        Main entry for user queries. We push the user’s message
        into the graph and stream the outputs from each node
        until we reach the end.
        """
        inputs = {"question": input_query}
        for output in self.app.stream(inputs, self.memory_config):
            for key, value in output.items():
                pprint.pprint(f"Output from node '{key}':")
                if "plan" in value or "generation" in value:
                    output_msg = value.get("plan", value.get("generation"))
                    pprint.pprint(output_msg)
                    self.output_response += str(output_msg) + "\n"
                pprint.pprint("\n---\n")

        return self.output_response
