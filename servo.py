from time import sleep
import digitalio
import pwmio
import adafruit_motor.servo as servo

class MyServo:
    motor: servo.Servo

    left: digitalio.Pin
    right: digitalio.Pin

    max_angle = 180
    min_angle = 0
    angle = 90
    step = 30

    def __init__(self, pwm: digitalio.Pin, left: digitalio.Pin, right: digitalio.Pin, min_pulse=600, max_pulse=2500):
        self.motor = servo.Servo(pwmio.PWMOut(pwm, frequency=50), min_pulse=min_pulse, max_pulse=max_pulse)
        self.left = self.__input_for(left)
        self.right = self.__input_for(right)
        self.motor.angle = 90

    def step_forward(self):
        self.set_position(self.angle + self.step)

    def step_backward(self):
        self.set_position(self.angle - self.step)

    def set_position(self, angle: int):
        if angle < self.min_angle or angle > self.max_angle:
            raise TypeError("Invalid motor position")
        self.angle = angle
        self.motor.angle = angle
        sleep(0.2)

    def __input_for(self, pin: digitalio.Pin):
        pin = digitalio.DigitalInOut(pin)
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.UP
        return pin

