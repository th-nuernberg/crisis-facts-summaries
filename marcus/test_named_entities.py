import os

import re
import html
import textacy.preprocessing as tprep
import pandas as pd
import json
#import sqlite3 
import spacy
import pprint as pp

nlp = spacy.load('en_core_web_sm')
pp.pprint("Done")