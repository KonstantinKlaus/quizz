import pygame
from quiz.constants import DE, EN


class Game:

    def __init__(self, controller, language=DE):
        self.language = language

        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("icons/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("minimal program")

        # create a surface on screen that has the size of 240 x 180
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.controller = controller

    def screen(self):
        return self.screen()

    def end_game(self):
        self.controller.controller_lights_off()
        pygame.quit()
        quit()
