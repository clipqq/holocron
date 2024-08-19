import os
from flask import Flask, request, render_template, send_from_directory
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI
from llama_index.legacy import LLMPredictor, PromptHelper, VectorStoreIndex
from langchain_community.embeddings import OpenAIEmbeddings
import prompts

# Load environment variables from a .env file
load_dotenv()

# Initialize Flask application
application = Flask(__name__)


def createLocalIndex():
    # Initialize the LLM with the system message incorporated
    llm = ChatOpenAI(
        temperature=0.3, model_name=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    )

    # Create an LLMPredictor with the system message as part of the prompt
    llm_predictor = LLMPredictor(
        llm=llm,
        prompt_template=prompts.system_message,  # Incorporate system message directly
    )

    # Define prompt helper
    max_input_size = 4096
    num_output = 256
    max_chunk_overlap = 20
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

    # Load documents using SimpleDirectoryReader
    loader = SimpleDirectoryReader(input_dir="./data", recursive=True)

    documents = loader.load_data()
    if not documents:
        print("No documents found in the specified folder.")
        return

    # Create the index using the LLM predictor with the system message
    index = VectorStoreIndex(
        documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper
    )

    # Save the index to a local file
    index.save_to_disk("index_trinity_test.json")

    # Optionally load the index from a local file (if needed elsewhere)
    index = VectorStoreIndex.load_from_disk("index_trinity_test.json")


@application.route("/get")
def invokePersona():
    userInput = request.args.get("msg")
    persona = request.args.get("person")

    # Initialize the embedding model
    embedding_model = OpenAIEmbeddings()

    # Initialize the LLM with system message support
    llm = ChatOpenAI(temperature=0.3)

    # Define the system message to guide the LLM (used in chat mode)
    system_message = {
        "role": "system",
        "content": prompts.system_message,
    }

    # Create the user's message
    user_message = {"role": "user", "content": userInput}

    # Load documents for the persona
    try:
        loader = DirectoryLoader(
            os.path.join("data", persona),
            glob="*",
            show_progress=True,
            loader_cls=TextLoader,
        )

        # Create the index using the embedding model
        index_creator = VectorstoreIndexCreator(embedding=embedding_model)
        index = index_creator.from_loaders([loader])

        # Extract the user's query string
        query_string = user_message["content"]

        # Query the index with the LLM using the query string
        gptResponse = index.query(query_string, llm=llm)
        return str(gptResponse)

    except Exception as e:
        return f"An error occurred: {str(e)}"


@application.route("/")
def index():
    print("Request for index page received")
    return render_template("index.html")


@application.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(application.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    print("Using model:", os.getenv("OPENAI_MODEL"))
    application.run(debug=True)
