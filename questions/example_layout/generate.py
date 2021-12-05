from moodle_helper import *
from typing import Any, List, Dict
from datetime import datetime


class MyQuestion(QuestionWrapper):
    # edit these parameters
    author: str = "John Doe"
    name: str = "Test: Example Layout"
    difficulty: int = 1
    created: datetime = datetime(2021, 9, 5)  # year, month, day, ...
    tags = ["moodle_quizzer_test"]
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

        q = ShortAnswerQuestion(__file__)
        q.name = self.name
        q.tags.extend(self.tags)

        # edit below
        layout = SimpleLayout([
            0.3, 0.3, 0.3, 0.1  # we have 4 columns of these proportions
        ])
        layout.text("A")
        layout.next_cell()  # now, first cell
        layout.text("B")
        layout.image(filepath="C.png", width="90%")
        layout.next_cell()
        layout.text("D")
        layout.text("E")  # subsequent texts result in linebreaks
        layout.next_cell()
        layout.text("F")
        layout.next_cell()
        layout.text("G")
        layout.next_cell()
        layout.text("H")
        layout.done()
        # Resulting layout:
        #
        # +---------------+
        # |       A       |
        # +---+---+---+---+
        # | B | D | F | G |
        # | C | E |   |   |
        # +---+---+---+---+
        # | H |   |   |   |
        # +---+---+---+---+
        q.text = layout

        q.add_answer("alternative answer one", "feedback when typed")
        q.add_answer("alternative answer two", "feedback when typed")

        q.generalfeedback = "general feedback"
        q.penalty = 0.3  # penalty in case of wrong answer
        q.defaultgrade = 4  # default grade that this question has

        return q

    def parameters_list(self) -> List[Dict[str, Any]]:
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
    default_main(generate())
