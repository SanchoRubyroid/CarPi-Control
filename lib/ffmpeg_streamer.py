import subprocess

class FFMPEGStramer():
    STREAM_PORTS_OFFSET = 20256

    def __init__(self, config, options = {}):
        self.streaming_port = self.STREAM_PORTS_OFFSET + int(options['streaming-port-number'])

        self.config = config
        self.closed = False

    def stream(self):
        width = self.config['ratio']['factor'] * self.config['ratio']['horizontal']
        height = self.config['ratio']['factor'] * self.config['ratio']['vertical']

        params = [self.config['ffmpeg']['command']]
        # INPUT
        params.append('-s')
        params.append(str(width) + 'x' + str(height))
        params.append('-f')
        params.append(self.config['ffmpeg']['input_format'])
        params.append('-i')
        params.append(self.config['ffmpeg']['input_device'])
        # OUTPUT
        params.append('-f')
        params.append('mpeg1video')
        params.append('-b')
        params.append(self.config['ffmpeg']['bitrate'])
        params.append('-r')
        params.append(str(self.config['ffmpeg']['fps']))
        params.append('http://'+ self.config['host'] +':'+ str(self.streaming_port) +'/')

        self.subprocess_proc = subprocess.Popen(params)

    def close(self):
        if not self.closed:
            self.subprocess_proc.terminate()
            self.subprocess_proc.wait()
            self.closed = True
