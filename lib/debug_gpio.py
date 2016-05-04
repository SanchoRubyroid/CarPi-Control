# -*- coding: UTF-8 -*-
LOW = 0
HIGH = 1

IN = '↓'
OUT = '↑'

PINS = {}

@classmethod
def setup(cls, pin, direction):
    cls.PINS[pin] = direction
    cls.__say(pin, "Setup completed.")

@classmethod
def output(cls, pin, status):
    cls.__say(pin, "Set status to " + status)

@classmethod
def __say(cls, pin, message):
    print "[GPIO " + pin + cls.PINS[pin] + "] " + message
