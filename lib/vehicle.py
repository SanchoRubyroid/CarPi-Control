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
        self.set_turning_apex(float(options['vehicle_turning_apex']))

        the_accessory_klass = (DebugAccessory if self.debug_mode else Accessory)
        self.accessory = the_accessory_klass(options['accessories'])

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

    def update(self, data):
        self.update_vehicle_state_values(data)

        if self.torque_level() == 0 and self.direction_level() == 0:
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

    def toggle_lights(self):
        self.accessory.toggle(Accessory.LIGHTS)

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
        left_torque = right_torque = self.torque_level()

        if self.is_turning():
            torque_level_turning_side = self.steering.calculate_torque_level_turning_side(self.torque_level(), self.direction_level(), self.turning_apex)

        if self.direction() == self.steering.LEFT:
            left_torque = torque_level_turning_side
        elif self.direction() == self.steering.RIGHT:
            right_torque = torque_level_turning_side

        self.left_wheel.set_level(left_torque)
        self.right_wheel.set_level(right_torque)

    def update_wheels_rotation(self):
        left_reverse = right_reverse = self.reverse()

        if self.steering.is_tank():
            if self.direction() == self.steering.LEFT and self.direction_level() > self.turning_apex:
                left_reverse = not self.reverse()
            elif self.direction() == self.steering.RIGHT and self.direction_level() > self.turning_apex:
                right_reverse = not self.reverse()

        self.left_wheel.set_rotation(left_reverse)
        self.right_wheel.set_rotation(right_reverse)

    def update_steering(self):
        self.steering.update(self.direction_level(), self.direction())

    def set_turning_apex(self, turning_apex):
        if turning_apex < 50 or turning_apex > 100:
            raise ValueError('Turning apex must be in range 50..100')
        self.turning_apex = turning_apex

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
