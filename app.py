import os
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
)

from langchain.document_loaders import TextLoader, DirectoryLoader, JSONLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from llama_index import (
    GPTVectorStoreIndex,
    download_loader,
    LLMPredictor,
    PromptHelper,
    load_index_from_storage,
    load_indices_from_storage,
    load_graph_from_storage,
)


OpenAI.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


def createLocalIndex(persona):
    print("called createLocalIndex...")
    dataDirectory = "data/" + persona
    indexJson = persona + "_index.json"

    # define prompt helper
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_output = 256
    # set maximum chunk overlap
    max_chunk_overlap = 0.1
    # set chunk token size
    chunk_size_limit = 600
    prompt_helper = PromptHelper(
        max_input_size, num_output, max_chunk_overlap, chunk_size_limit=chunk_size_limit
    )
    print("set prompt helper...")

    # Define LLM properties
    # Only required when building the index
    llm_predictor = LLMPredictor(
        llm=OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=num_output)
    )
    print("set llm_predictor...")

    SimpleDirectoryReader = download_loader("SimpleDirectoryReader")

    loader = SimpleDirectoryReader(dataDirectory)

    documents = loader.load_data()

    print("document loader created...")

    index = GPTVectorStoreIndex(
        documents,
        llm_predictor=llm_predictor,
        prompt_helper=prompt_helper,
        verbose=True,
    )

    print("index created...")

    # Save the index to a local file
    # index.save_to_disk(indexJson)
    # using new save syntax
    # if not os.path.isfile(os.path.join(dataDirectory, indexJson)):
    print("persona json not found, making one...")
    index.storage_context.persist(persist_dir=dataDirectory)
    print("saved new index in: " + dataDirectory)

    # # Load the index from a local file
    # index = GPTVectorStoreIndex.load_from_disk(indexJson)

    return index


@app.route("/get")
def invokePersona():
    print("invoking Persona...")

    userInput = request.args.get("msg")
    persona = request.args.get("person")

    dataDirectory = "data/" + persona

    # create index Json if not already in directory

    createLocalIndex(persona)

    # Load the index from a local file
    print("loading persona index...")
    index = load_index_from_storage(dataDirectory)

    while True:
        gptResponse = index.query(userInput, response_mode="compact", verbose=True)

        print("user asked: " + userInput)
        print("response is: " + gptResponse)

        return str(gptResponse)


@app.route("/")
def index():
    print("Request for index page received")
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    app.run(debug=True)
