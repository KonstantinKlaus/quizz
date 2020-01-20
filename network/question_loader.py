__author__ = "Konstantin Klaus"

import html
import json
import logging
import urllib.request

logger = logging.getLogger("log")
base_url = "https://opentdb.com/api.php?"

GENERAL_KNOWLEDGE = 9
ENTERTAINMENT_BOOKS = 10
ENTERTAINMENT_FILM = 11
ENTERTAINMENT_MUSIC = 12
ENTERTAINMENT_MUSICALS_THEATRES = 13
ENTERTAINMENT_TELEVISION = 14
ENTERTAINMENT_VIDEO_GAMES = 15
ENTERTAINMENT_BOARD_GAMES = 16
SCIENCE_NATURE = 17
SCIENCE_COMPUTERS = 18
SCIENCE_MATHEMATICS = 19
MYTHOLOGY = 20
SPORTS = 21
GEOGRAPHY = 22
HISTORY = 23
POLITICS = 24
ART = 25
CELEBRITIES = 26
ANIMALS = 27
VEHICLES = 28
ENTERTAINMENT_COMICS = 29
SCIENCE_GADGETS = 30,
ENTERTAINMENT_JAPANESE_ANIME_MANGA = 31
ENTERTAINMENT_CARTOON_ANIMATIONS = 32


def cut_question_number(category, number):
    if category == 30:
        if number > 15:
            number = 15

    elif category == 29:
        if number > 35:
            number = 35

    elif category == 27:
        if number > 35:
            number = 35

    elif category == 26:
        if number > 40:
            number = 40

    elif category == 25:
        if number > 20:
            number = 20

    elif category == 24:
        if number > 30:
            number = 30

    elif category == 20:
        if number > 30:
            number = 30

    elif category == 19:
        if number > 20:
            number = 20

    elif category == 13:
        if number > 15:
            number = 15

    return number


def get_questions(difficulty="", category=0, number=10):
    number = cut_question_number(category, number)

    generated_url = "%samount=%d&category=%d&difficulty=%s&type=multiple" % (base_url, number, category, difficulty)
    with urllib.request.urlopen(generated_url) as url:
        string = url.read().decode('utf-8')
        data = json.loads(string)
        if data["response_code"] == 0:
            logger.info("Download successful, url: %s" % generated_url)
        else:
            logger.info("Download not successful, url: %s" % generated_url)

    return data["results"]
