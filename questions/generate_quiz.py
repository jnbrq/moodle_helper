from moodle_helper import *


class Filter:
    def __init__(self) -> None:
        """
        Constructor.
        """
        pass

    def __call__(self, qw: QuestionWrapper) -> bool:
        """
        Filtering function. Returns true if the question should
        be included.
        """
        # You can also check: qw.tags
        return qw.difficulty >= 1


def main() -> None:
    qb = QuizBuilder("my-test-quiz")
    qb.fetch_questions(Filter())
    qb.shuffle_questions()
    qb.write_xml_file("my-test-quiz.xml")


if __name__ == "__main__":
    main()
