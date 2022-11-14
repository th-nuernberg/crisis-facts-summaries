## Docker
The Dockerfile that should be used to create an image is in the folder website. There is also a Readme for the Dockerfile
explaining how it can be used.

## Frontend
The files for the forntend can be found under website/data. The html file for the website can be found in the folder templates.
The css-file is found in the folder static together with the folder containing the Node.js-modules. Also the icon and pictures 
used in the website can be found there. In website/data is folder containing the JavaScript file used to implement the frontend 
logic for sending the parameters to the backend, dispaling the results and creating the diagramm.

## Backend
In website/data is the file app.py this is used for flask to manage the communication between front and backend and the creation of the website.
The file glpk_test.py is the file used to create summaries with the diffrent parameters and getting the data for the diagramm. 

## Other Folders
In the log folder are files used during the development.
In the Archive folder is file called format_json.txt, which contains an example how the entries of a text corpus
for this application should look like. The corpus should be stored in a file with a json or jsonl ending. The file named
download.py helps you to download 8 text corpi for the application to run on. Inorder to get them in the right format 
use the script transform_Json.py.