__author__ = "Konstantin Klaus"

from quiz.constants import *
import logging
import pygame


class Menu:

    def __init__(self, game):
        self.screen = pygame.display.get_surface()
        self.menu_running = True
        self.game = game
        self.logger = logging.getLogger("log")

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.game.end_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.end_game()
        elif event.type == pygame.USEREVENT:
            print(event.button)

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def run_menu(self):
        self.draw_main_menu()

        while self.menu_running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.game.end_game()

    def draw_main_menu(self):
        self.screen.fill(WHITE)

        (width, height) = self.screen.get_size()

        # Menu Buttons
        rec1 = pygame.Rect(0.3*width, 0.2*height, 0.4*width, 0.15*height)
        rec2 = pygame.Rect(0.3 * width, 0.4 * height, 0.4 * width, 0.15 * height)
        rec3 = pygame.Rect(0.3 * width, 0.6 * height, 0.4 * width, 0.15 * height)
        rec4 = pygame.Rect(0.3 * width, 0.8 * height, 0.4 * width, 0.15 * height)

        pygame.draw.rect(self.screen, BLUE, rec1)
        pygame.draw.rect(self.screen, ORANGE, rec2)
        pygame.draw.rect(self.screen, GREEN, rec3)
        pygame.draw.rect(self.screen, YELLOW, rec4)

        # Button Text
        font = pygame.font.Font('freesansbold.ttf', int(0.075*height))

        text1 = font.render("Spiel Starten", True, BLACK)
        text2 = font.render("Frage", True, BLACK)
        text3 = font.render("Einstellungen", True, BLACK)
        text4 = font.render("Beenden", True, BLACK)

        self.screen.blit(text1, (0.5*width - text1.get_width() // 2, 0.275*height - text1.get_height() // 2))
        self.screen.blit(text2, (0.5 * width - text2.get_width() // 2, 0.475 * height - text2.get_height() // 2))
        self.screen.blit(text3, (0.5 * width - text3.get_width() // 2, 0.675 * height - text3.get_height() // 2))
        self.screen.blit(text4, (0.5 * width - text4.get_width() // 2, 0.875 * height - text4.get_height() // 2))

        pygame.display.update()
