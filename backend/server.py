from flask import Flask, send_file
import model

app = Flask(__name__)

@app.route("/bpmn")
def generate_BPMN_image():
    model.generate_BPMN("B2.csv", 0)
    return send_file('model.png', mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
