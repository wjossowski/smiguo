import board
from time import sleep
import microcontroller
import wifi
from display import MyDisplay
from servo import MyServo
from ssid_connect import pool

from adafruit_httpserver.mime_type import MIMEType
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.methods import HTTPMethod

servo = MyServo(pwm=board.GP0, left=board.GP15, right= board.GP14)
display = MyDisplay(rs=board.GP9, en=board.GP8, d7=board.GP13, d6=board.GP12, d5=board.GP11, d4=board.GP10)

def set_motor_pos(angle, source = "Manual"):
    print("Setting angle to:", angle, "Source:", source)
    servo.set_position(angle)
    display.write(f"Angle: {servo.angle}", source)

server = HTTPServer(pool)
@server.route("/", method=HTTPMethod.GET)
def r_root(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send_file("index.html")

@server.route("/motor", method=HTTPMethod.POST)
def r_move(request: HTTPRequest):
    angle = int(request.query_params.get("a") or 90)
    with HTTPResponse(request, content_type=MIMEType.TYPE_TXT) as response:
        addr, _ = request.client_address
        set_motor_pos(angle, addr)
        response.send(f"Rotor position set to {angle}", angle)

@server.route("/data", method=HTTPMethod.GET)
def r_data(request:HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_JSON) as response:
        response.send(f'{{ "angle": {servo.angle}, "text": "{display.msg}" }}')

print("starting server..")

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
            servo.step_backward()
        elif not servo.right.value:
            servo.step_forward()
        else:
            server.poll()
            sleep(0.5)
    except Exception as e:
        print(e)
        continue

