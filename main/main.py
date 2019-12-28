from question_loader import question_loader
import logging

# logger
logger = logging.getLogger("log")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


question_loader.getQuestions()
