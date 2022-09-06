#FLASK and FLASK-Endpoint
import json
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from glpk_test import *

app = Flask(__name__, template_folder='templates', static_folder='static')
cors = CORS(app)

#localchost:500
@app.route("/", methods=["GET"])
def main_page():
    return render_template('index.html')

@app.route("/summarize", methods=["POST"])
def start_summarize():
   parameters_from_frontend = request.get_json()
   parameters = parameters_from_frontend
   all_parameters_set = False

   summary_as_json = gesamt(ngamms=int(parameters["ngrams"]),max_length=int(parameters["max_length"]))
   print(summary_as_json) # Zum debuggen
   return summary_as_json


@app.route("/datasets", methods=["GET"])
def get_datasets():
    #get datasetnames as json
    
    #momentan nicht korrekter Pfad, weil nicht genau klar welche Datensätze jetzt genutzt werden sollen
    #relative Pfade funktionieren noch nicht richtig -> Überarbeiten
    path = "./website/Datensaetze/prepared"
    dir_list = os.listdir(path)
    dir_list_json = {"files": dir_list}

    return json.dumps(dir_list_json)

#Run the app:
if __name__ == "__main__":
     init()
     app.run()