import random


class Question:

    def __init__(self, question_dic: dict):
        self.question_en = question_dic["question"]
        self.question_de = question_dic["question_de"]
        self.wrong_answers = question_dic["incorrect_answers"]
        self.correct_answer = question_dic["correct_answer"]

        # shuffle
        self.possible_answers = list(self.wrong_answers.copy())
        self.possible_answers.append(self.correct_answer)
        random.shuffle(self.possible_answers)

    """
    get possible answers, they are shuffled
    """
    def get_possible_answers(self) -> [str]:
        return self.possible_answers

    def index_correct_answer(self) -> [str]:
        return self.possible_answers.index(self.correct_answer)

    def check(self, answer) -> bool:
        if type(answer) is int:
            if self.possible_answers[answer] == self.correct_answer:
                return True
            else:
                return False
        else:
            if answer == self.correct_answer:
                return True
            else:
                return False
