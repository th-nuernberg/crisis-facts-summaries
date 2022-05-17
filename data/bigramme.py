import os
import pandas as pd
import json
import re

raw_dir ="D:\\Meine Dateien\\Uni\\IT-Projekt\\Arbeit\\it-projekt\\prepared\\"
out_dir ="D:\\Meine Dateien\\Uni\\IT-Projekt\\Arbeit\\it-projekt\\data\\"
#file="26.relonly.jsonl"
for file in os.listdir(raw_dir):
    df = []
    with open(raw_dir+file, 'r',encoding="utf-8") as json_file:
        mytext = json_file.read()
        lines = mytext.split("\n")
        for line in lines:
            if len(line) >0:
                df.append(json.loads(line))

    print("step")

    def bigramme(text):
        words  = re.findall(r'[A-Za-z0-9]+',text)    
        result=""
        for i in range(0,len(words)):
            if (i < (len(words)-1)):
                result = result+words[i]+"_"+words[i+1]+";"
        return result

    for item in df:
        item["bigramme"]= bigramme(item["content"])

    print("step1")

    with open(out_dir+file, "a", encoding="utf-8") as file:
        for line in df:
            file.write(json.dumps("stream_id:"+line["stream_id"]+",document_id:"+line["document_id"]+",document_source:"+line["document_source"]+",timestamp:"+line["timestamp"]+",lang:"+line["lang"]+",meta:"+line["meta"]+",title:"+line["title"]+",content:"+line["content"]+",bigramme:"+line["bigramme"])+'\n')

    print("step2")
print("done")