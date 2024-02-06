import redis
import time
import pymongo
import json
import threading
import yaml

class MyRedis():
    def Import_mongodb():
        with open('config.yml', 'r') as config_file:
          config = yaml.safe_load(config_file)

        r = redis.Redis(host=config['numberHost'], port=config['numberPort'], db=config['db'])
        client = pymongo.MongoClient(config['client'])
        db = client[config['dbMongoDB']]
        collection = db[config['collection']]
        for event in collection.find():
            key = f"{event['reporterId']}:{event['timestamp']}"
            event['_id'] = str(event['_id'])
            event_json = json.dumps(event)
            try:
                if not r.exists(key):
                    r.set(key, event_json)
                    print("Data added to Redis:", key)
                    printDetails = r.get(key)
                    printDetails = printDetails.decode('utf-8')
                    print(printDetails)
            except redis.RedisError as e:
                print("Error adding data to Redis:", e)
        # r.flushdb()
        client.close()
        time.sleep(30)
def main():
    thread = threading.Thread(target=MyRedis.Import_mongodb)
    thread.start() 
    
if __name__ == "__main__":
    main()