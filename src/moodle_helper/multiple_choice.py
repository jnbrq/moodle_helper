from .base import *

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
    
    @template
    def rest(self):
        if not self.answernumbering in ["none", "abc", "ABCD", "123"]:
            raise ValueError("invalid answernumbering")
        
        return """
<shuffleanswers>{{ 1 if q.shuffleanswers else 0 }}</shuffleanswers>
<single>{{ "true" if q.single else "false" }}</single>
<correctfeedback format="html">
    <text>
    <![CDATA[
        {{ q.render_fragment(q.correctfeedback) }}
    ]]>
    </text>
</correctfeedback>
<partiallycorrectfeedback format="html">
    <text>
    <![CDATA[
        {{ q.render_fragment(q.partiallycorrectfeedback) }}
    ]]>
    </text>
</partiallycorrectfeedback>
<incorrectfeedback format="html">
    <text>
    <![CDATA[
        {{ q.render_fragment(q.incorrectfeedback) }}
    ]]>
    </text>
</incorrectfeedback>
<answernumbering>{{ q.answernumbering }}</answernumbering>
{% for answer, fraction, feedback in q.answers %}
<answer fraction="{{ fraction }}">
    <text>
    <![CDATA[
        {{ q.render_fragment(answer) }}
    ]]>
    </text>
    <feedback>
        <text>
        <![CDATA[
            {{ q.render_fragment(feedback) }}
        ]]>
        </text>
    </feedback>
</answer>
{% endfor %}
        """
