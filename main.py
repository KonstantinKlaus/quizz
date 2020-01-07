import sched

from game.loading_screen import LoadingScreen
from questiondatabase.question_database import QuestionDatabase, prepare_question
from game.game import Game
from game.menu import Menu
from questionloader import question_loader
from translator import translator

__author__ = "Konstantin Klaus"

import logging
from controller import buzzcontroller
import time
import threading
from random import shuffle
import pygame


def main():
    # logger
    logger = logging.getLogger("log")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # connect to controller
    buzz = None
    game = Game(buzz)
    laoding_screen = LoadingScreen(game)
    laoding_screen.loading_screen()
    time.sleep(10)
    laoding_screen.exit()
    try:
        buzz = buzzcontroller.BuzzController()
    except AttributeError:
        logger.error("Error connecting to Buzz Controller")
        quit()

    logger.debug("start pygame")
    game = Game(buzz)
    laoding_screen = LoadingScreen(game)
    laoding_screen.loading_screen()
    game.question_db.load_data()
    laoding_screen.exit()
    game.start_buzz_listener()
    menu = Menu(game)
    menu.run_menu()


if __name__ == '__main__':
    main()
