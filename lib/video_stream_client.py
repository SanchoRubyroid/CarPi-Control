import threading
import io
import socket
import struct
import time

class VideoStreamClient(threading.Thread):
    def __init__(self, host_port, vehicle_name, camera):
        super(VideoStreamClient, self).__init__()
        self._stop = threading.Event()

        self.host_port = host_port
        self.vehicle_name = vehicle_name

        self.camera = camera
        self.camera.resolution = (240, 180)
        self.camera.vflip = True
        self.camera.hflip = True

        self.stream = io.BytesIO()

        self.stop_capture = False

        self.connection = socket.socket()
        self.connection.connect(self.host_port)

        self.connection.send('vn:' + self.vehicle_name)

        # Start a preview and let the camera warm up for 2 seconds
        self.camera.start_preview()
        time.sleep(2)

    def shutdown(self):
        self.camera.stop_preview()
        self.stop_capture = True
        self._stop.set()

    def run(self):
        try:
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
                time.sleep(0.1)
        finally:
            self.connection.close()
