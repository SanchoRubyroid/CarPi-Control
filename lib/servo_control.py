try:
    from Sunfounder_PWM_Servo_Driver.Sunfounder_PWM_Servo_Driver import PWM
except ImportError:
    print("ERROR: servo driver import failed. DEBUG_MODE only.")

import time

class ServoControl:
    STEERING_UNIT = 'steering-unit'
    CAMERA_VERTICAL = 'camera-vertical'
    CAMERA_HORIZONTAL = 'camera-horizontal'

    CHANNELS = {
        STEERING_UNIT: 0,
        CAMERA_VERTICAL: 14,
        CAMERA_HORIZONTAL: 15
    }

    DEAD_POINTS_DETLA = {
        STEERING_UNIT: 90
    }

    HOME_VALUES = {
        STEERING_UNIT: 497
    }

    def __init__(self, servo_unit):
        self.channel = self.CHANNELS[servo_unit]

        self.dead_point_delta = self.DEAD_POINTS_DETLA[servo_unit]
        self.home = self.HOME_VALUES[servo_unit]

        self.pwm = PWM(0x40)
        self.pwm.setPWMFreq(60)

        self.set_home()

    def set_home(self):
        self.__setPWM(self.home)

    def set_percent_before_home(self, percent_level):
        value = self.home - self.__calc_delta(percent_level)
        self.__setPWM(value)

    def set_percent_after_home(self, percent_level):
        value = self.home + self.__calc_delta(percent_level)
        self.__setPWM(value)

    def __calc_delta(self, level):
        return ((level * self.dead_point_delta) / 100)

    def __setPWM(self, value):
        self.pwm.setPWM(self.channel, 0, int(round(value)))
