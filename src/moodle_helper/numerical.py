from .base import *


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

    @template
    def rest(self):
        if self.answer is None:
            raise ValueError("answer is None")

        return """
<answer fraction="{{ q.answer[1] }}" format="moodle_auto_format">
    <text>
    <![CDATA[
        {{ q.answer[0] }}
    ]]>
    </text>
    <feedback>
        <text>
        <![CDATA[
            {{ q.answer[3] }}
        ]]>
        </text>
    </feedback>
    <tolerance>
        {{ q.answer[2] }}
    </tolerance>
</answer>
<units>
{% for multiplier, name in q.units %}
    <unit>
        <multiplier>{{ multiplier }}</multiplier>
        <unit_name>{{ name }}</unit_name>
    </unit>
{% endfor %}
</units>
<unitgradingtype>{{ q.unitgradingtype }}</unitgradingtype>
<unitpenalty>{{ q.unitpenalty }}</unitpenalty>
<showunits>{{ q.showunits }}</showunits>
<unitsleft>{{ q.unitsleft }}</unitsleft>
        """