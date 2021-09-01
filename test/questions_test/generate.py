from typing import List
from moodle_helper import *

def tags() -> List[str]:
    return [ "test" ]

def generate_questions() -> List[QuestionBase]:
    q1 = MultipleChoiceQuestion()
    q1.add_param("thingy", "logo")
    q1.name = "Test Question #1"
    q1.text = """
To which school does the following {{ q.param("thingy") }} belong?
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
    q2.add_falseans("You are correct!")
    q2.mark_correct(False)
    q2.tags.extend(["test", "epfl"])

    q3 = ShortAnswerQuestion()
    q3.name = "Test Question #3"
    q3.text = "What is the abbreviation of this institution?"
    q3.add_answer("EPFL", "This is the French one.")
    q3.add_answer("ETHL", "This is the German one.")
    q3.tags.extend(["test", "epfl"])
    
    return [q1, q2, q3]
