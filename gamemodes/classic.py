__author__ = "Konstantin Klaus"

import pygame
from gamemodes.game_mode import GameMode
from game.constants import *


class ClassicGame(GameMode):

    def load_questions(self):
        self.questions = self.question_db.get_questions(10)

    def run_game(self):
        self.game_running = True
        while self.game_running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(30)

    def on_loop(self):
        pass

    def on_render(self):
        self.screen.fill(WHITE)

        (width, height) = self.screen.get_size()

        # Menu Buttons
        rec1 = pygame.Rect(0.1 * width, 0.2 * height, 0.8 * width, 0.15 * height)
        rec2 = pygame.Rect(0.1 * width, 0.4 * height, 0.8 * width, 0.15 * height)
        rec3 = pygame.Rect(0.1 * width, 0.6 * height, 0.8 * width, 0.15 * height)
        rec4 = pygame.Rect(0.1 * width, 0.8 * height, 0.8 * width, 0.15 * height)

        pygame.draw.rect(self.screen, BLUE, rec1)
        pygame.draw.rect(self.screen, ORANGE, rec2)
        pygame.draw.rect(self.screen, GREEN, rec3)
        pygame.draw.rect(self.screen, YELLOW, rec4)

        # Button Text
        font = pygame.font.Font('freesansbold.ttf', int(0.075 * height))

        answers = self.current_question().possible_answers
        if self.game.language == DE:
            text0 = font.render(self.current_question().question_de, True, BLACK)
        else:
            text0 = font.render(self.current_question().question_en, True, BLACK)
        text1 = font.render(answers[0], True, BLACK)
        text2 = font.render(answers[1], True, BLACK)
        text3 = font.render(answers[2], True, BLACK)
        text4 = font.render(answers[3], True, BLACK)

        self.screen.blit(text0, (0.5 * width - text1.get_width() // 2, 0.1 * height - text1.get_height() // 2))
        self.screen.blit(text1, (0.5 * width - text1.get_width() // 2, 0.275 * height - text1.get_height() // 2))
        self.screen.blit(text2, (0.5 * width - text2.get_width() // 2, 0.475 * height - text2.get_height() // 2))
        self.screen.blit(text3, (0.5 * width - text3.get_width() // 2, 0.675 * height - text3.get_height() // 2))
        self.screen.blit(text4, (0.5 * width - text4.get_width() // 2, 0.875 * height - text4.get_height() // 2))

        pygame.display.update()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.game.end_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.end_game()
