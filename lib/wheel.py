import RPi.GPIO as GPIO

class Wheel:
    PINS = {
        'left': { 'pwm': 13, 'primary': 11, 'secondry': 15 },
        'right': { 'pwm': 12, 'primary': 16, 'secondry': 18 }
    }

    # PWM Frequece
    PWM_FQ = 500

    def __init__(self, options = {}):
        # self.side = options['side']
        self.pins = self.PINS[options['side']]

        if not self.pins:
            # TODO!!!!
            raise ValueError("'side' option is required. Valid values: ['left', 'right']")

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

    def shutdown(self):
        self.stop()
        GPIO.cleanup()

    def stop(self):
        # print self.side + ': STOP'
        self.pwm.ChangeDutyCycle(0)
        GPIO.output(self.pins['primary'], GPIO.LOW)
        GPIO.output(self.pins['secondry'], GPIO.LOW)

    def set_level(self, level):
        # print self.side + ': SET LVL: ' + str(level)
        self.pwm.ChangeDutyCycle(level)

    def set_rotation(self, reverse):
        # print self.side + ': ROTATION: ' + ('RV' if reverse else 'ST')
        if reverse:
            GPIO.output(self.pins['primary'], GPIO.LOW)
            GPIO.output(self.pins['secondry'], GPIO.HIGH)
        else:
            GPIO.output(self.pins['primary'], GPIO.HIGH)
            GPIO.output(self.pins['secondry'], GPIO.LOW)
