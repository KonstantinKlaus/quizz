__author__ = "Konstantin Klaus"

from game.constants import *
from gamemodes.game_mode import *


class ClassicGame(GameMode):

    ANSWER_TIME = 15
    seconds_left = ANSWER_TIME

    player_answers = [None, None, None, None]
    player_points = [0, 0, 0, 0]

    def __init__(self, game):
        super().__init__(game)
        self.questions = self.game.question_db.get_questions(10)

    def run_game(self):
        self.game_running = True
        pygame.time.set_timer(TIME_EVENT, 1000)
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

        # font
        font = pygame.font.Font('freesansbold.ttf', int(0.075 * height))

        # render answer
        if self.game.language == DE:
            question = self.current_question().question_de
        else:
            question = self.current_question().question_en

        # check if answer is too long for one line
        if len(question) > 40:
            # two lines
            part_1 = question[0:40]
            part_2 = question[41:]
            part_1_rendered = font.render(part_1, True, BLACK)
            part_2_rendered = font.render(part_2, True, BLACK)

            self.screen.blit(part_1_rendered, (0.5 * width - part_1_rendered.get_width() // 2,
                                               0.08 * height - part_1_rendered.get_height() // 2))

            self.screen.blit(part_2_rendered, (0.5 * width - part_2_rendered.get_width() // 2,
                                               0.14 * height - part_2_rendered.get_height() // 2))

        else:
            # one line
            answer_rendered = font.render(question, True, BLACK)

            self.screen.blit(answer_rendered, (0.5 * width - answer_rendered.get_width() // 2,
                                               0.1 * height - answer_rendered.get_height() // 2))

        # possible answers
        answers = self.current_question().possible_answers

        if self.show_correct_answer:
            index = self.current_question().index_correct_answer()
            text = font.render(answers[index], True, BLACK)

            rec = pygame.Rect(0.1 * width, (0.2 + index * 0.2) * height, 0.8 * width, 0.15 * height)

            pygame.draw.rect(self.screen, get_color_by_index(index), rec)

            self.screen.blit(text, (0.5 * width - text.get_width() // 2,
                                    (0.275 + index * 0.2) * height - text.get_height() // 2))

        else:

            # Answer Buttons
            rec1 = pygame.Rect(0.1 * width, 0.2 * height, 0.8 * width, 0.15 * height)
            rec2 = pygame.Rect(0.1 * width, 0.4 * height, 0.8 * width, 0.15 * height)
            rec3 = pygame.Rect(0.1 * width, 0.6 * height, 0.8 * width, 0.15 * height)
            rec4 = pygame.Rect(0.1 * width, 0.8 * height, 0.8 * width, 0.15 * height)

            pygame.draw.rect(self.screen, BLUE, rec1)
            pygame.draw.rect(self.screen, ORANGE, rec2)
            pygame.draw.rect(self.screen, GREEN, rec3)
            pygame.draw.rect(self.screen, YELLOW, rec4)

            text1 = font.render(answers[0], True, BLACK)
            text2 = font.render(answers[1], True, BLACK)
            text3 = font.render(answers[2], True, BLACK)
            text4 = font.render(answers[3], True, BLACK)

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
        elif event.type == BUZZEVENT:
            # if correct answer is displayed
            if self.show_correct_answer:
                if event.button == "red":
                    # stop blinking
                    self.game.controller.controller_lights_off()

                    # if now questions are left -> end game mode
                    if self.number_questions_left() == 0:
                        # end game mode
                        self.game_running = False
                    else:
                        # next question
                        self.next_question()
                        self.player_answers = [None, None, None, None]
                        self.show_correct_answer = False
                        self.seconds_left = self.ANSWER_TIME
            # else
            else:
                if event.button != "red":
                    controller = event.controller
                    button = button_value(event.button)
                    self.player_answers[controller] = button

        elif event.type == TIME_EVENT:
            self.seconds_left -= 1

            # if counter for next event is 0
            if self.seconds_left == 0:
                # show correct answers
                self.show_correct_answer = True

                # buttons blinking
                self.game.controller.controller_lights_blink()

                # give points to players

