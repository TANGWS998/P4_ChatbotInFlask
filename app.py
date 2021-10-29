from flask import Flask, request, make_response, jsonify
import random
from chatbot import Chatbot

app = Flask(__name__)
bot = Chatbot()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/fruit")
def generate_fruit():
    fruits = ["Apple", "Orange", "Mango", "Pineapple"]
    selected_fruit = random.choice(fruits)
    return {"fruit": selected_fruit}

@app.route("/chat", methods=["POST"])
def bot_chat():
    if request.is_json:
            requestData = request.get_json()
            queries = requestData['query']

            if queries:
                response_body = {'response': bot.chatbot_response(queries)}
                res = make_response(jsonify(response_body),201)
                return res

            else:
                # print("Incorrect data")
                return make_response(jsonify({"response": "Invalid JSON data"}), 400)
    else:
        # print("Incorrect format")
        return make_response(jsonify({"response": "Request must be JSON"}),400) 