import json
import os
from sqlite3 import Timestamp
import pandas as pd
from datetime import datetime


def newinput():
    for i in range(1,9):
        file="D:\\Meine Dateien\\Uni\\IT-Projekt\\Arbeit\\it-projekt\\Archive\\00"+str(i) 
        file_out="D:\\Meine Dateien\\Uni\\IT-Projekt\\Arbeit\\it-projekt\\Archive\\Datensatz_"+str(i)+".json"
        for f in os.listdir(file):
            df = pd.read_json(file+'\\'+f, orient='records')
            df = df[['event','doc_id', 'source_type', 'unix_timestamp',  'text']]
            df.insert(4, 'lang', "en")
            df.insert(5, 'meta', "")
            df.insert(6, 'title', "")
            df.rename(columns={'event':'stream_id', 'doc_id':'document_id', 'source_type':'document_source', 'unix_timestamp':'timestamp', 'text':'content'}, inplace=True)
            df['timestamp'] = df['timestamp'].map(lambda t: datetime.utcfromtimestamp(t).strftime('%Y-%m-%dT%H:%M:%S.0000Z'))
            with open(file_out, 'a',encoding="utf-8") as f:
                for row in df.to_dict('records'):
                    f.write('\n')
                    f.write(json.dumps(row))
            
newinput()  

#file="D:\\Meine Dateien\\Uni\\IT-Projekt\\Arbeit\\it-projekt\\website\\Data\\Datensaetze\\002\\2018-07-30.json"
#df = json.loads(file) #pd.read_json(file, orient='columns')
#df = df["source"]["created_at"]
#print(df[:10])   