import json
import time
import random
from kafka import KafkaProducer
import yaml

class Producer():
    with open('config.yml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    reporter_id_counter = config['reporter_id_counter']

    def generate_event(self):
        global reporter_id_counter
        event = {
            "reporterId": self.reporter_id_counter,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "metricId": random.randint(1, 10),
            "metricValue": random.randint(1, 100),
            "message": "HELLO WORLD" 
        }
        return event

def main():
    producer_instance = Producer() 
    producer = KafkaProducer(bootstrap_servers=[Producer.config['localhost']],
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    while True:
        event = producer_instance.generate_event()
        producer.send('events-topic', value=event)
        producer_instance.reporter_id_counter += Producer.config['numberPlus']
        print("sent")
        time.sleep(6) 

if __name__ == "__main__":
    main()
