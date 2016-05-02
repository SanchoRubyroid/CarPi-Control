from wheel import Wheel, DebugWheel
from accessory import Accessory, DebugAccessory
from steering import Steering
from status_bits import StatusBits

class Vehicle:
    TORQUE_LEVEL_INDEX = 0
    DIRECTION_LEVEL_INDEX = 1
    STATUS_INDEX = 2

    TORQUE_LEVEL = 'torque_level'
    REVERSE = 'reverse'
    DIRECTION_LEVEL = 'direction_level'
    DIRECTION = 'direction'

    def __init__(self, options):
        options.setdefault('debug_mode', False)

        self.name = options['vehicle_name']
        self.debug_mode = options['debug_mode']

        self.steering = Steering.get(options['steering_strategy'])

        the_wheel_klass = (DebugWheel if self.debug_mode else Wheel)
        self.left_wheel = the_wheel_klass({'side': 'left'})
        self.right_wheel = the_wheel_klass({'side': 'right'})

        initial_vehicle_state = {
            self.TORQUE_LEVEL: 0,
            self.REVERSE: False,
            self.DIRECTION_LEVEL: 0,
            self.DIRECTION: self.steering.STRAIGHT
        }
        self.vehicle_state = initial_vehicle_state

        the_accessory_klass = (DebugAccessory if self.debug_mode else Accessory)
        self.accessory = the_accessory_klass(options['accessories'])
        self.accessory.enable(Accessory.GLOBAL_ENABLE)

    def update(self, data):
        self.update_vehicle_state_values(data)

        if self.torque_level() == 0:
            self.stop_vehicle()
        else:
            self.update_wheels_torque()
            self.update_wheels_rotation()
            self.update_steering()

    def stop_vehicle(self):
        self.left_wheel.stop()
        self.right_wheel.stop()
        self.steering.set_center()

    def shutdown(self):
        self.stop_vehicle()
        self.accessory.disable(Accessory.GLOBAL_ENABLE)
        (DebugWheel if self.debug_mode else Wheel).cleanup()

    def update_vehicle_state_values(self, data):
        status_bits = StatusBits(data[self.STATUS_INDEX])

        self.vehicle_state[self.TORQUE_LEVEL] = data[self.TORQUE_LEVEL_INDEX]
        self.vehicle_state[self.REVERSE] = status_bits.reversed()
        self.vehicle_state[self.DIRECTION_LEVEL] = data[self.DIRECTION_LEVEL_INDEX]

        if status_bits.direction_right():
            self.vehicle_state[self.DIRECTION] = self.steering.RIGHT
        elif status_bits.direction_left():
            self.vehicle_state[self.DIRECTION] = self.steering.LEFT
        else:
            self.vehicle_state[self.DIRECTION] = self.steering.STRAIGHT

    def update_wheels_torque(self):
        if self.is_turning():
            torque_level_turning_side = self.steering.calculate_torque_level_turning_side(self.torque_level(), self.direction_level())

        if self.direction() == self.steering.LEFT:
            self.left_wheel.set_level(torque_level_turning_side)
            self.right_wheel.set_level(self.torque_level())
        elif self.direction() == self.steering.RIGHT:
            self.left_wheel.set_level(self.torque_level())
            self.right_wheel.set_level(torque_level_turning_side)
        else:
            self.left_wheel.set_level(self.torque_level())
            self.right_wheel.set_level(self.torque_level())

    def update_wheels_rotation(self):
        self.left_wheel.set_rotation(self.reverse())
        self.right_wheel.set_rotation(self.reverse())

    def update_steering(self):
        self.steering.update(self.direction_level(), self.direction())

    def is_turning(self):
        return self.direction() in [self.steering.LEFT, self.steering.RIGHT]

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
