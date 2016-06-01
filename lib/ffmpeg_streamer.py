import subprocess

class FFMPEGStramer():
    def __init__(self, config, streaming_port):
        self.streaming_port = streaming_port

        self.config = config
        self.closed = False

    def stream(self):
        width = self.config['ratio']['factor'] * self.config['ratio']['horizontal']
        height = self.config['ratio']['factor'] * self.config['ratio']['vertical']

        params = [self.config['ffmpeg']['command']]
        # INPUT
        params.append('-f')
        params.append(self.config['ffmpeg']['input_format'])
        if 'fps' in self.config['ffmpeg']:
            params.append('-framerate')
            params.append(str(self.config['ffmpeg']['fps']))
        params.append('-video_size')
        params.append(str(width) + 'x' + str(height))
        params.append('-i')
        params.append(self.config['ffmpeg']['input_device'])
        # OUTPUT
        params.append('-f')
        params.append('mpeg1video')
        params.append('-b')
        params.append(self.config['ffmpeg']['bitrate'])
        if self.config['ffmpeg']['rotate_180']:
            params.append('-vf')
            params.append('transpose=2,transpose=2')
        if 'loglevel' in self.config['ffmpeg']:
            params.append('-loglevel')
            params.append(self.config['ffmpeg']['loglevel'])
        params.append('http://'+ self.config['host'] +':'+ str(self.streaming_port) +'/')

        self.subprocess_proc = subprocess.Popen(params)

    def close(self):
        if not self.closed:
            self.subprocess_proc.terminate()
            self.subprocess_proc.wait()
            self.closed = True
