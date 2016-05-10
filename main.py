from lib.vehicle import Vehicle
from lib.video_stream_client import VideoStreamClient

import yaml
import json
import socket
import struct
import datetime
import binascii

try:
    import picamera
except ImportError:
    picamera = False

class Listener:
    BUFFER_SIZE = 3

    def __init__(self):
        self.config = yaml.safe_load(open('config.yml'))

        self.vehicle = Vehicle(self.config)
        self.tcp_cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.camera = (picamera.PiCamera() if picamera else False)

    def listen(self):
        self.tcp_cli_sock.connect((self.config['host'], self.config['port']))
        print('Connected')

        self.tcp_cli_sock.send('vn:' + self.vehicle.name)

        while True:
            data = self.tcp_cli_sock.recv(self.BUFFER_SIZE)
            #if len(data) == 0: continue # skip blank packet

            values = struct.unpack('bbb', data)

            if self.config['debug_mode']:
                print("DATA: " + str(values))

            if not data:
                print('Server has gone away.')
                break
            if values[0] <= 100:
                self.vehicle.update(values)
            elif values[0] == 101:
                self.shutdown()
                break
            elif values[0] == 102:
                self.tcp_cli_sock.send('pong')
            elif values[0] == 103:
                if self.camera:
                    self.stream = VideoStreamClient((self.config['host'], int(self.config['port'])+1), self.vehicle.name, self.camera)
                    self.stream.start()
            elif values[0] == 105:
                self.camera_shutdown()
            elif values[0] == 106:
                self.vehicle.set_turning_apex(values[1])
            else:
                self.say_bad_packet(data)

    def say_bad_packet(self, data):
        print('Bad incoming packet: ' + binascii.hexlify(data))

    def camera_shutdown(self):
        try:
            self.stream.shutdown()
            self.stream.join()
            print("Video streaming stopped")
        except AttributeError:
            pass # stream was not initialized so no need to shutdown

    def shutdown(self):
        self.vehicle.shutdown()
        self.camera_shutdown()
        print('Finished')

if __name__ == "__main__":
    try:
        print("Started at " + str(datetime.datetime.now()))
        listener = Listener()
        listener.listen()
    except KeyboardInterrupt:
        listener.shutdown()
