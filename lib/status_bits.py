class StatusBits:
    DIRECTION_RIGHT_MASK = 1<<0
    DIRECTION_LEFT_MASK = 1<<1
    REVERSE_MASK = 1<<2

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
