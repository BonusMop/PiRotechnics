# Operate a demultiplexer with Pi's GPIO
import sys

# If FakeRPi is already loaded, we're unit testing. Otherwise, we need the real 
# thing.
if 'FakeRPi.GPIO' in sys.modules:
    import FakeRPi.GPIO as GPIO
else:
    import RPi.GPIO as GPIO

class Demux:
    def __init__(self, inhibit_pin, data_pins):
        if len(data_pins) != 4:
            raise ValueError("must specify 4 data pins")
        self._inhibit_pin = inhibit_pin
        self._data_pins = data_pins
        self.initialize_pins()

    def initialize_pins(self):
        original_mode = GPIO.getmode()
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self._inhibit_pin, GPIO.OUT)
            GPIO.output(self._inhibit_pin, GPIO.HIGH)
            for index in range(len(self._data_pins)):
                GPIO.setup(self._data_pins[index], GPIO.OUT)
                GPIO.output(self._data_pins[index], GPIO.LOW)
        finally:
            if original_mode != None:
                GPIO.setmode(original_mode)

    def inhibit(self):
        original_mode = GPIO.getmode()
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.output(self._inhibit_pin, GPIO.HIGH)
        finally:
            if original_mode != None:
                GPIO.setmode(original_mode)
    
    def uninhibit(self):
        original_mode = GPIO.getmode()
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.output(self._inhibit_pin, GPIO.LOW)
        finally:
            if original_mode != None:
                GPIO.setmode(original_mode)

    def signal(self, value):
        original_mode = GPIO.getmode()
        try:
            GPIO.setmode(GPIO.BOARD)
            if value & 1:
                GPIO.output(self._data_pins[0], GPIO.HIGH)
            else:
                GPIO.output(self._data_pins[0], GPIO.LOW)
            if value & 2:
                GPIO.output(self._data_pins[1], GPIO.HIGH)
            else:
                GPIO.output(self._data_pins[1], GPIO.LOW)
            if value & 4:
                GPIO.output(self._data_pins[2], GPIO.HIGH)
            else:
                GPIO.output(self._data_pins[2], GPIO.LOW)
            if value & 8:
                GPIO.output(self._data_pins[3], GPIO.HIGH)
            else:
                GPIO.output(self._data_pins[3], GPIO.LOW)
        finally:
            if original_mode != None:
                GPIO.setmode(original_mode)

    def reset(self):
        original_mode = GPIO.getmode()
        try:
            GPIO.setmode(GPIO.BOARD)
            for index in range(len(self._data_pins)):
                GPIO.output(self._data_pins[index], GPIO.LOW)
        finally:
            if original_mode != None:
                GPIO.setmode(original_mode)
