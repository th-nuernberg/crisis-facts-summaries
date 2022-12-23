Crisis Facts

## Description
The Crisis Facts application is a tool to create a summary of the text corpus about a certain event. The many parameters allow you to test which effect any common parameter has on
the quality of the created summary and the runtime. Additionaly, it shows in a diagramme at which time the texts of the corpus were created. 

## Installation
Before running files without docker and webapplication, install python 3 and install all needed packages with the following commands:

pip install flask
pip install flask-cors
pip install pymprog
pip install nltk
pip install -U scikit-learn
pip install -U spacy
python3 -m nltk.downloader popular

In order to run the application with minimal effort download docker and use:

docker build -t <name> .

to create an image in the folder website. If you build the image successfully, you can create an container with the command:

docker run -v <PathToDocuments>:/usr/src/app/Datensaetze/prepared/ -p 5000:5000 <ImageName>

in order to get a working application. You can open the website in the docker container or with localhost over port 5000. If you are lacking datasets download them at the Crisis Facts website and transform them to fit the needs of the application with the scripts in the folder archive. Then you can open the website and start experimenting.

## Usage
If you want to have a summary without thinking too much about the internals ignore the "more options" button and hit the "Analyze" button. Soon there will be summary at the bottom
of the website. If you want to get a grip on the effects of some parameter hit the "more options" button and change the parameters as you please. Note any decrease in runtime 
will likely cause the summary to get worse. There are a few options that should be explained a little bit further:

Demo examples: This parameter can be used to give a quick Demonstration of the programm. It overrides other settings and can only be used if the two datasets 26.relonly.jsonl and 39.relonly.jsonl exist.
Number of concepts to consider: N-grams represent concepts. If the runtime is long try reducing them with this parameter
Min DF:  Although best known with the TF-IDF representation, we implemented this for all representations in order to filter less frequently occurring concepts. 
Max DF in %: Although best known with the TF-IDF representation, we implemented this for all representations in order to filter too frequently occurring concepts.
Positive factor of the Search Keywords: With this factor you decide how important it is to have the key words in the summary.
Negative factor of the Exclude Keywords: With this factor you decide how important it is to not have the key words in the summary.
Factor for filtering sentences: In order to reduce the runtime, we only include the most promising sentences in the final algorytihmen. This factor decides 
    How many times higher than the average sentence the sentences need to score in order to be included in the final calculation.
Hard Exclude instead of lower rating of the parameters: This removes any sentences containing the key words improving runtime.

## Support
There is no support for the application. However in this folder is a file describing the architecture of this procject.

## Roadmap
Future Releases may include a suggestion on which parameters will likely yield the best results and which yield the best result per minute of runtime.
Another feature might be the use of timestamps to find the best summary there is.

## Authors and acknowledgment
The authors of the are Marcus Heider, Daniel Titz, Tobias Gaiser and Felix Lutz.
A special Thank you goes to Philipp Seeberger and Professor Doctor Riedhammer for guiding this project.
Thank you to [makeareadme.com](https://www.makeareadme.com/) for this template.
And last but not least thank you to the Crisis Facts Challenge.

## License
Copyright 2022 Marcus Heider, Daniel Titz, Tobias Gaiser and Felix Lutz

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Project status
The project is finished. The website can be used to demonstrate the effects of different hyperparameters have on the task of text summarisation. 
