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

import os

os.environ['OPENAI_API_KEY'] = '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'

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
    index.storage_context.persist(persist_dir=dataDirectory) 
    print("saved new index: " + indexJson)

    return index


createLocalIndex('barack-obama')