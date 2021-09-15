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
    fname = "my-test-quiz"
    tag = "my-test-quiz"
    qb = QuizBuilder(tag)
    qb.fetch_questions(Filter())
    qb.shuffle_questions()
    qb.output_moodle_xml(f"{fname}.xml")
    qb.output_html_preview(f"{fname}.html")


if __name__ == "__main__":
    main()
