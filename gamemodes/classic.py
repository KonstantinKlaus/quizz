__author__ = "Konstantin Klaus"

from game.constants import *
from gamemodes.game_mode import *


def sort_score(score_list: list):
    # bubble sort
    for number in range(len(score_list) - 1, 0, -1):
        for i in range(number):
            if score_list[i][1] > score_list[i + 1][1]:
                temp = score_list[i]
                score_list[i] = score_list[i + 1]
                score_list[i + 1] = temp


class ClassicGame(GameMode):

    ANSWER_TIME = 15
    seconds_left = ANSWER_TIME

    player_answers = [None, None, None, None]
    player_points = [0, 0, 0, 0]

    score_list = []

    def __init__(self, game):
        super().__init__(game)
        self.questions = self.game.question_db.get_questions(10)

    def all_select(self):
        for selection in self.player_answers:
            if selection is not None:
                return False
        return True

    def run_game(self):
        self.game_running = True
        pygame.time.set_timer(TIME_EVENT, 1000)
        while self.game_running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
            self.clock.tick(30)

    def on_render(self):
        if self.game_state == SCORE:
            self.draw_score()
        else:
            self.draw_game()

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

            pygame.draw.rect(self.screen, BLUE, rec1)
            pygame.draw.rect(self.screen, ORANGE, rec2)
            pygame.draw.rect(self.screen, GREEN, rec3)
            pygame.draw.rect(self.screen, YELLOW, rec4)

            text1 = font.render(answers[0], True, BLACK)
            text2 = font.render(answers[1], True, BLACK)
            text3 = font.render(answers[2], True, BLACK)
            text4 = font.render(answers[3], True, BLACK)

            self.screen.blit(text1, (0.5 * width - text1.get_width() // 2, 0.325 * height - text1.get_height() // 2))
            self.screen.blit(text2, (0.5 * width - text2.get_width() // 2, 0.525 * height - text2.get_height() // 2))
            self.screen.blit(text3, (0.5 * width - text3.get_width() // 2, 0.725 * height - text3.get_height() // 2))
            self.screen.blit(text4, (0.5 * width - text4.get_width() // 2, 0.925 * height - text4.get_height() // 2))

        pygame.display.update()

    def draw_score(self):
        self.screen.fill(WHITE)

        (width, height) = self.screen.get_size()

        # font
        font = pygame.font.Font('freesansbold.ttf', int(0.1 * height))

        score_text = []
        for i in range(0, 3):
            if self.game.language == DE:
                player_string = "Spieler"
            else:
                player_string = "Player"
            score_text[i] = "%u - %s %u" % (self.score_list[i][1], player_string, self.score_list[i][0])

        for index in range(0, 3):
            text = font.render(score_text[index], True, BLACK)

            self.screen.blit(text, (0.5 * width - text.get_width() // 2, (0.2 + 0.2 * index) * height - text.get_height() // 2))

        pygame.display.update()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.game.end_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.end_game()

        # if question is showed
        elif self.game_state == QUESTION:
            # button is pressed
            if event.type == BUZZEVENT:
                if event.button != "red":
                    controller = event.controller
                    button = button_value(event.button)
                    self.player_answers[controller] = button

            # a second has passed
            elif event.type == TIME_EVENT:
                self.seconds_left -= 1

                # if counter for next event is 0
                if self.seconds_left == 0 or self.all_select():
                    # show correct answers
                    self.game_state = ANSWER

                    # buttons blinking
                    self.game.controller.controller_lights_blink()

                    # give points to players
                    index_correct_answer = self.current_question().index_correct_answer()

                    for player in range(0, 3):
                        if self.player_answers[player] == index_correct_answer:
                            self.player_points[player] = self.player_points[player] + 1

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
                        for i in range(0, 3):
                            self.score_list.append((i, self.player_points[i]))

                        sort_score(self.score_list)
                    else:
                        # next question
                        self.next_question()
                        self.player_answers = [None, None, None, None]
                        self.game_state = QUESTION
                        self.seconds_left = self.ANSWER_TIME

        # if score is showed
        elif self.game_state == SCORE:
            if event.type == BUZZEVENT:
                if event.button == "red":
                    # lights off and end game mode
                    self.game.controller.controller_lights_off()
                    self.game_running = False
