from .base import *


class ShortAnswerQuestion(QuestionBase):
    def __init__(self):
        super().__init__()
        self.type = "shortanswer"
        self.answers = []

    def add_answer(self, text, feedback):
        self.answers.append((text, feedback))

    @template
    def rest(self):
        return """
{% for answer, feedback in q.answers %}
<answer fraction="100">
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
