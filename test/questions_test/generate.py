from typing import List
from moodle_helper import *


def generate_questions() -> List[QuestionBase]:
    q1 = MultipleChoiceQuestion()
    q1.add_param("thingy", "logo")
    q1.name = "Test Question #1"
    q1.text = """
To which school does the following {{ q.thingy }} belong?
<br />
{{ q.image("epfl.png", style="width: 10%;") }} <!-- simple html -->
    """
    q1.add_answer("ETH Zurich", 0)
    q1.add_answer("EPFL", 100)
    q1.add_answer("CMU", 0)
    q1.add_answer("Politecnico Milano", 0)
    q1.add_answer("None of the above", 0)
    q1.tags.extend(["test", "epfl"])

    q2 = TrueFalseQuestion()
    q2.name = "Test Question #2"
    q2.text = "EPFL is not the best school in the world."
    q2.add_trueans("Wrong answer, EPFL is the best school.")
    # q2.add_falseans("You are correct!")
    q2.add_falseans(SimpleLayout([0.5, 0.5]).text(
        "canberk").next_cell().text("a").next_cell().text("b"))
    q2.mark_correct(False)
    q2.tags.extend(["test", "epfl"])

    q3 = ShortAnswerQuestion()
    q3.name = "Test Question #3"
    q3.text = "What is the abbreviation of this institution?"
    q3.add_answer("EPFL", "This is the French one.")
    q3.add_answer("ETHL", "This is the German one.")
    q3.tags.extend(["test", "epfl"])

    q4 = NumericalQuestion()
    q4.name = "Test Question #4"
    q4.text = "Do the following calculation: 5 mW * 2 ns"
    q4.add_answer(10, 0.1)
    q4.add_unit(1, "pJ")
    q4.add_unit(1000, "fJ")  # 1 fJ = 1000 pJ
    q4.show_units()
    q4.tags.extend(["test", "physics"])

    q5 = NumericalQuestion()
    q5.name = "Test Question #5"
    layout = SimpleLayout([0.3, 0.3, 0.3, .1])
    layout.text("This question has an answer of 1. Let's see if layout works")
    layout.next_cell()
    layout.text("Section A")
    layout.image("epfl.png")
    layout.next_cell()
    layout.text("Section B")
    layout.image("epfl.png")
    layout.next_cell()
    layout.text("Section C")
    layout.image("epfl.png")
    layout.done()
    q5.text = layout
    q5.add_answer(1, 0)
    q5.tags.extend(["test", "epfl"])

    return [q1, q2, q3, q4, q5]
