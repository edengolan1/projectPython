from kafka import KafkaConsumer
import json
import pymongo
import yaml
    
class Consumer():
    with open('config.yml', 'r') as config_file:
      config = yaml.safe_load(config_file)

    client = pymongo.MongoClient(config['client'])
    db = client[config['dbMongoDB']]
    collection = db[config['collection']]

    def insert_into_mongodb(event):
        Consumer.collection.insert_one(event)
        # for x in collection.find():
        #     print(x)

    def delete_all_from_mongodb():
        result = Consumer.collection.delete_many({})
        print("Deleted", result.deleted_count, "documents from MongoDB")
        
    def Update_MongoDB():
        myquery = { "reporterId": 5 }
        newvalues = { "$set": { "reporterId": 15 } }
        Consumer.collection.update_one(myquery, newvalues)

def main():
    consumer = KafkaConsumer('events-topic', bootstrap_servers=[Consumer.config['localhost']],
                        auto_offset_reset='earliest', 
                        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    print("gonna start listening")
    # Consumer.delete_all_from_mongodb()
    while(True):
        for message in consumer:
            print("ongoing consumer")
            newMessage = message.value
            Consumer.insert_into_mongodb(newMessage)
            print(newMessage)
    
if __name__ == "__main__":
    main()