from lib.vehicle import Vehicle
from lib.video_stream_client import VideoStreamClient

import yaml
import json
import socket
import struct
import datetime

class Listener:
    BUFSIZ = 3

    def __init__(self):
        self.config = yaml.safe_load(open('config.yml'))

        self.vehicle = Vehicle(self.config)
        self.tcp_cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.stream = VideoStreamClient((self.config['host'], int(self.config['port'])+1))

    def listen(self):
        self.tcp_cli_sock.connect((self.config['host'], self.config['port']))
        print('Connected')

        self.tcp_cli_sock.send('vn:' + self.vehicle.name)

        while True:
            data = self.tcp_cli_sock.recv(self.BUFSIZ)    # Receive data sent from the server.
            values = struct.unpack('bbb', data)

            if self.config['debug_mode']:
                print("DATA: " + str(values))

            if not data:
                print('Server has gone away.')
                break
            elif values[0] == 101:
                self.shutdown()
                break
            elif values[0] == 102:
                self.tcp_cli_sock.send('pong')
            elif values[0] == 103:
                self.stream.enable_camera()
                self.stream.start()
            else:
                self.vehicle.update(values)

    def shutdown(self):
        self.vehicle.shutdown()
        self.stream.shutdown()
        print('Finished')

if __name__ == "__main__":
    try:
        print("Started at " + str(datetime.datetime.now()))
        listener = Listener()
        listener.listen()
    except KeyboardInterrupt:
        listener.shutdown()
