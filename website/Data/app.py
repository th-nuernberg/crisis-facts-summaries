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
   json_parameters_from_frontend = jsonify(parameters_from_frontend)

   # TO DO: feed the Data to Tobias functions
    
   a = gesamt() 
   print(a) # Zum debuggen
   return a

#Run the app:
if __name__ == "__main__":
     init()
     app.run()