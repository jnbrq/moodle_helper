from .base import *

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

    @template
    def rest(self):
        if self.trueans is None or self.falseans is None:
            raise ValueError("true and/or false answers not present")
        return """
<answer fraction="{{ 100 if q.correctone else 0 }}">
    <text>
    <![CDATA[
        {{ q.render_fragment(q.trueans[0]) }}
    ]]>
    </text>
    <feedback>
        <text>
        <![CDATA[
            {{ q.render_fragment(q.trueans[1]) }}
        ]]>
        </text>
    </feedback>
</answer>
<answer fraction="{{ 0 if q.correctone else 100 }}">
    <text>
    <![CDATA[
        {{ q.render_fragment(q.falseans[0]) }}
    ]]>
    </text>
    <feedback>
        <text>
        <![CDATA[
            {{ q.render_fragment(q.falseans[1]) }}
        ]]>
        </text>
    </feedback>
</answer>
        """
