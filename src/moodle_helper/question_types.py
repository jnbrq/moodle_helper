
class QuestionBase:
    def __init__(self):
        self.tags = []
        self.text = ""
        self.name = ""
        self.defaultgrade = 4
        self.generalfeedback = ""
        self.penalty = 0.3
        self.hidden = 0
        self.type = ""
        self.res_dir = "."

    def add_param(self, param, value):
        setattr(self, param, value)

    def add_params(self, **kwargs):
        for k, v in kwargs.items():
            self.add_param(k, v)


class NumericalQuestion(QuestionBase):
    def __init__(self):
        super().__init__()
        self.type = "numerical"
        self.answer = None
        self.units = []
        self.unitgradingtype = 0
        self.showunits = 0
        self.unitpenalty = 0.0
        self.unitsleft = 0

    def add_answer(self, x, tolerance, feedback=""):
        self.answer = (x, 100, tolerance, feedback)

    def add_unit(self, multiplier, name):
        self.units.append((multiplier, name))

    def grade_units(self, grade: bool = True):
        self.unitgradingtype = 1 if grade else 0

    def show_units(self, show: bool = True):
        self.showunits = 1 if show else 0

    def unit_penalty(self, penalty: float):
        self.unitpenalty = penalty

    def units_on_left(self, on_left: bool):
        self.unitsleft = 1 if on_left else 0


class MultipleChoiceQuestion(QuestionBase):
    def __init__(self):
        super().__init__()
        self.type = "multichoice"
        self.answers = []
        self.shuffleanswers = True
        self.single = True
        self.correctfeedback = ""
        self.partiallycorrectfeedback = ""
        self.incorrectfeedback = ""
        self.answernumbering = "none"

    def add_answer(self, text, fraction, feedback=""):
        self.answers.append((text, fraction, feedback))


class ShortAnswerQuestion(QuestionBase):
    def __init__(self):
        super().__init__()
        self.type = "shortanswer"
        self.answers = []

    def add_answer(self, text, feedback):
        self.answers.append((text, feedback))


class TrueFalseQuestion(QuestionBase):
    def __init__(self):
        super().__init__()
        self.trueans = None
        self.falseans = None
        self.correctone = True
        self.type = "truefalse"

    def add_trueans(self, feedback=""):
        self.trueans = ("true", feedback)

    def add_falseans(self, feedback=""):
        self.falseans = ("false", feedback)

    def mark_correct(self, correctone):
        self.correctone = correctone
