import unittest
from mock import patch, call
import FakeRPi.GPIO as GPIO
from demux import Demux

# FakeRPi.GPIO doesn't implement getmode
def getmode():
    return getattr(GPIO, "_setup_mode")
setattr(GPIO, "getmode", getmode)

@patch("FakeRPi.GPIO.output", autospec=True)
class TestDeumx(unittest.TestCase):
    def test_init(self, mock_output):
        with patch("FakeRPi.GPIO.setup", autospec=True) as mock_setup:
            exp_inhibit = 12
            exp_pins = [4, 19, 1, 3]
            d = Demux(exp_inhibit, exp_pins)
            self.assertEqual(exp_inhibit, d._inhibit_pin)
            self.assertEqual(exp_pins, d._data_pins)
            mock_output.assert_has_calls([
                call(exp_inhibit, GPIO.HIGH),
                call(exp_pins[0], GPIO.LOW),
                call(exp_pins[1], GPIO.LOW),
                call(exp_pins[2], GPIO.LOW),
                call(exp_pins[3], GPIO.LOW)
                ], any_order=True)
            mock_setup.assert_has_calls([
                call(exp_inhibit, GPIO.OUT),
                call(exp_pins[0], GPIO.OUT),
                call(exp_pins[1], GPIO.OUT),
                call(exp_pins[2], GPIO.OUT),
                call(exp_pins[3], GPIO.OUT)
                ], any_order=True)

    def test_init_fails_without_four_pins(self, mock_output):
        exp_inhibit = 12
        exp_pins = [4, 19, 1]
        with self.assertRaises(ValueError):
            Demux(exp_inhibit, exp_pins)
    
    # TODO: my getmode hack allows the test to run, but isn't accurate
    # TODO: test to ensure pin mode is restored
    # def test_init_preserves_pin_mode(self, mock_output):

    def test_inhibit(self, mock_output):
        exp_inhibit = 12
        exp_pins = [4, 19, 1, 3]
        d = Demux(exp_inhibit, exp_pins)
        mock_output.reset_mock()
        d.inhibit()
        mock_output.assert_has_calls([call(exp_inhibit, GPIO.HIGH)], any_order=True)

    def test_uninhibit(self, mock_output):
        exp_inhibit = 2
        exp_pins = [8, 3, 6, 10]
        d = Demux(exp_inhibit, exp_pins)
        mock_output.reset_mock()
        d.uninhibit()
        mock_output.assert_has_calls([call(exp_inhibit, GPIO.LOW)], any_order=True)

    def test_signal(self, mock_output):
        exp_inhibit = 21
        exp_pins = [4, 5, 6, 8]
        d = Demux(exp_inhibit, exp_pins)
        mock_output.reset_mock()
        d.signal(3)
        mock_output.assert_has_calls([call(exp_pins[0], GPIO.HIGH), call(exp_pins[1], GPIO.HIGH)], any_order=True)
        mock_output.reset_mock()
        d.signal(8)
        mock_output.assert_has_calls([call(exp_pins[3], GPIO.HIGH)], any_order=True)

    def test_reset(self, mock_output):
        exp_inhibit = 21
        exp_pins = [4, 5, 6, 8]
        d = Demux(exp_inhibit, exp_pins)
        mock_output.reset_mock()
        d.reset()
        mock_output.assert_has_calls([call(exp_pins[0], GPIO.LOW), call(exp_pins[1], GPIO.LOW), call(exp_pins[2], GPIO.LOW), call(exp_pins[3], GPIO.LOW)], any_order=True)

if __name__ == '__main__':
    unittest.main()