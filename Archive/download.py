# Write this to a file so it can be read when needed
import json
import os
import requests
import ir_datasets
import pandas as pd

# download the first day for event 001 (this is a lazy call, it won't download until we first request a document from the stream

# Gets the list of days for a specified event number, e.g. '001'
def getDaysForEventNo(eventNo):

  # We will download a file containing the day list for an event
  url = "http://trecis.org/CrisisFACTs/CrisisFACTS-"+eventNo+".requests.json"

  # Download the list and parse as JSON
  dayList = requests.get(url).json()

  # Print each day
  # Note each day object contains the following fields
  #   {
  #      "eventID" : "CrisisFACTS-001",
  #      "requestID" : "CrisisFACTS-001-r3",
  #      "dateString" : "2017-12-07",
  #      "startUnixTimestamp" : 1512604800,
  #      "endUnixTimestamp" : 1512691199
  #   }

  return dayList
  
eventNoList = [
    #"001", # Lilac Wildfire 2017
    #"002", # Cranston Wildfire 2018
    "003", # Holy Wildfire 2018
    #"004", # Hurricane Florence 2018
    "005", # 2018 Maryland Flood
    "006", # Saddleridge Wildfire 2019
    "007", # Hurricane Laura 2020
    "008" # Hurricane Sally 2020
]

eventNoLis = [
    "004"
]

def  mk_cre():
    credentials = {
        "institution": "Technische Hochschule Nürnberg", # University, Company or Public Agency Name
        "contactname": "Felix Lutz", # Your Name
        "email": "lutzfe79909@th-nuernberg.de", # A contact email address
        "institutiontype": "Research" # Either 'Research', 'Industry', or 'Public Sector'
    }

    #Todo speicherort anpassen
    #home_dir = os.path.expanduser('~')

    #!mkdir -p ~/.ir_datasets/auth/
    with open( 'C:\\Users\\Ich\\.ir_datasets\\auth\\crisisfacts.json', 'w') as f:
        json.dump(credentials, f)

# for eventNo in eventNoList: # for each event
#   dayList = getDaysForEventNo(eventNo) # get the list of days
#   print("Event "+eventNo)
#   for day in dayList: # for each day
#     print("  crisisfacts/"+eventNo+"/"+day["dateString"]) # construct the request string
#   print()

#for day in getDaysForEventNo(eventNoList[0]):
#  print(day["dateString"])

#dataset = ir_datasets.load('crisisfacts/001/2017-12-07')

#for item in dataset.docs_iter()[:10]: # create an iterator over the stream containing the first 10 items
#  print(item)
#mk_cre()
test=[
"2018-09-01",
"2018-09-04",
"2018-09-05",
"2018-09-07",
"2018-09-08",
"2018-09-09",
"2018-09-10",
"2018-09-12",
"2018-09-13",
"2018-09-14",
"2018-09-15",
"2018-09-16",
"2018-09-17",
"2018-09-18"
]
path = "D:\\Meine Dateien\\Uni\\IT-Projekt\\Arbeit\\it-projekt\\Felix\\"

for event in eventNoLis:
    print(event)
    for day in test:#getDaysForEventNo(event):
        file_out = path+event+"\\"+day+".json" #["dateString"]
        print(day)#["dateString"]
        dataset = ir_datasets.load('crisisfacts/' +event+ '/' +day)#["dateString"]
        itemsAsDataFrame = pd.DataFrame(dataset.docs_iter())
        # with open(file_out, 'a',encoding="utf-8") as f:
        #     result = itemsAsDataFrame.to_json(orient="records")
        #     parsed = json.loads(result)
        #     f.write(json.dumps(parsed, indent=4))
        #for item in itemsAsDataFrame.head(1):#dataset.docs_iter()[1]: # create an iterator over the stream containing the first 10 items
        print(itemsAsDataFrame.head(1)["source"])
        #print(pd.DataFrame(dataset.queries_iter())[:10])
        
def newinput():
    file="D:\\Meine Dateien\\Uni\\IT-Projekt\\Arbeit\\it-projekt\\Felix\\002\\2018-07-30.json"
    df = pd.read_json(file, orient='records')
    print(df[:10])   