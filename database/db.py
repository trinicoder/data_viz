import psycopg2
import psycopg2.extras
import json


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
     return psycopg2.connect("dbname=population user = varoon password=varoon host=localhost")
    except:
        print("can't connect to databse")



def getjson():
    with open("jsonfiles/TT18.json") as json_file:
        json_data = json.load(json_file)
    return(json_data)


DB=connect()
c= DB.cursor()
json=getjson()
#151
for x in range(0,151):
    tuple=json['TT18'][x]
    #change to country id!
    ftuple=(3,)
    for key in tuple:
        if key!='total':
            ftuple=ftuple + (tuple[key],)
    c.execute("INSERT INTO populationdata (countryid, age, male, female, year) values (%s,%s,%s,%s,%s)",(ftuple))

#print (ftuple)



#c.execute("INSERT INTO country values (%s)",("Jamaica",))
#c.execute("INSERT INTO country values (%s)",("Trinidad and Tobago",))
DB.commit()
DB.close()