from lib.vehicle import Vehicle

import redis
import yaml
import threading
import json

CAR_NAME = 'carName'

class Manager:
    def __init__(self, name):
        self.vehicle = Vehicle(name)

        redis_config = yaml.safe_load(open('redis-conf.yml'))
        print redis_config

        self.redis = redis.Redis(host=redis_config['host'], port=redis_config['port'])
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(self.vehicle.name)

    def execute(self):
        for item in self.pubsub.listen():
            if item['data'] == 'KILL':
                self.shutdown()
                break
            elif isinstance(item['data'], str):
                try:
                    self.vehicle.update(json.loads(item['data']))
                except ValueError:
                    print 'ERROR: Bad JSON received: ' + item['data']
            else:
                print 'Non string value received. Skipped.'

    def shutdown(self):
        self.pubsub.unsubscribe()
        self.vehicle.shutdown()
        print 'unsubscribed and finished'

if __name__ == "__main__":
    try:
        manager = Manager(CAR_NAME)
        manager.execute()
    except KeyboardInterrupt:
        manager.shutdown()
