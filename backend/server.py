import os
from flask import Flask, request, send_file
import model
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app, resources=r'/*', headers='Content-Type')

app.config["TRACES_DIRECTORY"] = "./traces"
app.config["THRESHOLD_HEADER"] = "Threshold"

@app.route("/bpmn", methods=["POST"])
def bpmn():

    if request.method == "POST":

        if request.files:

            #Note - this requires the frontend upload to set the name property of an input to "traces"
            traces = request.files["traces"]
            filepath = os.path.join(app.config["TRACES_DIRECTORY"], traces.filename)
            traces.save(filepath)

            #Note - this requires the frontend upload to set the custom header called "Threshold" with a numeric value representing the event threshold
            threshold = int(request.headers[app.config["THRESHOLD_HEADER"]])

            model.generate_BPMN(filepath, threshold)
            return send_file('model.png', mimetype='image/png')
        
        return "No input file provided", 400
    
    return "Resource not found", 404

if __name__ == "__main__":
    app.run(debug=True)
