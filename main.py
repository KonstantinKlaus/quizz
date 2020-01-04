import sched

from questiondatabase.question_database import QuestionDatabase
from game.game import Game
from game.menu import Menu

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

    q_dbase = QuestionDatabase()
    q_dbase.load_data()
    if q_dbase.new_data:
        q_dbase.save_data()

    # connect to controller
    try:
        buzz = buzzcontroller.BuzzController()
    except AttributeError:
        logger.error("Error connecting to Buzz Controller")
        quit()

    logger.debug("start pygame")
    game = Game(buzz)
    game.start_buzz_listener()
    menu = Menu(game)
    menu.run_menu()


if __name__ == '__main__':
    main()
