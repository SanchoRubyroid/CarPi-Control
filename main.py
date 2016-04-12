from lib.vehicle import Vehicle

import redis
import yaml
import threading
import json

CAR_NAME = 'shelby-gt100500'

class Listener:
    def __init__(self, name):
        self.vehicle = Vehicle(name)
        self.initialize_redis()

    def initialize_redis(self):
        redis_config = yaml.safe_load(open('redis-conf.yml'))
        redis_config.setdefault('password', None)

        self.redis = redis.Redis(
            host=redis_config['host'],
            port=redis_config['port'],
            password=redis_config['password'])

        self.redis.setex('car-online', '', 1)
        self.redis.execute_command('client', 'setname', '__vehicle__' + self.vehicle.name)

        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(self.vehicle.name)

    def listen(self):
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
        listener = Listener(CAR_NAME)
        listener.listen()
    except KeyboardInterrupt:
        listener.shutdown()
