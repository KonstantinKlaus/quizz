import random


class Question:

    def __init__(self, question_dic: dict):
        self.question_en = question_dic["question"]
        self.question_de = question_dic["question_de"]
        self.wrong_answers = question_dic["incorrect_answers"]
        self.correct_answer = question_dic["correct_answer"]

        # shuffle
        self.possible_answers = self.wrong_answers.copy()
        self.possible_answers.append(self.correct_answer)
        random.shuffle(self.possible_answers)

    def get_possible_answers_shuffeled(self):
        return self.possible_answers

    def check(self, answer):
        if type(answer) == int:
            if self.possible_answers[answer] == self.correct_answer:
                return True
            else:
                return False
        else:
            if answer == self.correct_answer:
                return True
            else:
                return False


example_question = {"question": "Da?", "question_de": "Na?", "correct_answer": "Da!",
                    "incorrect_answers": ["Wa", "Ra", "La"]}
question = Question(example_question)
answers = question.get_possible_answers_shuffeled()
print(answers)