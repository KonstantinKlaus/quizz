from quiz.game import Game
from quiz.menu import Menu

__author__ = "Konstantin Klaus"

import logging
from controller import buzzcontroller
import time
import threading
from random import shuffle
import pygame


def main():
    # logger
    logger = logging.getLogger("log")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # controller test
    buzz = buzzcontroller.BuzzController()
    controller = buzz.get_controller(0)
    controller.light_on()
    logger.debug("controller 1 light on")
    threading.Thread(target=buzz.read_and_print(),
                     ).start()
    logger.debug("thread running")
    game = Game()
    menu = Menu(game)
    menu.run_menu()


def easy_quiz():
    import_questions = [
        {"question": "What is the capital of Australia", "answers": ["Canberra", "Sydney", "Hobart", "Melbourne"]},
        {"question": "What is the capital of Japan", "answers": ["Tokyo", "Hiroshima", "Osaka", "Kyoto"]},
    ]
    questions = []
    score = [0, 0, 0, 0]

    for question in import_questions:
        buttons = ["blue", "orange", "green", "yellow"]
        new_answer = {}
        shuffle(buttons)
        new_answer['question'] = question['question']
        for i in range(4):
            if i == 0:
                new_answer["correct"] = buttons[i]
            new_answer[buttons[i]] = question["answers"][i]
        questions.append(new_answer)

    buzz = buzzcontroller.BuzzController()

    for question in questions:
        question_answered = False
        available_answers = ["Blue", "Orange", "Green", "Yellow"]
        available_controllers = [0, 1, 2, 3]

        while not question_answered:
            print(question["question"])

            for i in available_answers:
                print(i + " " + question[i.lower()])

            threading.Thread(target=buzz.light_blink,
                             args=(available_controllers,),
                             ).start()

            controller = buzz.controller_get_first_pressed("red", available_controllers)
            buzz.light_blinking = False
            buzz.light_set(controller, True)
            time.sleep(0.5)

            while True:
                button = buzz.get_button_pressed(controller)
                if button and button != "red":
                    if button == question["correct"]:
                        print("Controller " + str(controller) + " was correct")
                        question_answered = True
                        score[controller] += 1
                        break
                    elif button.capitalize() in available_answers:
                        print("Sorry incorrect answer")
                        available_controllers.remove(controller)
                        available_answers.remove(button.capitalize())
                        break
            buzz.light_set(controller, False)
        time.sleep(1)

    print("Final score")
    print(score)


if __name__ == '__main__':
    main()
