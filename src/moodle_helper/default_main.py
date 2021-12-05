from typing import List
from .quiz_builder import QuestionWrapper, QuizBuilder

def default_main(*args: List[List[QuestionWrapper]]):
    qb = QuizBuilder("preview")
    qb.begin()

    for qw in args:
        qb.add(qw)

    qb.end()

    qb.output_html_preview("preview.html")
