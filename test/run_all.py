from moodle_helper import *
from typing import *
import os

if __name__ == "__main__":
    package_names = filter(os.path.isdir, os.listdir(os.curdir))
    print("<?xml version=\"1.0\" ?>\n<quiz>")
    for package_name in package_names:
        m = __import__(f"{ package_name }.generate", fromlist=[None])
        questions: List[QuestionBase] = getattr(m, "generate_questions")()
        for question in questions:
            question.res_dir = f"./" + package_name
            print(question.render())
    print("</quiz>")

# please take a look at the foll
# https://stackoverflow.com/a/37308413
