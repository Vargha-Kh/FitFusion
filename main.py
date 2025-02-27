from utils import get_prompt, get_vectorstores, FitFusionAgent
from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings
import os
from langchain.chains import HypotheticalDocumentEmbedder


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = 'default'


class FitFusion:
    """
    Langchain Model class to handle different types of language models.
    """

    def __init__(self, llm_model, vectorstore_name="weaviate", embeddings_model="openai"):
        """
        Initialize the LangchainModel class with the specified LLM model type and options.

        Args:
            llm_model (str): The type of LLM model to use.
            vectorstore_name (str): The name of the vector store to use.
            embeddings_model (str): The embeddings model to use.
        """
        self.loader = None
        self.results = None
        self.model_type = llm_model
        self.text_splitter = None
        self.model = None
        self.temperature = 0.1
        self.chain = None
        self.result = None
        self.results = None
        self.chat_history = []
        self.vectorstore_name = vectorstore_name
        self.create_db = False
        self.database_collection_name = "RAG"
        self.chunk_size = 5000
        self.embeddings_model = embeddings_model

    def model_chain_init(self, data_path, data_types):
        """
        Initialize the model chain based on the specified model type.

        Args:
            data_path (str): The path to the data directory.
            data_types (list): The list of data types to process.
        """
        self._init_fit_agent_rag_chain(data_path, data_types)

    def _select_embeddings_model(self):
        """
        Select the embeddings model based on the embeddings_model attribute.

        Returns:
            BaseEmbeddings: The selected embeddings instance.
        """
        if self.embeddings_model == "ollama":
            return OllamaEmbeddings(model=self.model_type)
        else:
            # Default to OpenAI Embeddings
            return OpenAIEmbeddings(model="text-embedding-3-small")

    def _init_fit_agent_rag_chain(self, data_path, data_types):
        """
        Initialize the FitFusion chain.

        Args:
            data_path (str): The path to the data directory.
            data_types (list): The list of data types to process.
        """
        # HyDe Embeddings
        hyde_llm = OpenAI(n=5, best_of=5)
        hyde_embeddings = HypotheticalDocumentEmbedder.from_llm(
            llm=hyde_llm,
            base_embeddings=self._select_embeddings_model(),
            prompt_key="web_search",
        )
        # Initialize vector database with embeddings
        vector_store = get_vectorstores(self.vectorstore_name, data_path, data_types, hyde_embeddings,
                                        self.database_collection_name, self.chunk_size, self.create_db)

        # Initialize AgenticRAG chain with the retriever tool
        self.chain = FitFusionAgent(vector_store.as_retriever())
        self.chain.create_graph()

    def query_inferences(self, query_input):
        """
        Perform inference based on the query input and the model type.

        Args:
            query_input (str): The query input for inference.
        """
        # Invoke the chain with the query input
        self.results = self.chain.invoke(query_input)

        # Print and return the results
        return self.results


dummy_user_info = f"""
        Generate Diet plan with full instruction and scheduling based on the information:
        ### Personal Information
        Age: 25
        Gender: Male
        Height: 180 cm
        Weight: 70 kg

        ### Goals
        Primary Goal: Muscle Gain
        Target Weight: 78 kg
        Timeframe: 3 months

        ### Activity Levels
        Current Physical Activity: Moderately active (fitness enthusiast)

        ### Medical and Health Information
        Existing Medical Conditions: None
        Food Allergies: None

        ### Dietary Preferences
        Diet Type: Omnivore
        Meal Frequency Preferences: 3 meals + 2 snacks

        ### Workout Preferences
        Preferred Workout Types: Cardio, Strength training
        Current Fitness Level: Beginner
        Workout Frequency: 3 days/week
        Workout Duration: ~45 min

        ### Lifestyle and Habits
        Sleep Patterns: ~8 hours
        Stress Levels: low
        Hydration Habits: ~3L water/day

        ### Metrics and Tracking
        Current Weight: 78 kg

        ### Behavioral Insights
        Motivators: General Health, Appearance
        Barriers: Time constraints (office job)

        ### Feedback and Customization
        Adjustability: Willing to adjust plan each month
        Feedback Loop: Weekly weigh-ins and monthly measurements
        """

# if __name__ == "__main__":
#     """
#     Main function to run Langchain Model.
#     """
#     directory, model_type, vectorstore, file_formats = './diet', 'gpt-4o', 'weaviate', ['txt']
#     # Langchain model init
#     fitfusion_model = FitFusion(llm_model=model_type, vectorstore_name=vectorstore)
#     fitfusion_model.model_chain_init(directory, data_types=file_formats)
    # fitfusion_model.query_inferences(dummy_user_info)
    # while True:
    #     query = input("Please ask your question! ")
    #     llm.query_inferences(query)
