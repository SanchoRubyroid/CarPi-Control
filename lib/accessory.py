try:
    import RPi.GPIO as GPIO
except ImportError:
    print 'ERROR: RPi.GPIO import failed. DEBUG_MODE only.'

class Accessory:
    GLOBAL_ENABLE = 'global-enable'
    LIGHTS = 'lights'

    PINS = {
        GLOBAL_ENABLE: 22,
        LIGHTS: 29
    }

    INITIAL_STATE = {
        GLOBAL_ENABLE: GPIO.LOW,
        LIGHTS: GPIO.HIGH
    }

    def __init__(self, features):
        self.supported_features = features

        # Numbers GPIOs by physical location
        GPIO.setmode(GPIO.BOARD)

        for feature in features:
            GPIO.setup(self.PINS[feature], GPIO.OUT)
            GPIO.output(self.PINS[feature], self.INITIAL_STATE[feature])

    def enable(self, feature):
        if feature in self.supported_features:
            self.__set_pin(self.PINS[feature], GPIO.LOW)

    def disable(self, feature):
        if feature in self.supported_features:
            self.__set_pin(self.PINS[feature], GPIO.HIGH)

    def __set_pin(self, pin, value):
        GPIO.output(pin, value)

class DebugAccessory(Accessory):
    def __init__(self, features):
        self.supported_features = features

    def enable(self, feature):
        if feature in self.supported_features:
            print 'Accessory ' + feature + ' is enabled'

    def disable(self, feature):
        if feature in self.supported_features:
            print 'Accessory ' + feature + ' is disabled'
