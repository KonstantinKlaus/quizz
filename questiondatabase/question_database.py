import json
import random
from pathlib import Path
import logging

from questiondatabase.question_database import categories
from questionloader import question_loader

categories = {"General Knowledge":9, "Entertainment: Books":10, "Entertainment: Film":11,	"Entertainment: Music":12,
              "Entertainment: Musicals & Theatres":13, "Entertainment: Television":14, 	"Entertainment: Video Games":15,
              "Entertainment: Board Games":16, "Science & Nature":17, 	"Science: Computers":18,
              "Science: Mathematics":19, "Mythology":20, "Sports": 21, "Geography":22, "History":23, "Politics":24,
              "Art":25, "Celebrities":26, "Animals": 27, "Vehicles":28,	"Entertainment: Comics":29,
              "Science: Gadgets":30, "Entertainment: Japanese Anime & Manga":31, "Entertainment: Cartoon & Animations":32}


class QuestionDatabase:

    questions = {}


    max_id = 0

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

    def insert_question(self, question):
        self.max_id = self.max_id + 1
        self.questions[self.max_id] = question

    def insert_question_no_double(self, new_question):
        for question in self.questions.values():
            if new_question["question"] == question["question"]:
                logging.info("question already in database")
                return
        self.max_id = self.max_id + 1
        self.questions[self.max_id] = question
        logging.info("new question added to database with id " + str(self.max_id))

    def download_initial(self):
        for category_id in categories.values():
            new_questions = question_loader.get_questions(category=category_id, number=50)
            for new_question in new_questions.values():
                self.insert_question(new_question)

