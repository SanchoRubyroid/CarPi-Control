class StatusBits:
    REVERSE_MASK = 0b00000100
    DIRECTION_RIGHT_MASK = 0b00000001
    DIRECTION_LEFT_MASK = 0b00000010

    def __init__(self, status_bits):
        self.status_bits = status_bits

    def reversed(self):
        return self.__apply_mask(self.REVERSE_MASK)

    def direction_right(self):
        return self.__apply_mask(self.DIRECTION_RIGHT_MASK)

    def direction_left(self):
        return self.__apply_mask(self.DIRECTION_LEFT_MASK)

    def __apply_mask(self, mask):
        return ((self.status_bits & mask) > 0)
