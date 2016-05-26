from lib.vehicle import Vehicle
from lib.ffmpeg_streamer import FFMPEGStramer

import yaml
import socket
import struct
import datetime
import binascii

class Listener:
    BUFFER_SIZE = 3

    def __init__(self):
        self.config = yaml.safe_load(open('config.yml'))

        self.vehicle = Vehicle(self.config)
        self.tcp_cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self):
        self.tcp_cli_sock.connect((self.config['host'], self.config['port']))
        print('Connected')

        self.tcp_cli_sock.send('vn:' + self.vehicle.name)

        while True:
            data = self.tcp_cli_sock.recv(self.BUFFER_SIZE)

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
            elif values[0] == 102: # Shutdown command
                self.tcp_cli_sock.send('pong')
            elif values[0] == 103: # Start real-time video streaming
                self.stream_shutdown()
                self.stream = FFMPEGStramer(self.config, {
                    'streaming-port-number': values[1],
                    'ratio-factor': values[2] })
                self.stream.stream()
            elif values[0] == 105: # Stop real-time video streaming
                self.stream_shutdown()
            elif values[0] == 106: # Set vehicle turning apex
                self.vehicle.set_turning_apex(values[1])
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
