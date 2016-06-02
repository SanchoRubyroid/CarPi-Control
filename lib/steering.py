from servo_control import ServoControl

class Steering:
    TANK_STRATEGY = 'tank'
    SERVO_STRATEGY = 'servo'

    STRAIGHT = 0
    LEFT = -1
    RIGHT = 1

    @classmethod
    def get(cls, steering_strategy):
        if steering_strategy == cls.TANK_STRATEGY:
            return SteeringTank()
        elif steering_strategy == cls.SERVO_STRATEGY:
            return SteeringServo()
        else:
            raise ValueError('Unrecognized steering strategy.')

    def calculate_torque_level_turning_side(self, torque_level, _1, _2):
        return torque_level

    def update(self, _1, _2):
        return True

    def set_center(self):
        return True

    def is_tank(self):
        return self.strategy == self.TANK_STRATEGY

class SteeringTank(Steering):
    def __init__(self):
        self.strategy = self.TANK_STRATEGY

    def calculate_torque_level_turning_side(self, torque_level, direction_level, turning_apex):
        if direction_level > turning_apex:
            direction_level = turning_apex*2 - direction_level

        direction_level *= 100/turning_apex

        delta_percent = ((torque_level * direction_level) / 100)
        return torque_level - delta_percent

class SteeringServo(Steering):
    def __init__(self):
        self.strategy = SERVO_STRATEGY
        self.steering_servo = ServoControl(ServoControl.STEERING_UNIT)

    def set_center(self):
        self.steering_servo.set_home()

    def update(self, direction_level, direction):
        if direction == self.LEFT:
            self.steering_servo.set_percent_before_home(direction_level)
        elif direction == self.RIGHT:
            self.steering_servo.set_percent_after_home(direction_level)
        else:
            self.set_center()
