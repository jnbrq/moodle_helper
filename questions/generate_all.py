from moodle_helper import *
from moodle_helper.quiz_builder import Chooser

def main() -> None:
    qb = QuizBuilder("my-test-quiz")
    qb.fetch_questions()
    qb.shuffle_questions()
    qb.write_xml_file("my-all-questions.xml", chooser=Chooser.all)


if __name__ == "__main__":
    main()
