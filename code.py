import board
from time import sleep
import microcontroller
import wifi
from adafruit_httpserver.server import HTTPServer

from display import MyDisplay
from servo import MyServo
from ssid_connect import pool
from controller import Controller

servo = MyServo(pwm=board.GP0, left=board.GP15, right= board.GP14)
display = MyDisplay(rs=board.GP9, en=board.GP8, d7=board.GP13, d6=board.GP12, d5=board.GP11, d4=board.GP10)
server = HTTPServer(pool)
controller = Controller(server, servo, display).combine_routes()
controller.update_display()

try:
    server.start(str(wifi.radio.ipv4_address))
    print("Listening on http://%s:80" % wifi.radio.ipv4_address)
except OSError:
    sleep(5)
    print("restarting..")
    microcontroller.reset()

while True:
    try:
        if not servo.left.value:
            controller.manual_step_backward()
        elif not servo.right.value:
            controller.manual_step_forward()
        else:
            server.poll()
            sleep(0.5)
    except Exception as e:
        print(e)
        sleep(1)
        continue

