from utils import get_prompt, get_vectorstores, FitFusionAgent
from utils.tools import *
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings
import os
import openai

# Set API Keys
os.environ[
    "OPENAI_API_KEY"] = "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"
# os.environ["OPENAI_API_KEY"] = "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"
os.environ["TAVILY_API_KEY"] = "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"
os.environ["LANGSMITH_API"] = "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"
os.environ["COHERE_API_KEY"] = "JV4zDNnW13pe5kyjOkj4Yf2FX4pAcroV8oQevj7F"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = 'default'

openai.proxy = {
    "http": f"socks5h://127.0.0.1:8087",
    "https": f"socks5h://127.0.0.1:8087"
}


class FitFusion:
    """
    Langchain Model class to handle different types of language models.
    """

    def __init__(self, llm_model, vectorstore_name="weaviate", embeddings_model="openai", use_mongo_memory=False,
                 use_cohere_rank=False, use_multi_query_retriever=False, use_contextual_compression=False,
                 use_hyde=False):
        """
        Initialize the LangchainModel class with the specified LLM model type and options.

        Args:
            llm_model (str): The type of LLM model to use.
            vectorstore_name (str): The name of the vector store to use.
            embeddings_model (str): The embeddings model to use.
            use_mongo_memory (bool): Whether to use MongoDB for chat history.
            use_cohere_rank (bool): Whether to use Cohere Rank for retriever compression.
            use_multi_query_retriever (bool): Whether to use MultiQueryRetriever.
            use_contextual_compression (bool): Whether to use Contextual Compression Retriever.
            use_hyde (bool): Whether to Hypothetical Embedding for documents
        """
        self.loader = None
        self.llm = OpenAI()
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
        self.use_mongo_memory = use_mongo_memory
        self.use_cohere_rank = use_cohere_rank
        self.use_multi_query_retriever = use_multi_query_retriever
        self.use_contextual_compression = use_contextual_compression
        self.use_hyde = use_hyde
        self.embeddings_model = embeddings_model

    def model_chain_init(self, data_path, data_types):
        """
        Initialize the model chain based on the specified model type.

        Args:
            data_path (str): The path to the data directory.
            data_types (list): The list of data types to process.
        """
        self._init_agentic_rag_chain(data_path, data_types)

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

    def _init_agentic_rag_chain(self, data_path, data_types):
        """
        Initialize the AgenticRAG chain.

        Args:
            data_path (str): The path to the data directory.
            data_types (list): The list of data types to process.
        """
        # Initialize vector database with embeddings
        vector_store = get_vectorstores(self.vectorstore_name, data_path, data_types, OpenAIEmbeddings(),
                                        self.database_collection_name, self.chunk_size, self.create_db)

        # Create a retriever tool for the agent
        retriever_tool = create_retriever_tool(vector_store.as_retriever(), f"{os.path.basename(data_path)}",
                                               f"Searches and returns answers from {os.path.basename(data_path)} document.")

        # Initialize AgenticRAG chain with the retriever tool
        self.chain = FitFusionAgent(vector_store.as_retriever(), retriever_tool)
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
        print(self.results)
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


def main():
    """
    Main function to run Langchain Model.
    """
    directory, model_type, vectorstore, file_formats = './diet', 'gpt-4o', 'weaviate', ['txt']
    # Langchain model init
    llm = FitFusion(llm_model=model_type, vectorstore_name=vectorstore)
    llm.model_chain_init(directory, data_types=file_formats)
    llm.query_inferences(dummy_user_info)
    # while True:
    #     query = input("Please ask your question! ")
    #     llm.query_inferences(query)


if __name__ == "__main__":
    main()
