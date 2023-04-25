from adafruit_httpserver.mime_type import MIMEType
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.server import HTTPServer
from display import MyDisplay
from servo import MyServo

class Controller:
    server: HTTPServer
    motor: MyServo
    display: MyDisplay

    def __init__(self, server: HTTPServer, servo: MyServo, display: MyDisplay ):
        self.server = server
        self.motor = servo
        self.display = display

    def combine_routes(self):
        @self.server.route("/", method=HTTPMethod.GET)
        def r_root(request: HTTPRequest):
            with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
                response.send_file("index.html")

        @self.server.route("/motor", method=HTTPMethod.POST)
        def r_move(request: HTTPRequest):
            angle = int(request.query_params.get("a") or 90)
            with HTTPResponse(request, content_type=MIMEType.TYPE_TXT) as response:
                self.motor.set_position(angle)
                addr, _ = request.client_address
                self.update_display(addr)
                response.send()

        @self.server.route("/data", method=HTTPMethod.GET)
        def r_data(request:HTTPRequest):
            with HTTPResponse(request, content_type=MIMEType.TYPE_JSON) as response:
                response.send(f'{{ "angle": {self.motor.angle}, "text": "{self.display.msg}" }}')

        @self.server.route("/text", method=HTTPMethod.POST)
        def r_display(request: HTTPRequest):
            line1 = request.query_params.get("l1")
            line2 = request.query_params.get("l2")
            with HTTPResponse(request, content_type=MIMEType.TYPE_JSON) as response:
                print(line1, line2, 'HEHEHE   ')
                self.display.write(line1, line2)
                response.send()

        print("starting server..")
        return self
    
    def manual_step_forward(self):
        self.motor.step_forward()
        self.update_display()

    def manual_step_backward(self):
        self.motor.step_backward()
        self.update_display()

    def update_display(self, source = "Manual"):
        print("Setting angle to:", self.motor.angle, "Source:", source)
        self.display.write(f"Angle: {self.motor.angle}", source)

