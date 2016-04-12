from lib.vehicle import Vehicle

import redis
import yaml
import threading
import json

CAR_NAME = 'carName'

class Listener(threading.Thread):
    def __init__(self, vehicle):
        threading.Thread.__init__(self)

        self.vehicle = vehicle

        redis_config = yaml.safe_load(open('redis-conf.yml'))
        print redis_config

        self.redis = redis.Redis(host=redis_config['host'], port=redis_config['port'])
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(vehicle.name)

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == 'KILL':
                self.pubsub.unsubscribe()
                self.vehicle.shutdown()
                print self, 'unsubscribed and finished'
                break
            elif isinstance(item['data'], str):
                try:
                    #print self, "ITEM DATA " + item['data']
                    self.vehicle.update(json.loads(item['data']))
                    #print self, "-----------------"
                except ValueError:
                    print self, 'ERROR: Bad JSON received: ' + item['data']
            else:
                print self, 'Non string value received. Skipped.'

if __name__ == "__main__":
    client = Listener(Vehicle(CAR_NAME))
    client.start()
