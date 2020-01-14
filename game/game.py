import logging
import threading
import time

from controller.buzzcontroller import BuzzController
from game.constants import *
from questiondatabase.question_database import QuestionDatabase


class Game:
    # button states
    button_state_old = [{"red": False, "blue": False, "orange": False, "green": False, "yellow": False},
                        {"red": False, "blue": False, "orange": False, "green": False, "yellow": False},
                        {"red": False, "blue": False, "orange": False, "green": False, "yellow": False},
                        {"red": False, "blue": False, "orange": False, "green": False, "yellow": False}]

    question_db = QuestionDatabase()
    controller: BuzzController

    def __init__(self, controller: BuzzController, language=DE):
        # logger
        self.logger = logging.getLogger("log")

        self.game_is_running = True

        self.listener_thread = None
        self.language = language

        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("icons/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("minimal program")

        # create a surface on screen that has the size of 240 x 180
        self.screen = pygame.display.set_mode((900, 600), )

        self.controller = controller

    def set_language(self, language):
        if language not in [DE, EN]:
            self.language = EN
        else:
            self.language = language

    def screen(self):
        return self.screen()

    def end_game(self):
        # save new data
        if self.question_db.new_data:
            self.question_db.save_data()

        self.game_is_running = False
        self.controller.controller_lights_off()
        self.logger.info("End program")
        pygame.quit()
        quit()

    def start_buzz_listener(self):
        self.listener_thread = threading.Thread(target=self.listen_buzz,
                                                args=(),
                                                )
        self.listener_thread.start()

    def listen_buzz(self):
        self.logger.debug("start thread")
        while self.game_is_running:
            button_states = self.controller.get_button_status()
            if button_states is not None:
                for controller_id in range(0, 4):
                    for button in ["red", "blue", "orange", "green", "yellow"]:
                        # check if False -> True
                        if button_states[controller_id][button]:
                            # check if state has hanged
                            if button_states[controller_id][button] != self.button_state_old[controller_id][button]:
                                event = pygame.event.Event(BUZZEVENT, controller=controller_id, button=button)
                                pygame.event.post(event)

                self.button_state_old = button_states
            time.sleep(0.05)
