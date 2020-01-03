import logging
import pygame
from game.constants import *


class Quiz:
    strings = {
        EN: {"quit": "Quit", "options": "Options", "questions": "Questions", "start game": "Start Game",
             "game_mode_1": "Classic", "back": "Back"},
        DE: {"quit": "Beenden", "options": "Optionen", "questions": "Fragen", "start game": "Spiel starten",
             "game_mode_1": "Klassisch", "back": "Zurück"}}

    def __init__(self, game):
        self.screen = pygame.display.get_surface()
        self.quizz_running = True
        self.game = game
        self.logger = logging.getLogger("log")
        self.menu = None

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.game.end_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.end_game()


    def on_loop(self):
        pass

    def on_render(self):
        pass

    def run_quizz(self):
        self.draw_language_selection()

        while self.quizz_running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

    def draw_quiz_classic(self, question, answer1, answer2, answer3, answer4):
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

        text1 = font.render(answer1, True, BLACK)
        text2 = font.render(answer2, True, BLACK)
        text3 = font.render(answer3, True, BLACK)
        text4 = font.render(answer4, True, BLACK)

        self.screen.blit(text1, (0.5 * width - text1.get_width() // 2, 0.275 * height - text1.get_height() // 2))
        self.screen.blit(text2, (0.5 * width - text2.get_width() // 2, 0.475 * height - text2.get_height() // 2))
        self.screen.blit(text3, (0.5 * width - text3.get_width() // 2, 0.675 * height - text3.get_height() // 2))
        self.screen.blit(text4, (0.5 * width - text4.get_width() // 2, 0.875 * height - text4.get_height() // 2))

        pygame.display.update()