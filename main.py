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
    game.question_db.load_data()
    game.start_buzz_listener()
    menu = Menu(game)
    menu.run_menu()


if __name__ == '__main__':
    main()
