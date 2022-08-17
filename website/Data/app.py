#FLASK and FLASK-Endpoint
import json
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
def start_summaraize():
   parameters_from_frontend = request.get_json()
   parameters = parameters_from_frontend[0]

   # summary_as_json is currently not in a valid JSON format. Pls Fix that
   summary_as_json = gesamt(ngamms=int(parameters["ngrams"]),max_length=int(parameters["max_length"])) 
   print(summary_as_json) # Zum debuggen
   return summary_as_json

#Run the app:
if __name__ == "__main__":
     init()
     app.run()