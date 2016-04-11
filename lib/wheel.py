class Wheel:
    PINS = {
        'left': { 'pwm': 13, 'primary': 11, 'secondry': 15 },
        'right': { 'pwm': 12, 'primary': 16, 'secondry': 18 }
    }

    def __init__(self, options = {}):
        self.side = options['side']

        pins = self.PINS[options['side']]

        if not pins:
            # TODO!!!!
            raise ValueError("'side' option is required. Valid values: ['left', 'right']")

        # TODO!!!!
        # self.pwm = PiPiper::Pwm.new pin: pins[:pwm]
        # self.primary = PiPiper::Pin.new pin: pins[:primary], direction: :out
        # self.@secondry = PiPiper::Pin.new pin: pins[:secondry], direction: :out

    def stop(self):
        print self.side + ': STOP'
        #all_off

    def set_level(self, level):
        print self.side + ': SET LVL: ' + str(level)
        # self.pwm.on
        # self.pwm.value = (level / 100)

    def set_rotation(self, reverse):
        print self.side + ': ROTATION: ' + ('RV' if reverse else 'ST')
    #     if reverse:
    #         self.primary.off
    #         self.secondry.on
    #     else:
    #         self.primary.on
    #         self.secondry.off
    #
    # def all_off(self):
    #     @pwm.off
    #     @primary.off
    #     @secondry.off
