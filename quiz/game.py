import pygame
from quiz.constants import DE, EN


def end_game():
    pygame.quit()
    quit()


class Game:

    def __init__(self, language=DE):
        self.language = language

        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("icons/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("minimal program")

        # create a surface on screen that has the size of 240 x 180
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def screen(self):
        return self.screen()
