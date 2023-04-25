from time import sleep
import microcontroller
import board
import digitalio
import pwmio
import os
import adafruit_motor.servo as servo
import socketpool
import wifi
from adafruit_httpserver.mime_type import MIMEType
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.methods import HTTPMethod
from display import write
from page import render_page

### ===============================
pwm = pwmio.PWMOut(board.GP0, frequency=50)
servo = servo.Servo(pwm, min_pulse=600, max_pulse=2500)

left = digitalio.DigitalInOut(board.GP15)
left.direction = digitalio.Direction.INPUT
left.pull = digitalio.Pull.UP

right = digitalio.DigitalInOut(board.GP14)
right.direction = digitalio.Direction.INPUT
right.pull = digitalio.Pull.UP

msg = ""
pos = 90
step = 30

def set_motor_pos(angle, remote = False):
    global pos, msg
    print("Setting angle to", angle)
    mode = "Remote" if remote else "Manual"
    msg = write(f"Angle: {angle}", f"Source: {mode}")
    pos = angle
    servo.angle = pos
    sleep(0.20)

def move(angle):
    global pos
    set_motor_pos(pos + angle)

print("Connecting to WiFi")

for network in wifi.radio.start_scanning_networks():
    print(network, network.ssid, network.channel)
wifi.radio.stop_scanning_networks()

print("joining network...")

ssid = os.getenv('CIRCUITPY_WIFI_SSID')
passwd = os.getenv('CIRCUITPY_WIFI_PASSWORD')
wifi.radio.connect(ssid, passwd)

ip = wifi.radio.ipv4_address
print(f"Connected: {ip}")

pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool)

@server.route("/", method=HTTPMethod.GET)
def r_root(request: HTTPRequest):
    print("CALE TE")
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(render_page())


@server.route("/motor", method=HTTPMethod.POST)
def r_move(request: HTTPRequest):
    angle = int(request.query_params.get("a") or 90)
    if (angle < 0 or angle > 180):
        with HTTPResponse(request, content_type=MIMEType.TYPE_TXT) as response:
            response.send("Invalid kąt")
    else:
        with HTTPResponse(request, content_type=MIMEType.TYPE_TXT) as response:
            set_motor_pos(angle, True)
            response.send(f"Rotor position set to {angle}", angle)

@server.route("/data", method=HTTPMethod.GET)
def r_data(request:HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_JSON) as response:
        text = msg.replace('\n', '\\n')
        response.send(f'{{ "angle": {pos}, "text": "{text}" }}')

print("starting server..")

try:
    server.start(str(wifi.radio.ipv4_address))
    print("Listening on http://%s:80" % wifi.radio.ipv4_address)
    set_motor_pos(pos)
except OSError:
    sleep(5)
    print("restarting..")
    microcontroller.reset()

while True:
    try:
        if not left.value and pos - step >= 0:
            move(-step)
        elif not right.value and pos + step <= 180:
            move(step)
        server.poll()
        sleep(0.15)
    except Exception as e:
        print(e)
        continue

