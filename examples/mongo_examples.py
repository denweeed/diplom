import pymongo

if __name__ == '__main__':
    client = pymongo.MongoClient('localhost', 8081)
    db = client['database']
    collection = db ['collection']

    data = {'id': 1, 'name': 'Kate', 'price': 20}
    result = collection.insert_one(data)
    print(result.inserted_id)

    cursor = collection.find()

    for document in cursor:
        print(document)
