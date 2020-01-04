__author__ = "Konstantin Klaus"
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


def get_questions(difficulty="", category="", number=10):
    amount = "amount=" + str(number)
    generated_url = base_url + amount
    if category != "":
        generated_url = generated_url + "&" + "category=" + category

    if difficulty != "":
        generated_url = generated_url + "&" + "difficulty=" + difficulty

    with urllib.request.urlopen(generated_url) as url:
        data = json.loads(url.read().decode())
        logger.info("Downloaded:" + str(data) + "&type=multiple")

    return data
