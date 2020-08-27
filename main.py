#!/usr/bin/python3 -u

import WebServer
import RocketLauncher
import control_socket
import threading

# import pydevd_pycharm
# pydevd_pycharm.settrace('192.168.0.146', port=1324, stdoutToServer=True, stderrToServer=True)


def main():
    control = RocketLauncher.LaunchControl()

    def web_server_start(launch_control):
        WebServer.WebServer(launch_control).start()

    threading.Thread(target=web_server_start, args=(control, )).start()
    control_socket.control_socket_start(control)


if __name__ == '__main__':
    main()
