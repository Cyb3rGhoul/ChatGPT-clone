from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo


import openai

openai.api_key = "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"



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://harsh19112003:Harsh$1911@cluster0.flegxfd.mongodb.net/chatgpt1"
mongo = PyMongo(app)


@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    myChats = [chat for chat in chats]
    print(myChats)
    return render_template("index.html", mychats = myChats)

@app.route("/api", methods=["GET", "POST"] )
def qa():
    if request.method == "POST":
        print(request.json)
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question": question})

        
        print(chat)
        if chat:
            data = {"result": f"{chat['solution']}"}
            return jsonify(data)
        else: 
            

            response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=question,
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )
            data = {"question": question, "answer": response["choices"][0]["text"]}
            mongo.db.chats.insert_one({"question": question, "answer": response["choices"][0]["text"]})
            return jsonify(data)
    data = {"Result": "Thank you! I'm glad to hear that you find me helpful. Is there anything specific you would like to chat about or any questions you have? I'm here to assist you to the best of my abilities."}
    return jsonify(data)

app.run(debug=True)