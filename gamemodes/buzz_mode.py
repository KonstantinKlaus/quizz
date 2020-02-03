__author__ = "Konstantin Klaus"

from builtins import range

from game.constants import *
from gamemodes.game_mode import *


class BuzzMode(GameMode):

    QUESTION_TIME = 10
    ANSWER_TIME = 5
    seconds_left = ANSWER_TIME

    player_points = [0, 0, 0, 0]
    player_answered = [False, False, False, False]

    answers_available = [True, True, True, True]

    score_list = []

    buzzed = False
    player_buzzed = 0

    def __init__(self, game):
        super().__init__(game)
        self.questions = self.game.question_db.get_questions(10)

    def run_game(self):
        self.game_running = True
        pygame.time.set_timer(TIME_EVENT, 1000)
        while self.game_running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
            self.clock.tick(30)

    def all_answered(self) -> bool:
        for answer in self.answers_available:
            if not answer:
                return True
        return False

    def on_render(self):
        if self.game_state == SCORE:
            self.draw_score()
        else:
            self.draw_game()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.game.end_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.end_game()

        # if question is showed
        elif self.game_state == QUESTION:
            # if nobody has buzzed yet
            if not self.buzzed:
                if event.type == BUZZEVENT:
                    if event.button == "red":
                        player_buzzed = event.controller
                        # if player has not buzzed yet
                        if not self.player_answered[player_buzzed]:
                            self.buzzed = True
                            self.player_buzzed = player_buzzed
                            # stop blinking, controller that buzzed lights on
                            self.game.controller.controller_lights_off()
                            self.game.controller.get_controller(player_buzzed).light_on()
                            # set timer
                            self.seconds_left = self.ANSWER_TIME
                            pygame.time.set_timer(TIME_EVENT, 1000)

                elif event.type == TIME_EVENT:
                    self.seconds_left -= 1
                    if self.seconds_left == 0:
                        self.seconds_left = self.QUESTION_TIME
                        self.game_state = QUESTION
                        self.game.controller.controller_lights_on()

            else:
                # button is pressed
                if event.type == BUZZEVENT:
                    if event.button != "red":
                        controller = event.controller
                        # if buzzed controller
                        if controller == self.player_buzzed:
                            button = button_value(event.button)
                            # check if correct answer was selected
                            if self.current_question().check(button):
                                self.player_points[controller] += 1
                                self.game_state = ANSWER
                                self.game.controller.controller_lights_on()

                            # if wrong answer
                            else:
                                self.player_answered[controller] = False
                                # if all player answered
                                if self.all_answered():
                                    self.game_state = ANSWER
                                    self.game.controller.controller_lights_on()
                                else:
                                    self.unbuzzed_controllers_blink()
                                    self.seconds_left = self.QUESTION_TIME

                                    # disable selected answer
                                    self.answers_available[button] = False

                # a second has passed
                elif event.type == TIME_EVENT:
                    self.seconds_left -= 1

                    # if counter for next event is 0
                    if self.seconds_left == 0:

                        # other players have chance to buzz
                        self.buzzed = False
                        self.player_answered[self.player_buzzed] = True

        # if answer is showed
        elif self.game_state == ANSWER:
            if event.type == BUZZEVENT:
                if event.button == "red":
                    # stop blinking
                    self.game.controller.controller_lights_off()

                    # if now questions are left -> end game mode
                    if self.number_questions_left() == 0:
                        # goto score
                        self.game_state = SCORE
                        self.game.controller.controller_lights_on()

                        # make score
                        for i in range(0, 4):
                            self.score_list.append((i, self.player_points[i]))

                        sort_score(self.score_list)
                    else:
                        # next question
                        self.next_question()
                        self.player_answered = [False, False, False, False]
                        self.answers_available = [True, True, True, True]
                        self.game_state = QUESTION
                        self.seconds_left = self.ANSWER_TIME

        # if score is showed
        elif self.game_state == SCORE:
            if event.type == BUZZEVENT:
                if event.button == "red":
                    # lights off and end game mode
                    self.game.controller.controller_lights_off()
                    self.game_running = False

    def draw_game(self):
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
            part_2 = question[40:]
            part_1_rendered = font.render(part_1, True, BLACK)
            part_2_rendered = font.render(part_2, True, BLACK)

            self.screen.blit(part_1_rendered, (0.5 * width - part_1_rendered.get_width() // 2,
                                               0.06 * height - part_1_rendered.get_height() // 2))

            self.screen.blit(part_2_rendered, (0.5 * width - part_2_rendered.get_width() // 2,
                                               0.16 * height - part_2_rendered.get_height() // 2))

        else:
            # one line
            answer_rendered = font.render(question, True, BLACK)

            self.screen.blit(answer_rendered, (0.5 * width - answer_rendered.get_width() // 2,
                                               0.1 * height - answer_rendered.get_height() // 2))

        # possible answers
        answers = self.current_question().possible_answers

        if self.game_state == ANSWER:
            index = self.current_question().index_correct_answer()
            text = font.render(answers[index], True, BLACK)

            rec = pygame.Rect(0.1 * width, (0.25 + index * 0.2) * height, 0.8 * width, 0.15 * height)

            pygame.draw.rect(self.screen, get_color_by_index(index), rec)

            self.screen.blit(text, (0.5 * width - text.get_width() // 2,
                                    (0.325 + index * 0.2) * height - text.get_height() // 2))

        else:

            # Answer Buttons
            rec1 = pygame.Rect(0.1 * width, 0.25 * height, 0.8 * width, 0.15 * height)
            rec2 = pygame.Rect(0.1 * width, 0.45 * height, 0.8 * width, 0.15 * height)
            rec3 = pygame.Rect(0.1 * width, 0.65 * height, 0.8 * width, 0.15 * height)
            rec4 = pygame.Rect(0.1 * width, 0.85 * height, 0.8 * width, 0.15 * height)

            text1 = font.render(answers[0], True, BLACK)
            text2 = font.render(answers[1], True, BLACK)
            text3 = font.render(answers[2], True, BLACK)
            text4 = font.render(answers[3], True, BLACK)

            if self.answers_available[0]:
                pygame.draw.rect(self.screen, BLUE, rec1)
                self.screen.blit(text1,
                                 (0.5 * width - text1.get_width() // 2, 0.325 * height - text1.get_height() // 2))

            if self.answers_available[1]:
                pygame.draw.rect(self.screen, ORANGE, rec2)
                self.screen.blit(text2,
                                 (0.5 * width - text2.get_width() // 2, 0.525 * height - text2.get_height() // 2))

            if self.answers_available[2]:
                pygame.draw.rect(self.screen, GREEN, rec3)
                self.screen.blit(text3,
                                 (0.5 * width - text3.get_width() // 2, 0.725 * height - text3.get_height() // 2))

            if self.answers_available[3]:
                pygame.draw.rect(self.screen, YELLOW, rec4)
                self.screen.blit(text4,
                                 (0.5 * width - text4.get_width() // 2, 0.925 * height - text4.get_height() // 2))

        pygame.display.update()

    def draw_score(self):
        self.screen.fill(WHITE)

        (width, height) = self.screen.get_size()

        # font
        font = pygame.font.Font('freesansbold.ttf', int(0.1 * height))

        score_text = []
        for i in range(0, 4):
            if self.game.language == DE:
                player_string = "Spieler"
            else:
                player_string = "Player"
            score_text.append("%u - %s %u" % (self.score_list[i][1], player_string, self.score_list[i][0]))

        for index in range(0, 4):
            text = font.render(score_text[index], True, BLACK)

            self.screen.blit(text, (0.5 * width - text.get_width() // 2, (0.2 + 0.2 * index) * height - text.get_height() // 2))

        pygame.display.update()

    def unbuzzed_controllers_blink(self):
        for i in range(0, 4):
            if not self.player_answered[i]:
                self.game.controller.get_controller(i).blink()