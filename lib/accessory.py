try:
    import RPi.GPIO as GPIO
except ImportError:
    print('ERROR: RPi.GPIO import failed. DEBUG_MODE only.')
    import debug_gpio as GPIO

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
        self.__set_feature_if_supported(self, feature, GPIO.LOW)

    def disable(self, feature):
        self.__set_feature_if_supported(self, feature, GPIO.HIGH)

    def __set_feature_if_supported(self, feature, status):
        if feature in self.supported_features:
            GPIO.output(self.PINS[feature], status)

class DebugAccessory(Accessory):
    def __init__(self, features):
        self.supported_features = features

    def enable(self, feature):
        self.__set_feature_if_supported(self, feature, 'enabled')

    def disable(self, feature):
        self.__set_feature_if_supported(self, feature, 'disabled')

    def __set_feature_if_supported(self, feature, status):
        if feature in self.supported_features:
            print('Accessory ' + feature + ' is ' + status)
