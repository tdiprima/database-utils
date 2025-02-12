# Connects to a MongoDB, accesses a specific database and collection, then retrieves and prints the first document
# where the 'provenance.analysis.execution_id' field equals 'somebody@gmail.com'.
from pymongo import MongoClient

if __name__ == '__main__':

    db_host = "example.com"
    db_port = "27017"
    db_name = "camic"

    client = MongoClient('mongodb://' + db_host + ':' + db_port + '/')
    db = client[db_name]
    mark = db.mark

    for record in mark.find({"provenance.analysis.execution_id": "somebody@gmail.com"}).limit(1):
        print(record)

    exit()
