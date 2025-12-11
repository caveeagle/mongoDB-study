
from pymongo import MongoClient

import config

SERVER = config.SERVER
USER   = config.USER
PASSWD = config.PASSWD

###############################


REMOTE = 0

if( not REMOTE ):
    SERVER = 'localhost'


client = MongoClient(
    host=SERVER,
    port=27017,
    username=USER,
    password=PASSWD
)

db = client['study_db_shop']

###############################

collections = db.list_collection_names()

if(1):
    print('All collections:\n')
    for n in collections:
        print(n)
    print('\n')

###############################









###############################

print('Job finished!')

###############################
