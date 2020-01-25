__author__ = "Konstantin Klaus"

import pygame
import logging

from game.game import Game
from gamemodes.question import Question

QUESTION = 0
ANSWER = 1
SCORE = 2


def sort_score(score_list: list):
    # bubble sort
    for number in range(len(score_list) - 1, 0, -1):
        for i in range(number):
            if score_list[i][1] > score_list[i + 1][1]:
                temp = score_list[i]
                score_list[i] = score_list[i + 1]
                score_list[i + 1] = temp


class GameMode:

    game: Game =None

    questions = []
    position = 0

    game_running = False

    game_state = QUESTION

    def __init__(self, game):
        self.logger = logging.getLogger("log")
        self.game = game
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.get_surface()

    def current_question(self) -> Question:
        return self.questions[self.position]

    def next_question(self):
        if len(self.questions) == self.position:
            pass
        else:
            self.position = self.position + 1

    def get_next_question(self):
        if not len(self.questions) == self.position:
            self.position = self.position + 1

        return self.questions[self.position]

    def number_questions_left(self):
        return (len(self.questions) - 1) - self.position
