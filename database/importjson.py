import json

def getjson():
    with open("jsonfiles/guy18.json") as json_file:
        json_data = json.load(json_file)
    return(json_data)



json=getjson()
print (len(json['GUY18']))