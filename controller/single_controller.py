import threading
import time

from controller.constants import *


class SingleController:
    light_array = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    buttonState = {"red": False, "blue": False, "orange": False, "green": False, "yellow": False}

    def __init__(self, controller_id, device):
        self.light = OFF
        self.controller_id = controller_id
        self.device = device

    def light_off(self):
        self.light = OFF

        self.light_array[self.controller_id + 2] = 0x00
        self.device.write(self.light_array)

    def light_on(self):
        self.light = ON

        self.light_array[self.controller_id + 2] = 0xFF
        self.device.write(self.light_array)

    def light_blinking(self):
        self.light = BLINKING

        threading.Thread(target=self.blink, ).start()

    def blink(self):
        blink = False
        while self.light == BLINKING:
            if blink:
                self.light_array[self.controller_id + 2] = 0x00
                self.device.write(self.light_array)
            else:
                self.light_array[self.controller_id + 2] = 0x00
                self.device.write(self.light_array)
            blink = not blink
            time.sleep(0.5)
