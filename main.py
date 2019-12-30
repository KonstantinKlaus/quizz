__author__ = "Konstantin Klaus"

from controller.enumerate import print_usb
from translator import translator
from questionloader import question_loader
import logging
import controller.buzzcontroller
import time
import thread
from random import shuffle


def main():
    # logger
    logger = logging.getLogger("log")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    question_loader.getQuestions()

    translator.translate("Good morning!")

    print_usb()
if __name__ == '__main__':
    main()
