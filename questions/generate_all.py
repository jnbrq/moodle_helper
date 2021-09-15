from moodle_helper import *
from moodle_helper.quiz_builder import Chooser

def main() -> None:
    fname = "all-questions"
    tag = "all-questions"
    qb = QuizBuilder(tag)
    qb.fetch_questions()
    qb.output_moodle_xml(f"{fname}.xml", chooser=Chooser.all)
    qb.output_html_preview(f"{fname}.html", chooser=Chooser.random)


if __name__ == "__main__":
    main()
