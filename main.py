from lib.vehicle import Vehicle
from lib.ffmpeg_streamer import FFMPEGStramer

import yaml
import socket
import struct
import datetime
import binascii
import json

class Listener:
    BUFFER_SIZE = 3

    def __init__(self):
        self.config = yaml.safe_load(open('config.yml'))

        self.vehicle = Vehicle(self.config)
        self.tcp_cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self):
        self.tcp_cli_sock.connect((self.config['host'], self.config['port']))
        print('Connected')

        self.tcp_cli_sock.send(json.dumps(self.config))

        while True:
            data = self.tcp_cli_sock.recv(self.BUFFER_SIZE)

            # Reveive 3 bytes of data
            values = struct.unpack('bbb', data)

            if self.config['debug_mode']:
                print("DATA: " + str(values))

            if not data:
                print('Server has gone away.')
                break
            if values[0] <= 100: # Regular control values
                self.vehicle.update(values)
            elif values[0] == 101: # Shutdown command
                self.shutdown()
                break
            elif values[0] == 102: # Ping
                self.tcp_cli_sock.send('pong')
            elif values[0] == 103: # Start real-time video streaming
                streaming_port = struct.unpack('<L', self.tcp_cli_sock.recv(struct.calcsize('<L')))[0]
                self.stream_shutdown()
                self.stream = FFMPEGStramer(self.config, streaming_port)
                self.stream.stream()
            elif values[0] == 105: # Stop real-time video streaming
                self.stream_shutdown()
            elif values[0] == 106: # Set vehicle turning apex
                self.vehicle.set_turning_apex(values[1])
            elif values[0] == 107: # Set Video Quality
                self.config['ratio']['horizontal'] = 16
                self.config['ratio']['vertical'] = 12
                if values[1] == 2:
                    self.config['ratio']['factor'] = 40
                elif values[1] == 0:
                    self.config['ratio']['factor'] = 10
                else:
                    self.config['ratio']['factor'] = 20

                self.tcp_cli_sock.send(json.dumps(self.config))
            else:
                self.say_bad_packet(data)

    def say_bad_packet(self, data):
        print('Bad incoming packet: ' + binascii.hexlify(data))

    def stream_shutdown(self):
        try:
            self.stream.close()
            print("Video streaming stopped")
        except AttributeError:
            pass # stream was not initialized so no need to shutdown

    def shutdown(self):
        self.vehicle.shutdown()
        self.stream_shutdown()
        print('Finished')

if __name__ == "__main__":
    try:
        print("Started at " + str(datetime.datetime.now()))
        listener = Listener()
        listener.listen()
    except KeyboardInterrupt:
        listener.shutdown()
