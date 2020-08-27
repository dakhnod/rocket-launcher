#!/usr/bin/python3



import os
import usb.core
import threading
import time


class LaunchControl:
    def __init__(self):
        if not os.geteuid() == 0:
            raise Exception("Script must be run as root.")
        self.dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
        if self.dev is None:
            raise ValueError('Launcher not found.')
        if self.dev.is_kernel_driver_active(0) is True:
            self.dev.detach_kernel_driver(0)
        self.dev.set_configuration()
        self.shot_mutex = threading.Lock()
        
    def parse_command(self, command):
        if self.shot_mutex.locked():
            print('currently firing...')
            return
        if command == 'down':
            print("going down")
            self.turretDown()
        if command == 'up':
            print("going up")
            self.turretUp()
        if command == 'left':
            print("going left")
            self.turretLeft()
        if command == 'right':
            print("going right")
            self.turretRight()
        if command == 'stop':
            print("stopping")
            self.turretStop()
        if command == 'fire':
            def fire(mutex):
                mutex.acquire()
                print("fire!!!")
                self.turretStop()
                self.turretFire()
                time.sleep(4)
                mutex.release()

            threading.Thread(target=fire, args=(self.shot_mutex,)).start()

    def turretUp(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretDown(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretLeft(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretRight(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretStop(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretFire(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])