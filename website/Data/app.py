# %% FLASK and FLASK-Endpoints
import json
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from glpk_test import *

# %% Flask preparation
app = Flask(__name__, template_folder='templates', static_folder='static')
cors = CORS(app)

# %% create the website when localchost:5000 is reqeusted
@app.route("/", methods=["GET"])
def main_page():
    return render_template('index.html')

# %% Parse Json into a Dict
def parseJson(parameters):
    parameterDict = {
        "one": parameters["kontext_checkmarks"]["eins"] ,
        "two":parameters["kontext_checkmarks"]["zwei"],
        "three":parameters["kontext_checkmarks"]["drei"],
        "four":parameters["kontext_checkmarks"]["vier"],
        "maxLength":int(parameters["max_length"]),
        "percentConcepts":parameters["number_of_concepts"],
        "calcMethode":parameters["function_type"],
        "TF": parameters["represent_type"].find("tf") != -1,
        "IDF": parameters["represent_type"] =="tf-idf",
        "question":parameters["question"],
        "questionFactor":parameters["weight_of_params"]["include"],
        "exclude":parameters["exclude_params"]["params"],
        "excludeFactor":parameters["weight_of_params"]["exclude"],
        "hardexclude":parameters["exclude_params"]["hard_exclude"],
        "returnorder":parameters["return_order_of_summary"],
        "minDf":int(parameters["tf_idf"]["min_df"]),
        "maxDf":float(parameters["tf_idf"]["max_df"]),
        "startDate":parameters["timespan"]["from"]["date"]+"T"+parameters["timespan"]["from"]["time"],
        "endDate":parameters["timespan"]["to"]["date"]+"T"+parameters["timespan"]["to"]["time"],
        "Timeout": parameters["time_till_timeout_in_ms"] ,
        "toLower":parameters["use_lowercase"],
        "sentenceFactor":parameters["factor_filtering_sentences"],
        "stopwords":parameters["use_stopwordlist"],
        "dataset":parameters["dataset"]}
    return parameterDict

# %% Invoke a summaristion with the sent parameter upon a reqeust ending with /summarize
@app.route("/summarize", methods=["POST"])
def start_summarize():
   parameters_from_frontend = request.get_json()
   parameters = parameters_from_frontend
   all_parameters_set = False
   print(parameters)
   parameterDict = parseJson(parameters)
   summary_as_json = prepareDatasetAndCreateSummary(parameterDict)
   print(summary_as_json)
   return summary_as_json

# %% get datasetnames as json upon a reqeust ending with /datasets
@app.route("/datasets", methods=["GET"])
def get_datasets()->json:
    dir_list = "/usr/src/app/Datensaetze/prepared/"

    list_of_json_files = []
    for name in os.listdir(dir_list):
        # check if file is a json by checking if the string ends with .json or jsonl
        if(name.endswith(".json") or name.endswith(".jsonl")):
            list_of_json_files.append(name)

    dir_list_json = {"files": list_of_json_files}

    return jsonify(dir_list_json)

# %% Run the app:
if __name__ == "__main__":
     init()
     app.run()