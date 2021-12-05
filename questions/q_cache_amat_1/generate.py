from moodle_helper import *
from typing import Any, List, Dict
from datetime import datetime


class MyQuestion(QuestionWrapper):
    # edit these parameters
    author: str = "Canberk Sonmez"
    name: str = "Caches: Average Memory Access Time - 1"
    difficulty: int = 1
    created: datetime = datetime(2021, 9, 8)  # year, month, day, ...
    tags = ["cache", "amat", "cache-amat-q1"]
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

        q = NumericalQuestion(__file__)
        q.name = self.name
        q.tags.extend(self.tags)

        # edit below
        q.text = """
        Consider a processor with the following cache hierarchy:
        <br/>
        <ul>
            <li>
            1-cycle L1 cache has a hit rate of {{ q.l1_hr }}.
            </li>

            <li>
            {{ q.l2_lat }}-cycle L2 cache has a hit rate of {{ q.l2_hr }}
            </li>

            <li>
            Main memory has a {{ q.mm_lat }}-cycle latency.
            </li>
        </ul>
        <br/>
        What is the average memory access time (AMAT) for this processor?

        <table>
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">First</th>
      <th scope="col">Last</th>
      <th scope="col">Handle</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>Mark</td>
      <td>Otto</td>
      <td>@mdo</td>
    </tr>
    <tr>
      <th scope="row">2</th>
      <td>Jacob</td>
      <td>Thornton</td>
      <td>@fat</td>
    </tr>
    <tr>
      <th scope="row">3</th>
      <td>Larry</td>
      <td>the Bird</td>
      <td>@twitter</td>
    </tr>
  </tbody>
</table>
        """
        # Some quick tips for formatting the question text and answers:
        #
        #  - Import an image: {{ r.image("epfl.png", style="width: 30%;") }}
        #  - Bold text: <strong>text...</strong>
        #  - Italic text: <em>text...</em>
        #  - Linebreak: <br/>
        #  - Latex equation within text: \( latex \)
        #  - Latex equation: $$ latex $$
        #  - Make sure that sequences {{ and }} do not occur in Latex equations.
        #    These sequences interfere with jinja2 template generator.

        # usage: q.add_answer(ans, tolerance, "feedback")
        q.add_answer("{{ q.ans }}", 0.001, "")

        # you can also add different units. please check the test question q4.

        q.generalfeedback = ""
        q.penalty = 1  # penalty in case of wrong answer
        q.defaultgrade = 2  # default grade that this question has

        return q

    def parameters_list(self) -> List[Dict[str, Any]]:
        """
        Returns parameters to instantiate the question.
        """

        # parameters are a set of values that substitute the variables
        # in the question text.
        l = []

        def add(l1_hr, l2_hr, l2_lat, mm_lat):
            ans = 1 + (1 - l1_hr) * (l2_lat + (1 - l2_hr) * mm_lat)
            l.append({
                "l1_hr": l1_hr,
                "l2_hr": l2_hr,
                "l2_lat": l2_lat,
                "mm_lat": mm_lat,
                "ans": ans
            })

        add(0.80, 0.90, 5, 100)
        add(0.85, 0.70, 6, 110)
        add(0.90, 0.75, 7, 120)
        add(0.95, 0.40, 8, 130)
        add(0.99, 0.10, 9, 140)

        return l


def generate() -> List[QuestionWrapper]:
    return [MyQuestion()]


if __name__ == "__main__":
    default_main(generate())
