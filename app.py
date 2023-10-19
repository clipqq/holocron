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

import json

OpenAI.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)


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


@app.route("/hello", methods=["POST"])
def hello():
    userInput = request.form.get("user-input")

    # loader = TextLoader('data.txt')
    loader = DirectoryLoader(
        "data/benjamin-graham", glob="*", show_progress=True, loader_cls=TextLoader
    )
    index = VectorstoreIndexCreator().from_loaders([loader])

    # gptRes = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": userInput}],
    # )
    # gptContent = gptRes["choices"][0]["message"]["content"]
    # print(gptContent)

    gptResponse = index.query(userInput)
    print(gptResponse)

    if userInput:
        print("Request for input page received: " + userInput)
        return render_template("hello.html", input=userInput, output=gptResponse)
    else:
        print("Request for input page received with empty input -- redirecting")
        return redirect(url_for("index"))


@app.route("/get")
def invokePersona():
    persona = "steve-jobs"

    # if name is not None:
    #     persona = name

    userInput = request.args.get("msg")

    loader = DirectoryLoader(
        "data/" + persona, glob="*", show_progress=True, loader_cls=TextLoader
    )
    index = VectorstoreIndexCreator().from_loaders([loader])

    gptResponse = index.query(userInput)

    return str(gptResponse)


if __name__ == "__main__":
    app.run(debug=True)
