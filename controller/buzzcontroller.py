import hid
import logging

from controller.single_controller import SingleController


class BuzzController:
    light_array = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    def __init__(self):
        self.logger = logging.getLogger("log")

        # instantiate the device class
        self.blink_lights_on = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.hid = hid.device()

        # Open up the device (use vendor_id and product_id)
        self.hid.open(0x54c, 0x2)

        self.logger.debug("Connection successful")

        # Set the non blocking mode
        self.hid.set_nonblocking(1)

        # Clear the Buzz Controller LEDs
        self.hid.write(self.light_array)
        self.logger.debug("lights off")

        controller1 = SingleController(0, self.hid)
        controller2 = SingleController(1, self.hid)
        controller3 = SingleController(2, self.hid)
        controller4 = SingleController(3, self.hid)
        self.controller = [controller1, controller2, controller3, controller4]
        self.logger.debug("controller classes instantiated")

    def get_controller(self, controller_id):
        return self.controller[controller_id]

    def get_button_status(self):
        data = self.hid.read(5)
        button_state = [{}, {}, {}, {}]
        if data:
            button_state[0]["red"] = ((data[2] & 0x01) != 0)  # red
            button_state[0]["yellow"] = ((data[2] & 0x02) != 0)  # yellow
            button_state[0]["green"] = ((data[2] & 0x04) != 0)  # green
            button_state[0]["orange"] = ((data[2] & 0x08) != 0)  # orange
            button_state[0]["blue"] = ((data[2] & 0x10) != 0)  # blue

            button_state[1]["red"] = ((data[2] & 0x20) != 0)  # red
            button_state[1]["yellow"] = ((data[2] & 0x40) != 0)  # yellow
            button_state[1]["green"] = ((data[2] & 0x80) != 0)  # green
            button_state[1]["orange"] = ((data[3] & 0x01) != 0)  # orange
            button_state[1]["blue"] = ((data[3] & 0x02) != 0)  # blue

            button_state[2]["red"] = ((data[3] & 0x04) != 0)  # red
            button_state[2]["yellow"] = ((data[3] & 0x08) != 0)  # yellow
            button_state[2]["green"] = ((data[3] & 0x10) != 0)  # green
            button_state[2]["orange"] = ((data[3] & 0x20) != 0)  # orange
            button_state[2]["blue"] = ((data[3] & 0x40) != 0)  # blue

            button_state[3]["red"] = ((data[3] & 0x80) != 0)  # red
            button_state[3]["yellow"] = ((data[4] & 0x01) != 0)  # yellow
            button_state[3]["green"] = ((data[4] & 0x02) != 0)  # green
            button_state[3]["orange"] = ((data[4] & 0x04) != 0)  # orange
            button_state[3]["blue"] = ((data[4] & 0x08) != 0)  # blue
        return button_state

    def get_button_pressed(self, controller):
        buttons = self.get_button_status()
        for key, value in buttons[controller].items():
            if value:
                return key

    def controller_get_first_pressed(self, buzz_button, controllers=None):
        if controllers is None:
            controllers = [0, 1, 2, 3]
        while True:
            buttons = self.get_button_status()
            for i in controllers:
                if buttons[i][buzz_button]:
                    return i

    def read_and_print(self):
        d = self.hid.read(5, 1)
        if d:
            print(d)
