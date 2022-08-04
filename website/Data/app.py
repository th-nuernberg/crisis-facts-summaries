#FLASK and FLASK-Endpoint
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS


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
    

   # TO DO: Return Value needs to be a Json file containing the summary
   return " "


#Run the app:
if __name__ == "__main__":
     app.run()