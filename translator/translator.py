__author__ = "Konstantin Klaus"
import logging

from translate import Translator

logger = logging.getLogger("log")

translator = Translator(to_lang="de", from_lang="en")


def translate_question(question):
    a = 2


"""
translate a english sentence into a german sentence using google translate
"""


def translate(string):
    res = translator.translate(string)
    logger.info("Translated: %s" % res)
    return res
