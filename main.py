__author__ = "Konstantin Klaus"

from game.game import Game
from game.loading_screen import LoadingScreen
from game.menu import Menu

__author__ = "Konstantin Klaus"

import logging
from controller import buzzcontroller
import time


def dumb_task(seconds):
    time.sleep(seconds)
    print("finished waiting")


def main():
    # logger
    logger = logging.getLogger("log")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # connect to controller
    buzz = None

    try:
        buzz = buzzcontroller.BuzzController()
    except AttributeError:
        logger.info("Error connecting to Buzz Controller, use keyboard instead")
        buzz = None
    logger.debug("start pygame")
    game = Game(buzz)
    loading_screen = LoadingScreen(game)
    loading_screen.start_task(game.check_online_state())
    game.question_db.load_data()
    game.start_buzz_listener()
    menu = Menu(game)
    menu.run_menu()


if __name__ == '__main__':
    main()
