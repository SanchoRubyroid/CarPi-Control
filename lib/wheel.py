try:
    import RPi.GPIO as GPIO
except ImportError:
    print('ERROR: RPi.GPIO import failed. DEBUG_MODE only.')

class Wheel:
    PINS = {
        'left': { 'pwm': 13, 'primary': 11, 'secondry': 15 },
        'right': { 'pwm': 12, 'primary': 16, 'secondry': 18 }
    }

    # PWM Frequece
    PWM_FQ = 40

    @classmethod
    def cleanup(cls):
        GPIO.cleanup()

    def __init__(self, options = {}):
        try:
            self.pins = self.PINS[options['side']]
        except KeyError:
            raise ValueError("'side' option is required. Valid values: " + str(self.PINS.keys()))

        # Numbers GPIOs by physical location
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.pins['pwm'], GPIO.OUT)
        GPIO.setup(self.pins['primary'], GPIO.OUT)
        GPIO.setup(self.pins['secondry'], GPIO.OUT)

        GPIO.output(self.pins['pwm'], GPIO.HIGH)
        GPIO.output(self.pins['primary'], GPIO.LOW)
        GPIO.output(self.pins['secondry'], GPIO.LOW)

        self.pwm = GPIO.PWM(self.pins['pwm'], self.PWM_FQ)
        self.pwm.start(0)

    def stop(self):
        self.pwm.ChangeDutyCycle(0)
        GPIO.output(self.pins['primary'], GPIO.LOW)
        GPIO.output(self.pins['secondry'], GPIO.LOW)

    def set_level(self, level):
        self.pwm.ChangeDutyCycle(level)

    def set_rotation(self, reverse):
        if reverse:
            GPIO.output(self.pins['primary'], GPIO.LOW)
            GPIO.output(self.pins['secondry'], GPIO.HIGH)
        else:
            GPIO.output(self.pins['primary'], GPIO.HIGH)
            GPIO.output(self.pins['secondry'], GPIO.LOW)

class DebugWheel:
    @classmethod
    def cleanup(cls):
        print('[WHEEL] CLEANUP')

    def __init__(self, options = {}):
        self.side = options['side'].upper().ljust(5)

    def stop(self):
        self.say('STOPPED')

    def set_level(self, level):
        self.say('TQ: ' + str(level))

    def set_rotation(self, reverse):
        self.say('RT: ' + str(reverse))

    def say(self, message):
        print('[' + self.side + '] ' + message)
