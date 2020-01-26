__author__ = "Konstantin Klaus"

from game.loading_screen import LoadingScreen
from gamemodes.buzz_mode import BuzzMode
from gamemodes.classic import ClassicGame
from game.constants import *
import logging
import pygame

LANGUAGE_SELECTION: int = 0
MAIN_MENU: int = 1
GAME_MODE_SELECTION: int = 2
OPTIONS: int = 3
QUESTIONS: int = 4

CLASSIC: int = 0
BUZZ: int = 1

MAX_GAME_MODE = 2


class Menu:
    strings = {
        EN: {"quit": "Quit", "options": "Options", "questions": "Questions", "start game": "Start Game",
             "game_mode_1": "Classic", "back": "Back",
             "loading_questions": "Rebasing Question Database ... please wait",
             "new_questions": "New Questions", "language_selection": "Language Selection",
             "check_connection": "Check Network Connection", CLASSIC: "Classic Mode",
             BUZZ: "Buzz Mode"},

        DE: {"quit": "Beenden", "options": "Optionen", "questions": "Fragen", "start game": "Spiel starten",
             "game_mode_1": "Klassisch", "back": "Zurück",
             "loading_questions": "Fragenkatalog wird neu erstellt... bitte warten",
             "new_questions": "Neue Fragen herunterladen", "language_selection": "Sprachauswahl",
             "check_connection": "Netzwerkverbindung prüfen", CLASSIC: "Klassischer Modus",
             BUZZ: "Buzz Modus"}}

    selected_game_mode = CLASSIC

    def __init__(self, game):
        self.screen = pygame.display.get_surface()
        self.menu_running = True
        self.game = game
        self.logger = logging.getLogger("log")
        self.menu = None
        self.clock = pygame.time.Clock()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.game.end_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.end_game()
            elif event.key == pygame.K_1:
                event = pygame.event.Event(BUZZEVENT, controller=0, button="red")
                pygame.event.post(event)
            elif event.key == pygame.K_2:
                event = pygame.event.Event(BUZZEVENT, controller=0, button="blue")
                pygame.event.post(event)
            elif event.key == pygame.K_3:
                event = pygame.event.Event(BUZZEVENT, controller=0, button="orange")
                pygame.event.post(event)
            elif event.key == pygame.K_4:
                event = pygame.event.Event(BUZZEVENT, controller=0, button="green")
                pygame.event.post(event)
            elif event.key == pygame.K_5:
                event = pygame.event.Event(BUZZEVENT, controller=0, button="yellow")
                pygame.event.post(event)

        # main menu
        elif self.menu == MAIN_MENU:
            if event.type == BUZZEVENT:
                if event.button == "yellow":
                    self.game.end_game()
                elif event.button == "blue":
                    self.menu = GAME_MODE_SELECTION
                elif event.button == "orange":
                    self.menu = QUESTIONS

        # language selection
        elif self.menu == LANGUAGE_SELECTION:
            if event.type == BUZZEVENT:
                if event.button == "blue":
                    self.game.set_language(DE)
                    self.menu = MAIN_MENU
                elif event.button == "orange":
                    self.game.set_language(EN)
                    self.menu = MAIN_MENU

        # game mode selection
        elif self.menu == GAME_MODE_SELECTION:
            if event.type == BUZZEVENT:
                if event.button == "yellow":
                    self.menu = MAIN_MENU
                elif event.button == "blue":
                    self.game_mode_up()
                elif event.button == "green":
                    self.game_mode_down()
                elif event.button == "red" or event.button == "orange":
                    # start classic game
                    self.start_game_mode()

        # question selection
        elif self.menu == QUESTIONS:
            if event.type == BUZZEVENT:
                if event.button == "yellow":
                    self.menu = MAIN_MENU
                elif event.button == "blue" and self.game.online:
                    # rebase question Database
                    loading_screen = LoadingScreen(self.game)
                    loading_screen.loading(self.game.question_db.download_initial, (),
                                           self.strings[self.game.language]["loading_questions"])

        # options menu
        elif self.menu == OPTIONS:
            if event.type == BUZZEVENT:
                if event.button == "yellow":
                    self.menu = MAIN_MENU
                elif event.button == "blue":
                    # check connection
                    loading_screen = LoadingScreen(self.game)
                    loading_screen.loading(self.game.check_online_state, ())

    def on_loop(self):
        pass

    def on_render(self):
        if self.menu == LANGUAGE_SELECTION:
            self.draw_language_selection()
        elif self.menu == GAME_MODE_SELECTION:
            self.draw_game_mode_selection()
        elif self.menu == QUESTIONS:
            self.draw_question_menu()
        elif self.menu == OPTIONS:
            self.draw_option_menu()
        else:
            self.draw_main_menu()

    def run_menu(self):
        self.menu = LANGUAGE_SELECTION

        while self.menu_running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(30)
        self.game.end_game()

    def draw_main_menu(self):
        self.screen.fill(WHITE)

        (width, height) = self.screen.get_size()

        # Menu Buttons
        rec1 = pygame.Rect(0.3 * width, 0.2 * height, 0.4 * width, 0.15 * height)
        rec2 = pygame.Rect(0.3 * width, 0.4 * height, 0.4 * width, 0.15 * height)
        rec3 = pygame.Rect(0.3 * width, 0.6 * height, 0.4 * width, 0.15 * height)
        rec4 = pygame.Rect(0.3 * width, 0.8 * height, 0.4 * width, 0.15 * height)

        pygame.draw.rect(self.screen, BLUE, rec1)
        pygame.draw.rect(self.screen, ORANGE, rec2)
        pygame.draw.rect(self.screen, GREEN, rec3)
        pygame.draw.rect(self.screen, YELLOW, rec4)

        # Button Text
        font = pygame.font.Font('freesansbold.ttf', int(0.075 * height))

        text1 = font.render(self.strings[self.game.language]["start game"], True, BLACK)
        text2 = font.render(self.strings[self.game.language]["questions"], True, BLACK)
        text3 = font.render(self.strings[self.game.language]["options"], True, BLACK)
        text4 = font.render(self.strings[self.game.language]["quit"], True, BLACK)

        self.screen.blit(text1, (0.5 * width - text1.get_width() // 2, 0.275 * height - text1.get_height() // 2))
        self.screen.blit(text2, (0.5 * width - text2.get_width() // 2, 0.475 * height - text2.get_height() // 2))
        self.screen.blit(text3, (0.5 * width - text3.get_width() // 2, 0.675 * height - text3.get_height() // 2))
        self.screen.blit(text4, (0.5 * width - text4.get_width() // 2, 0.875 * height - text4.get_height() // 2))

        pygame.display.update()

    def draw_question_menu(self):
        self.screen.fill(WHITE)

        (width, height) = self.screen.get_size()

        # Menu Buttons
        rec1 = pygame.Rect(0.3 * width, 0.2 * height, 0.4 * width, 0.15 * height)
        rec2 = pygame.Rect(0.3 * width, 0.4 * height, 0.4 * width, 0.15 * height)
        rec4 = pygame.Rect(0.3 * width, 0.8 * height, 0.4 * width, 0.15 * height)

        if self.game.online:
            pygame.draw.rect(self.screen, BLUE, rec1)
            pygame.draw.rect(self.screen, ORANGE, rec2)
        else:
            pygame.draw.rect(self.screen, GREY, rec1)
            pygame.draw.rect(self.screen, ORANGE, rec2)

        pygame.draw.rect(self.screen, YELLOW, rec4)

        # Button Text
        font = pygame.font.Font('freesansbold.ttf', int(0.075 * height))

        text1 = font.render("Rebase Questions", True, BLACK)
        text2 = font.render(self.strings[self.game.language]["new_questions"], True, BLACK)

        text4 = font.render(self.strings[self.game.language]["back"], True, BLACK)

        self.screen.blit(text1, (0.5 * width - text1.get_width() // 2, 0.275 * height - text1.get_height() // 2))
        self.screen.blit(text2, (0.5 * width - text2.get_width() // 2, 0.475 * height - text2.get_height() // 2))
        self.screen.blit(text4, (0.5 * width - text4.get_width() // 2, 0.875 * height - text4.get_height() // 2))

        pygame.display.update()

    def draw_option_menu(self):
        self.screen.fill(WHITE)

        (width, height) = self.screen.get_size()

        # Menu Buttons
        rec1 = pygame.Rect(0.3 * width, 0.2 * height, 0.4 * width, 0.15 * height)
        rec2 = pygame.Rect(0.3 * width, 0.4 * height, 0.4 * width, 0.15 * height)
        rec4 = pygame.Rect(0.3 * width, 0.8 * height, 0.4 * width, 0.15 * height)

        pygame.draw.rect(self.screen, BLUE, rec1)
        pygame.draw.rect(self.screen, ORANGE, rec2)

        pygame.draw.rect(self.screen, YELLOW, rec4)

        # Button Text
        font = pygame.font.Font('freesansbold.ttf', int(0.075 * height))

        text1 = font.render(self.strings[self.game.language]["check_connection"], True, BLACK)
        text2 = font.render(self.strings[self.game.language]["language_selection"], True, BLACK)

        text4 = font.render(self.strings[self.game.language]["back"], True, BLACK)

        self.screen.blit(text1, (0.5 * width - text1.get_width() // 2, 0.275 * height - text1.get_height() // 2))
        self.screen.blit(text2, (0.5 * width - text2.get_width() // 2, 0.475 * height - text2.get_height() // 2))
        self.screen.blit(text4, (0.5 * width - text4.get_width() // 2, 0.875 * height - text4.get_height() // 2))

        pygame.display.update()

    def draw_language_selection(self):
        self.screen.fill(WHITE)

        (width, height) = self.screen.get_size()

        # Menu Buttons
        rec1 = pygame.Rect(0.3 * width, 0.2 * height, 0.4 * width, 0.15 * height)
        rec2 = pygame.Rect(0.3 * width, 0.4 * height, 0.4 * width, 0.15 * height)

        pygame.draw.rect(self.screen, BLUE, rec1)
        pygame.draw.rect(self.screen, ORANGE, rec2)

        # Button Text
        font = pygame.font.Font('freesansbold.ttf', int(0.075 * height))

        text1 = font.render("Deutsch", True, BLACK)
        text2 = font.render("English", True, BLACK)

        self.screen.blit(text1, (0.5 * width - text1.get_width() // 2, 0.275 * height - text1.get_height() // 2))
        self.screen.blit(text2, (0.5 * width - text2.get_width() // 2, 0.475 * height - text2.get_height() // 2))

        pygame.display.update()

    def draw_game_mode_selection(self):
        self.screen.fill(WHITE)

        (width, height) = self.screen.get_size()

        # Menu Buttons
        rec2 = pygame.Rect(0.2 * width, 0.3125 * height, 0.6 * width, 0.125 * height)
        rec4 = pygame.Rect(0.3 * width, 0.825 * height, 0.4 * width, 0.1 * height)

        pygame.draw.polygon(self.screen, BLUE,
                            [(0.5 * width, 0.025 * height), (0.4 * width, 0.175 * height),
                             (0.6 * width, 0.175 * height)])
        pygame.draw.rect(self.screen, RED, rec2)
        pygame.draw.polygon(self.screen, ORANGE,
                            [(0.5 * width, 0.725 * height), (0.4 * width, 0.575 * height),
                             (0.6 * width, 0.575 * height)])
        pygame.draw.rect(self.screen, YELLOW, rec4)

        # Button Text
        font = pygame.font.Font('freesansbold.ttf', int(0.075 * height))

        text_game_mode = font.render(self.strings[self.game.language][self.selected_game_mode], True, BLACK)
        text_back = font.render(self.strings[self.game.language]["back"], True, BLACK)
        text_next_game_mode = \
            font.render(self.strings[self.game.language][(self.selected_game_mode + 1) % MAX_GAME_MODE], True,
                        DARK_GREY)
        text_last_next_game_mode = \
            font.render(self.strings[self.game.language][(self.selected_game_mode - 1) % MAX_GAME_MODE], True,
                        DARK_GREY)

        self.screen.blit(text_game_mode, (0.5 * width - text_game_mode.get_width() // 2,
                                          0.375 * height - text_game_mode.get_height() // 2))
        self.screen.blit(text_back, (0.5 * width - text_back.get_width() // 2,
                                     0.875 * height - text_back.get_height() // 2))
        self.screen.blit(text_next_game_mode, (0.5 * width - text_next_game_mode.get_width() // 2,
                                               0.25 * height - text_next_game_mode.get_height() // 2))
        self.screen.blit(text_last_next_game_mode, (0.5 * width - text_last_next_game_mode.get_width() // 2,
                                                    0.5 * height - text_last_next_game_mode.get_height() // 2))

        pygame.display.update()

    def game_mode_up(self):
        self.selected_game_mode = (self.selected_game_mode + 1) % MAX_GAME_MODE

    def game_mode_down(self):
        self.selected_game_mode = (self.selected_game_mode - 1) % MAX_GAME_MODE

    def start_game_mode(self):
        # start game mode
        if self.selected_game_mode == CLASSIC:
            game_mode = ClassicGame(self.game)
        else:
            game_mode = BuzzMode(self.game)
        game_mode.run_game()
