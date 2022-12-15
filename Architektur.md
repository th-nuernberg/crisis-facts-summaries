In the beginnign of each line the relative path to a file is given.
Any important file is listed here.

## Docker
website/Dockerfile:     The Dockerfile that should be used to create an image is in the folder website. 
website/Readme.txt:     There is also a Readme for the Dockerfileexplaining how it can be used.

## Frontend
website/data/templates/index.html:                      The html file is the foundation of the website.
website/data/static/first_design.css:                   The used for the cosmetics of the website.
website/data/static/node_modules:                       The Node.js-modules used for the website.
website/data/static/th_ohm_logo.png:                    The ohm logo used for the website.
website/data/static/Icon_from_web.ico:                  The icon used for the website.
website/data/static/javascript/summarize_script.js:     This is the file containing the javascript code powering the frontend.

## Backend
website/data/app.py:                        This file is used for flask to manage the communication between front and backend.
website/data/text_corpus_summarization.py:  This file is used to create summaries with the diffrent parameters and getting the data for the diagramm. 

## Other Folders
log:                            In the log folder are files used during the development.
Archive/format_json.txt:        This contains an example of how the entries of a text corpus for this application should look like. The corpus should be stored in a file with a json or jsonl ending. 
Archive/download.py:            The file helps you to download 8 text corpi for the application to run on. 
Archive/transform_Json.py:      Inorder to get text corpi in the right format use the script transform_Json.py.
Archive/run.py:                 Helps to bring the datasets that can be downloaded with form this https://sites.google.com/site/temporalsummarization/downloads website into a Jsonformat. 
Archive/prepare.py:             Helps with cleaning the content of the Jsonfiles.