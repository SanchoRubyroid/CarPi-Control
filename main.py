from lib.vehicle import Vehicle

import redis
import yaml
import json
import socket

class Listener:
    BUFSIZ = 1024

    def __init__(self):
        self.config = yaml.safe_load(open('config.yml'))

        self.vehicle = Vehicle(self.config)
        self.tcp_cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # def initialize_redis(self):
    #     redis_config = yaml.safe_load(open('redis-conf.yml'))
    #     redis_config.setdefault('password', None)
    #
    #     self.redis = redis.Redis(
    #         host=redis_config['host'],
    #         port=redis_config['port'],
    #         password=redis_config['password'])
    #
    #     self.redis.setex('cars-list-refresh', '', 1)
    #     self.redis.execute_command('client', 'setname', '__vehicle__' + self.vehicle.name)
    #
    #     self.pubsub = self.redis.pubsub()
    #     self.pubsub.subscribe(self.vehicle.name)

    def listen(self):
        self.tcp_cli_sock.connect((self.config['host'], self.config['port']))
        print 'Connected'

        self.tcp_cli_sock.send('vn:' + self.vehicle.name)

        while True:
            data = self.tcp_cli_sock.recv(self.BUFSIZ)    # Receive data sent from the client.
            print data

            if not data:
                print 'Server has gone away.'
                break
            elif data == 'KILL':
                self.shutdown()
                break
            elif isinstance(data, str):
                try:
                    self.vehicle.update(json.loads(data))
                except ValueError:
                    print 'ERROR: Bad JSON received: ' + data
            else:
                print 'Non string value received. Skipped.'

    def shutdown(self):
        self.vehicle.shutdown()
        print 'Finished'

if __name__ == "__main__":
    try:
        listener = Listener()
        listener.listen()
    except KeyboardInterrupt:
        listener.shutdown()
