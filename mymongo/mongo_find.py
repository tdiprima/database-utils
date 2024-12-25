from pymongo import MongoClient

if __name__ == '__main__':

    db_host = "example.com"
    db_port = "27017"
    db_name = "camic"

    client = MongoClient('mongodb://' + db_host + ':' + db_port + '/')
    db = client[db_name]
    mark = db.mark

    for record in mark.find({"provenance.analysis.execution_id": "ardy360@gmail.com"}).limit(1):
        print(record)

    exit()
