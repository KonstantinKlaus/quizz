import pygame


def end_game():
    pygame.quit()
    quit()


class Game:
    def __init__(self, language):
        self.language = language
