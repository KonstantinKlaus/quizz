__author__ = "Konstantin Klaus"
import logging

from translate import Translator

logger = logging.getLogger("log")

translator = Translator(provider="mymemory", to_lang="de", from_lang="en", email="buzzquiz@protonmail.com")


class ContingentException(Exception):
    """Base class for exceptions in this module."""
    pass


"""
translate a english sentence into a german sentence using mymemory translate
"""


def translate(string):
    res = translator.translate(string)
    if res == "MYMEMORY WARNING: YOU USED ALL AVAILABLE FREE TRANSLATIONS FOR TODAY. NEXT AVAILABLE IN  03 HOURS 51 " \
              "MINUTES 42 SECONDSVISIT HTTPS://MYMEMORY.TRANSLATED.NET/DOC/USAGELIMITS.PHP TO TRANSLATE MORE":
        raise ContingentException()
    logger.info("Translated: %s" % res)
    return res
