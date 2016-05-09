import threading
import io
import socket
import struct
import time
import picamera

class VideoStreamClient(threading.Thread):
    def __init__(self, host_port):
        threading.Thread.__init__(self)
        self.host_port = host_port

        self.camera = picamera.PiCamera()
        self.camera.resolution = (240, 180)
        self.camera.vflip = True
        # Start a preview and let the camera warm up for 2 seconds

        self.stream = io.BytesIO()

        self.stop_capture = False

    def enable_camera(self):
        self.connection = socket.socket()
        self.connection.connect(self.host_port)

        self.camera.start_preview()
        time.sleep(2)

    def shutdown(self):
        self.camera.stop_preview()
        self.stop_capture = True

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
                if recv_len == 0xFFFFFFFF or self.stop_capture:
                    print 'Stop Capture'
                    self.stop_capture = False
                    break;
                #print("RECV LEN: " + str(recv_len))
                time.sleep(0.1)
        finally:
            self.connection.close()
