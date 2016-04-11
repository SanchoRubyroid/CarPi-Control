from wheel import Wheel

class Vehicle:
    STRAIGHT = 0
    LEFT = -1
    RIGHT = 1

    TORQUE_LEVEL = 'torque_level'
    REVERSE = 'reverse'
    DIRECTION_LEVEL = 'direction_level'
    DIRECTION = 'direction'

    EXTERNAL_MAPPING = {
        TORQUE_LEVEL: 'torqueLevel',
        REVERSE: 'torqueReversed',
        DIRECTION_LEVEL: 'directionLevel',
        DIRECTION: 'direction'
    }

    def __init__(self, name, initial_vehicle_state = {}):
        self.name = name

        initial_vehicle_state.setdefault(self.TORQUE_LEVEL, 0)
        initial_vehicle_state.setdefault(self.REVERSE, False)
        initial_vehicle_state.setdefault(self.DIRECTION_LEVEL, 0)
        initial_vehicle_state.setdefault(self.DIRECTION, self.STRAIGHT)

        self.vehicle_state = initial_vehicle_state

        self.left_wheel = Wheel({'side': 'left'})
        self.right_wheel = Wheel({'side': 'right'})

    def shutdown(self):
        self.left_wheel.shutdown
        self.right_wheel.shutdown

    def update(self, data):
        self.vehicle_state[self.TORQUE_LEVEL] = float(data[self.EXTERNAL_MAPPING[self.TORQUE_LEVEL]])
        self.vehicle_state[self.REVERSE] = data[self.EXTERNAL_MAPPING[self.REVERSE]]
        self.vehicle_state[self.DIRECTION_LEVEL] = float(data[self.EXTERNAL_MAPPING[self.DIRECTION_LEVEL]])
        self.vehicle_state[self.DIRECTION] = int(data[self.EXTERNAL_MAPPING[self.DIRECTION]])

        if self.vehicle_state[self.TORQUE_LEVEL] == 0:
            self.left_wheel.stop()
            self.right_wheel.stop()
            return

        if self.is_turning():
            torque_level_turning_side = self.calculate_torque_level_turning_side()

        if self.vehicle_state[self.DIRECTION] == self.LEFT:
            self.left_wheel.set_level(torque_level_turning_side)
            self.right_wheel.set_level(self.vehicle_state[self.TORQUE_LEVEL])
        elif self.vehicle_state[self.DIRECTION] == self.RIGHT:
            self.left_wheel.set_level(self.vehicle_state[self.TORQUE_LEVEL])
            self.right_wheel.set_level(torque_level_turning_side)
        else:
            self.left_wheel.set_level(self.vehicle_state[self.TORQUE_LEVEL])
            self.right_wheel.set_level(self.vehicle_state[self.TORQUE_LEVEL])

        self.left_wheel.set_rotation(self.vehicle_state[self.REVERSE])
        self.right_wheel.set_rotation(self.vehicle_state[self.REVERSE])

    def calculate_torque_level_turning_side(self):
        delta_percent = ((self.vehicle_state[self.TORQUE_LEVEL] * self.vehicle_state[self.DIRECTION_LEVEL]) / 100)
        return self.vehicle_state[self.TORQUE_LEVEL] - delta_percent

    def is_turning(self):
        return self.vehicle_state[self.DIRECTION] in [self.LEFT, self.RIGHT]

    # def to_s
    #     @vehicle_state.map {|key, value| "#{key}: #{value}" }.join('; ')
