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

    def calculate_torque_level_turning_side(self, torque_level, _1):
        return torque_level

    def update(self, _1, _2):
        return True

class SteeringTank(Steering):
    def calculate_torque_level_turning_side(self, torque_level, direction_level):
        delta_percent = ((torque_level * direction_level) / 100)
        return torque_level - delta_percent

class SteeringServo(Steering):
    def __init__(self):
        self.steering_servo = ServoControl('steering')

    def update(self, direction_level, direction):
        if direction == self.LEFT:
            self.steering_servo.turn_left(direction_level)
        elif direction == self.RIGHT:
            self.steering_servo.turn_right(direction_level)
