import http.server
from threading import Lock, Thread

import io
import time


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.handle_main()
        elif self.path.startswith('/stream'):
            self.send_response(302)
            self.send_header('Location', 'http://192.168.0.159:81/?action=stream')
            self.end_headers()
        elif self.path == ('/control'):
            self.send_response(302)
            self.send_header('Location', 'ws://192.168.0.159:82')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_main(self):
        with open('main.html', 'r') as inputFile:
            self.send_response(200)
            self.end_headers()

            self.send(inputFile.read())

    def do_PUT(self):
        if self.path == '/control':
            self.send_response(200)
            self.end_headers()

            length = int(self.headers['Content-Length'])
            command = self.rfile.read(length).decode('utf-8')
            self.server.launcher.parse_command(command)

    def send(self, str):
        self.wfile.write(bytes(str, 'utf-8'))


class WebServer:
    def __init__(self, launcher):
        self.launcher = launcher

    def start(self):
        server = http.server.ThreadingHTTPServer(('', 80), Handler)
        server.launcher = self.launcher
        # server.camera = picamera.PiCamera()
        # server.camera.resolution = (640, 480)
        # server.camera.rotation = 270
        print('web server started')
        server.serve_forever(0.1)
