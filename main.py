import sched

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

    question_db = QuestionDatabase()
    question_db.load_data()
    if question_db.new_data:
        question_db.save_data()

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
