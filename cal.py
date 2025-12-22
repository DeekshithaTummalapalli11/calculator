
from flask import Flask, render_template, request
import os

app = Flask(__name__)

HISTORY_FILE = "history.txt"

def read_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return f.readlines()

def save_history(expr, result):
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{expr} = {result}\n")

def clear_history():
    open(HISTORY_FILE, "w").close()

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = ""
    expression = ""
    history = read_history()

    if request.method == "POST":
        expression = request.form["expression"]
        try:
            result = eval(expression, {"__builtins__": None}, {})
            save_history(expression, result)
            history = read_history()
        except:
            result = "Error"

    return render_template(
        "calN.html",
        result=result,
        expression=expression,
        history=history
    )

@app.route("/clear-history")
def clear_hist():
    clear_history()
    return render_template(
        "calN.html",
        result="",
        expression="",
        history=[]
    )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
