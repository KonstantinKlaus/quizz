__author__ = "Konstantin Klaus"
import logging
from googletrans import Translator

logger = logging.getLogger("log")

translator = Translator()

def translate_question(question):
    a=2

"""
translate a english sentence into a german sentence using google translate
"""
def translate(string):
    res = translator.translate(string,src="en",dest="de")
    logger.info(res)