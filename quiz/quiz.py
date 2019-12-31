from quiz.constants import DE


class Quiz:

    def __init__(self, language: DE):
        self.language = language

    def change_language(self, language):
        self.language = language
