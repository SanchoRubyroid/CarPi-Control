import threading
import io
import socket
import struct
import time
import picamera

class VideoStreamClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.connection = socket.socket()
        self.connection.connect(('192.168.0.100', 1338))

        self.camera.resolution = (240, 180)
        self.camera.vflip = True
        # Start a preview and let the camera warm up for 2 seconds
        self.camera.start_preview()
        time.sleep(2)

        self.stream = io.BytesIO()

    def run(self):
        try:
            for _1 in self.camera.capture_continuous(self.stream, 'jpeg', True):
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                # print("LEN: " + str(stream.tell()))
                self.connection.send(struct.pack('<L', self.stream.tell()))
                # time.sleep(0.05)
                # Rewind the stream and send the image data over the wire
                self.stream.seek(0)
                self.connection.send(self.stream.read())

                # Reset the stream for the next capture
                self.stream.seek(0)
                self.stream.truncate()
                recv_len = struct.unpack('<L', self.connection.recv(struct.calcsize('<L')))[0]
                if recv_len == 0xFFFFFFFF:
                    break;
                #print("RECV LEN: " + str(recv_len))
                time.sleep(0.1)
        finally:
            self.connection.close()
