from moodle_helper import QuestionBase, ShortAnswerQuestion, QuestionWrapper
from typing import List, Dict
from datetime import datetime


class MyQuestion(QuestionWrapper):
    # edit these parameters
    author: str = "John Doe"
    name: str = "Test: Short Answer"
    difficulty: int = 1
    created: datetime = datetime(2021, 9, 5)  # year, month, day, ...
    tags = ["none"]
    skip = False

    def __init__(self) -> None:
        """
        Constructor.
        """
        pass  # pass is required for empty functions

    def question(self) -> QuestionBase:
        """
        Returns the base question.
        """

        q = ShortAnswerQuestion()
        q.name = self.name
        q.tags.extend(self.tags)

        # edit below
        q.text = """
        Question text here...
        </br>
        You can use HTML tags, such as <strong>bold</strong>.
        </br>
        You can use parameters: {{ q.school }} is amazing!
        </br>
        Parameters are also applicable in answers as well.
        """
        # Some quick tips for formatting the question text and answers:
        #
        #  - Import an image: {{ q.image("epfl.png", style="width: 30%;") }}
        #  - Bold text: <strong>text...</strong>
        #  - Italic text: <em>text...</em>
        #  - Linebreak: <br/>
        #  - Latex equation within text: \( latex \)
        #  - Latex equation: $$ latex $$
        #  - Make sure that sequences {{ and }} do not occur in Latex equations.
        #    These sequences interfere with jinja2 template generator.

        q.add_answer("alternative answer one", "feedback when typed")
        q.add_answer("alternative answer two", "feedback when typed")
        
        q.generalfeedback = "general feedback"
        q.penalty = 0.3 # penalty in case of wrong answer
        q.defaultgrade = 4 # default grade that this question has
        
        return q

    def parameters_list(self) -> List[Dict[str, object]]:
        """
        Returns parameters to instantiate the question.
        """

        # parameters are a set of values that substitute the variables
        # in the question text.
        l = []

        l.append({"school": "EPFL"})
        l.append({"school": "UNIL"})
        # the question is instantiated twice with q.school being replaced
        # by EPFL and UNIL.

        # you can add new sets of parameters

        return l


def generate() -> List[QuestionWrapper]:
    return [MyQuestion()]


if __name__ == "__main__":
    pass