from translator import translator

__author__ = "Konstantin Klaus"
from question_loader import question_loader
import logging

# logger
logger = logging.getLogger("log")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


question_loader.getQuestions()

translator.translate("Good morning!")