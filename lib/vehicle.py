from wheel import Wheel, DebugWheel

class Vehicle:
    STRAIGHT = 0
    LEFT = -1
    RIGHT = 1

    TORQUE_LEVEL_INDEX = 0
    DIRECTION_LEVEL_INDEX = 1
    STATUS_INDEX = 2

    REVERSE_MASK = 0b00000100
    DIRECTION_RIGHT_MASK = 0b00000001
    DIRECTION_LEFT_MASK = 0b00000010

    TORQUE_LEVEL = 'torque_level'
    REVERSE = 'reverse'
    DIRECTION_LEVEL = 'direction_level'
    DIRECTION = 'direction'

    def __init__(self, options, initial_vehicle_state = {}):
        self.name = options['vehicle_name']

        initial_vehicle_state.setdefault(self.TORQUE_LEVEL, 0)
        initial_vehicle_state.setdefault(self.REVERSE, False)
        initial_vehicle_state.setdefault(self.DIRECTION_LEVEL, 0)
        initial_vehicle_state.setdefault(self.DIRECTION, self.STRAIGHT)
        self.vehicle_state = initial_vehicle_state

        options.setdefault('debug_mode', False)
        self.options = options

        the_wheel_klass = (DebugWheel if self.options['debug_mode'] else Wheel)

        self.left_wheel = the_wheel_klass({'side': 'left'})
        self.right_wheel = the_wheel_klass({'side': 'right'})

    def update(self, data):
        self.update_vehicle_state_values(data)

        if self.torque_level() == 0:
            self.stop_vehicle()
        else:
            self.update_wheels_torque()
            self.update_wheels_rotation()

    def stop_vehicle(self):
        self.left_wheel.stop()
        self.right_wheel.stop()

    def shutdown(self):
        self.stop_vehicle()
        (DebugWheel if self.options['debug_mode'] else Wheel).cleanup()

    def update_vehicle_state_values(self, data):
        self.vehicle_state[self.TORQUE_LEVEL] = data[self.TORQUE_LEVEL_INDEX]
        self.vehicle_state[self.REVERSE] = self.get_from_status(data[self.STATUS_INDEX], 'reverse')
        self.vehicle_state[self.DIRECTION_LEVEL] = data[self.DIRECTION_LEVEL_INDEX]
        self.vehicle_state[self.DIRECTION] = self.get_from_status(data[self.STATUS_INDEX], 'direction')

    def get_from_status(self, status_bits, status_type):
        if status_type == 'reverse':
            return ((status_bits & self.REVERSE_MASK) > 0)
        elif status_type == 'direction':
            if ((status_bits & self.DIRECTION_RIGHT_MASK) > 0):
                return self.RIGHT
            elif ((status_bits & self.DIRECTION_LEFT_MASK) > 0):
                return self.LEFT
            else:
                return self.STRAIGHT
        else:
            return 'Bad type'

    def update_wheels_torque(self):
        if self.is_turning():
            torque_level_turning_side = self.calculate_torque_level_turning_side()

        if self.direction() == self.LEFT:
            self.left_wheel.set_level(torque_level_turning_side)
            self.right_wheel.set_level(self.torque_level())
        elif self.direction() == self.RIGHT:
            self.left_wheel.set_level(self.torque_level())
            self.right_wheel.set_level(torque_level_turning_side)
        else:
            self.left_wheel.set_level(self.torque_level())
            self.right_wheel.set_level(self.torque_level())

    def update_wheels_rotation(self):
        self.left_wheel.set_rotation(self.reverse())
        self.right_wheel.set_rotation(self.reverse())

    def calculate_torque_level_turning_side(self):
        delta_percent = ((self.torque_level() * self.direction_level()) / 100)
        return self.torque_level() - delta_percent

    def is_turning(self):
        return self.direction() in [self.LEFT, self.RIGHT]

    def torque_level(self):
        return self.get_state_value(self.TORQUE_LEVEL)

    def reverse(self):
        return self.get_state_value(self.REVERSE)

    def direction_level(self):
        return self.get_state_value(self.DIRECTION_LEVEL)

    def direction(self):
        return self.get_state_value(self.DIRECTION)

    def get_state_value(self, key):
        return self.vehicle_state[key]
