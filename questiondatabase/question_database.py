import json
import random
from pathlib import Path
import logging


class QuestionDatabase:
    questions = {}

    def __init__(self):
        self.logger = logging.getLogger("logger")

    def load_data(self):
        home_path = str(Path.home())
        self.logger.debug("home path:" + home_path)
        with open(home_path + "/buzzquiz/questions.json") as json_file:
            self.questions = json.load(json_file)
            self.logger.debug("file read successful")

    def save_data(self):
        home_path = str(Path.home())
        self.logger.debug("home path:" + home_path)

        # check if directory exists
        Path(home_path + "/buzzquiz").mkdir(parents=True, exist_ok=True)

        with open(home_path + "/buzzquiz/questions.json", "w+") as json_file:
            self.questions = json.dump(self.questions, json_file)
            self.logger.debug("file writing successful")

    def get_questions(self, number: 1, category: None):
        result = []
        if category is None:
            keys = list(self.questions.keys())
            for i in range(1, number):
                key, value = random.choice(keys)
                result.append(value)
                keys.remove(key)
        return result


