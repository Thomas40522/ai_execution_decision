from flask import Flask, request, jsonify
from decision import decide_execution

app = Flask(__name__)

@app.route("/decide", methods=["POST"])
def decide():
    data = request.json

    action = data.get("action", "")
    message = data.get("message", "")
    history = data.get("history", [])
    user_state = data.get("user_state", {})

    result = decide_execution(action, message, history, user_state)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)