import threading
import io
import socket
import struct
import time

class VideoStreamClient(threading.Thread):
    RATIO_VERTICAL = 16
    RATIO_HORIZONTAL = 9

    def __init__(self, options):
        super(VideoStreamClient, self).__init__()
        self._stop = threading.Event()

        ratio_factor = int(options['ratio_factor'])

        self.camera = options['camera']
        self.camera.resolution = (ratio_factor * self.RATIO_VERTICAL, ratio_factor * self.RATIO_HORIZONTAL)
        self.camera.vflip = True
        self.camera.hflip = True

        self.stream = io.BytesIO()

        self.stop_capture = False

        self.connection = socket.socket()
        self.connection.connect((options['host'], int(options['port'])+1))

        self.connection.send('vn:' + options['vehicle_name'])

    def shutdown(self):
        self.camera.stop_preview()
        self.stop_capture = True
        self._stop.set()

    def run(self):
        try:
            # Start a preview and let the camera warm up for 2 seconds
            self.camera.start_preview()
            time.sleep(2)
            for _1 in self.camera.capture_continuous(self.stream, 'jpeg', True):
                # Write the length of the capture to the stream
                self.connection.send(struct.pack('<L', self.stream.tell()))

                # Rewind the stream and send the image data over the wire
                self.stream.seek(0)
                self.connection.send(self.stream.read())

                # Reset the stream for the next capture
                self.stream.seek(0)
                self.stream.truncate()

                # Wait for response and check if we need to stop streaming
                recv_data = struct.unpack('<L', self.connection.recv(struct.calcsize('<L')))[0]
                if recv_data == 0xFFFFFFFF or self.stop_capture:
                    break;

                # Sleep before the next shot
                time.sleep(0.07)
        finally:
            self.connection.close()
