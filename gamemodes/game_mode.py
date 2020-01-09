class GameMode:

    questions = []

    position = 0

    game_running = False

    def __init__(self, game, question_db):
        self.game = game
        self.question_db = question_db

    def get_current_question(self):
        return self.questions[self.position]

    def next_question(self):
        if len(self.questions)==self.position:
            pass
        else:
            self.position = self.position + 1

    def get_next_question(self):
        if not len(self.questions)==self.position:
            self.position = self.position + 1

        return self.questions[self.position]

    def get_number_questions_left(self):
        return len(self.questions) - self.position
