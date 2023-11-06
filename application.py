import os
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from dotenv import load_dotenv

# import openai
import nltk

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
)

import json

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

application = Flask(__name__)


def createLocalIndex():
    # Define LLM properties
    # Only required when building the index
    llm_predictor = LLMPredictor(
        llm=OpenAI(temperature=0, model_name="text-davinci-003")
    )

    # define prompt helper
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_output = 256
    # set maximum chunk overlap
    max_chunk_overlap = 20
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

    SimpleDirectoryReader = download_loader("SimpleDirectoryReader")

    loader = SimpleDirectoryReader("./myFolder")

    documents = loader.load_data()
    index = GPTVectorStoreIndex(
        documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper
    )

    # Save the index to a local file
    index.save_to_disk("index_trinity_test.json")

    # Load the index from a local file
    index = GPTVectorStoreIndex.load_from_disk("index_trinity_test.json")


@application.route("/get")
def invokePersona():
    userInput = request.args.get("msg")
    persona = request.args.get("person")

    loader = DirectoryLoader(
        "data/" + persona, glob="*", show_progress=True, loader_cls=TextLoader
    )
    index = VectorstoreIndexCreator().from_loaders([loader])

    gptResponse = index.query(userInput)

    return str(gptResponse)


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
    application.run(debug=True)
