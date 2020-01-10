import pygame
import logging
from gamemodes.question import Question


class GameMode:
    questions = []
    position = 0

    game_running = False

    def __init__(self, game, question_db):
        self.logger = logging.getLogger("log")
        self.game = game
        self.question_db = question_db
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
        return len(self.questions) - self.position
