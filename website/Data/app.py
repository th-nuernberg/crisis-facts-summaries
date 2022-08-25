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
   parameters = parameters_from_frontend
   all_parameters_set = False


   
   # Startupcheck -> Testet ob alle Parameter existieren, wenn das nicht der Fall ist und diese trotzdem an gesamt() übergeben werden gibt es einen Fehler, da int(NULL) angewendet wird
   
   for element in parameters: 
        if parameters[element] != "":
            all_parameters_set = True
        else:
            all_parameters_set = False
            break

   print("All Parameters set ?")
   print(all_parameters_set)
   
   if all_parameters_set == True:
        summary_as_json = gesamt(ngamms=int(parameters["ngrams"]),max_length=int(parameters["max_length"])) 
        print(":)")
   else:
        summary_as_json = gesamt()
        print(":(")

   print(summary_as_json) # Zum debuggen
   return summary_as_json

#Run the app:
if __name__ == "__main__":
     init()
     app.run()