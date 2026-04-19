from flask import Flask, request, jsonify
from flask_cors import CORS
from decision import decide_execution

app = Flask(__name__)
CORS(app)

@app.route("/decide", methods=["POST"])
def decide():
    data = request.json

    message = data.get("message", "")
    context = data.get("context", [])
    
    result = decide_execution(message, context)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)