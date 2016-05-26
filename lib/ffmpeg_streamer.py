import subprocess

class FFMPEGStramer():
    STREAM_PORTS_OFFSET = 20256

    RATIO_HORIZONTAL = 16
    RATIO_VERTICAL = 12

    def __init__(self, config, options = {}):
        options.setdefault('ratio-factor', 20)

        self.streaming_port = self.STREAM_PORTS_OFFSET + int(options['streaming-port-number'])
        self.ratio_factor = int(options['ratio-factor'])

        self.config = config
        self.closed = False

    def stream(self):
        width = self.ratio_factor * self.RATIO_HORIZONTAL
        height = self.ratio_factor * self.RATIO_VERTICAL

        params = [self.config['ffmpeg_command']]
        # INPUT
        params.append('-s')
        params.append(str(width) + 'x' + str(height))
        params.append('-f')
        params.append(self.config['ffmpeg_input_format'])
        params.append('-i')
        params.append(self.config['ffmpeg_input_device'])
        # OUTPUT
        params.append('-f')
        params.append('mpeg1video')
        params.append('-b')
        params.append('800k')
        params.append('http://'+ self.config['host'] +':'+ str(self.streaming_port) +'/'+ str(width) +'/'+ str(height) +'/')

        print(">>>>>> PARAMS: "+str(params))

        self.subprocess_proc = subprocess.Popen(params)

    def close(self):
        if not self.closed:
            self.subprocess_proc.terminate()
            self.subprocess_proc.wait()
            self.closed = True
