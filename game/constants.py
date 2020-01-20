import pygame

EN = 0
DE = 1

WHITE = (255, 255, 255)
BLUE = (0, 70, 161)
BLACK = (0, 0, 0)
ORANGE = (255, 128, 0)
GREEN = (0, 102, 0)
YELLOW = (255, 255, 0)
RED = (204, 0, 0)
GREY = (192, 192, 192)


def get_color_by_index(index: int):
    if index == 0:
        return BLUE
    elif index == 1:
        return ORANGE
    elif index == 2:
        return GREEN
    elif index == 3:
        return YELLOW
    else:
        return RED


BLUE_BUTTON = 0
ORANGE_BUTTON = 1
GREEN_BUTTON = 2
YELLOW_BUTTON = 3
RED_BUTTON = 5


def button_value(button: str) -> int:
    if button == "blue":
        return BLUE_BUTTON
    elif button == "orange":
        return ORANGE_BUTTON
    elif button == "green":
        return GREEN_BUTTON
    elif button == "yellow":
        return YELLOW_BUTTON
    else:
        return RED_BUTTON


# pygame user events
BUZZEVENT = pygame.USEREVENT + 1
TIME_EVENT = pygame.USEREVENT + 2
