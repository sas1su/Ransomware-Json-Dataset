# Open the json file and read the json data 
import json
from pprint import pprint
import sqlite3

connection = sqlite3.connect("ransomware.db")
cursor = connection.cursor()

# Sanitize the data to be stored in database
# Schemas
# tables 
# ransomware = id, fk(rans_name), extensions TEXT, extensionPattern TXT, ransomNoteFilenames TXT, comment, 
# encryptionAlgorithm, decryptor, fk(resources), screenshots, microsoftDetectionName, microsoftInfo, sandbox, iocs, snort
# name,extensions,extensionPattern,ransomNoteFilenames,comment, 
# encryptionAlgorithm,decryptor,resources,screenshots,microsoftDetectionName,microsoftInfo,sandbox,iocs,snort
# 1, 1, 
# rans_name = id, name
# 1, "777"
# 2, "Sevleg"
# resources = id, resource
# id, "https://decrypter.emsisoft.com/777"

cursor.execute("CREATE TABLE rans_names (id INTEGER PRIMARY KEY, name TEXT)")

cursor.execute("CREATE TABLE ransomware (id INTEGER PRIMARY KEY,name_id INTEGER, extensions TEXT, extensionPattern TEXT, ransomNoteFilenames TEXT, comment TEXT,encryptionAlgorithm TEXT, decryptor TEXT, resources TXT, screenshots TEXT, microsoftDetectionName TEXT, microsoftInfo TEXT, sandbox TEXT, iocs TEXT, snort TEXT)")


# no more using this to reduce numner of records
# cursor.execute("CREATE TABLE resources (id INTEGER PRIMARY KEY, resources TEXT)") 

try:
    with open("ransomware_overview.json", "r") as r:
        data = json.load(r)
except Exception as e:
    print("Exception: Cannot get data from json file")

# counter to keep track of record
count = 1

# process each record
for record in data:
    print(f"Record: {count}")
    count += 1

    for name in record["name"]:
        res = cursor.execute("SELECT id FROM rans_names where name = ?", (name,))
        id = res.fetchone()
        if not id: 
            print(f"Ransomware name does not exist, adding {name} to database")
            cursor.execute("INSERT INTO rans_names (id, name) VALUES (?, ?)", (None, name))

            last_inserted_row = cursor.execute("SELECT max(id) FROM rans_names")
            id = last_inserted_row.fetchone()
            print(f"Ransomware name {name} inserted with id {id[0]}")


            ## Pack resources into a comma separated entry to the ransomware table. So that the number of 
            ## records for each name will not be multiple for resources
            if len(record["resources"]) > 0:
                resources = ",".join(record["resources"])


        
            # Check the record already exit. if not insert
            res = cursor.execute("SELECT id FROM ransomware where name_id = ?", (id[0],))
            rans_id = res.fetchone()
            if rans_id:
                print(f"Ransomware record exist {rans_id}")
                continue
            else:
                cursor.execute("""
                            INSERT INTO ransomware(id, name_id, extensions, extensionPattern, ransomNoteFilenames, comment,encryptionAlgorithm, decryptor, resources, screenshots, microsoftDetectionName, microsoftInfo, sandbox, iocs, snort) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", 
                            (None,id[0], record["extensions"], record["extensionPattern"], record["ransomNoteFilenames"], record["comment"], record["encryptionAlgorithm"], record["decryptor"], resources, record["screenshots"], record.get("microsoftDetectionName", None), record.get("microsoftInfo", None), record.get("sandbox", None), record.get("iocs", None), record.get("snort", None) ))
        else:
            print(f"Ransomware name exist {name}")
            #continue
        

connection.commit()