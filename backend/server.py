from flask import Flask

app = Flask(__name__)

@app.route("/dupa")
def dupa():
    return {"dupcia": [True, False, True]}

if __name__ == "__main__":
    app.run(debug=True)
