#FLASK and FLASK-Endpoints
import json
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from glpk_test import *

app = Flask(__name__, template_folder='templates', static_folder='static')
cors = CORS(app)

#localchost:5000
@app.route("/", methods=["GET"])
def main_page():
    return render_template('index.html')

@app.route("/summarize", methods=["POST"])
def start_summarize():
   parameters_from_frontend = request.get_json()
   parameters = parameters_from_frontend
   all_parameters_set = False
   print(parameters)
   summary_as_json = gesamt(eins=parameters["kontext_checkmarks"]["eins"], 
                        zwei=parameters["kontext_checkmarks"]["zwei"],
                        drei=parameters["kontext_checkmarks"]["drei"],
                        vier=parameters["kontext_checkmarks"]["vier"],
                        max_length=int(parameters["max_length"]),
                        percentConcepts=parameters["number_of_concepts"],  
                        question=parameters["question"],
                        exclude=parameters["exclude_params"],
                        returnorder=parameters["return_order_of_summary"],
                        Datensatz=parameters["dataset"]
                        )
   print(summary_as_json) # Zum debuggen
   return summary_as_json


@app.route("/datasets", methods=["GET"])
def get_datasets()->json:
    #get datasetnames as json
    
    #momentan nicht korrekter Pfad, weil nicht genau klar welche Datensätze jetzt genutzt werden sollen
    #relative Pfade funktionieren noch nicht richtig, deswegen über current working directory (cwd)
    
    curr_path = os.path.abspath(os.getcwd())
    curr_path+="\Datensaetze"
    dir_list = "/usr/src/app/Datensaetze/prepared/" #os.listdir(curr_path)
    
    #until dataset file structure is cleaned, chekc if file is a json by checking if the string ends with .json
    list_of_json_files = []
    for name in os.listdir(dir_list):
        if(name.endswith(".json") or name.endswith(".jsonl")):
            list_of_json_files.append(name)


    dir_list_json = {"files": list_of_json_files}

    return jsonify(dir_list_json)

#Run the app:
if __name__ == "__main__":
     init()
     app.run()