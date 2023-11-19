#!/home/mongodb/miniconda3/envs/pymongo_env/bin/python
from pymongo import MongoClient
import sys

URI = "mongodb://localhost:27019"

client = MongoClient(URI)
db = client['admin']

createUser={
    "createUser": sys.argv[1],
    "pwd": sys.argv[2],
    "roles": [
        {"role": "userAdminAnyDatabase", "db": "admin"},
        {"role": "clusterAdmin", "db": "admin" }
    ]
}

isUserExists = False
try:

    user_info = db.command('usersInfo', sys.argv[1])
    if len(user_info['users'])>0:
        user_id = user_info['users'][0]['_id']
        user_id_arr = user_id.split('.')
        user_id_name = user_id_arr[1]
        if sys.argv[1] == user_id_name:
            isUserExists = True
            print("User exists")

    if not isUserExists:
        db.command(createUser)
        print("User created successfully")

except Exception as err:
    print(err)
finally:
    client.close()
