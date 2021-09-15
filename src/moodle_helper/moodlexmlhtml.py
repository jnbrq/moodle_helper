from .renderer_base import *
from .question_types import *
import os
from jinja2 import Template


class MoodleXMLHTMLRenderer(RendererBase):
    """
    Outputs in MoodleXML format, text parts are HTML.
    """

    def __init__(self, q: QuestionBase) -> None:
        super().__init__(q)

    @render_jinja
    def render_question(self) -> str:
        return """
<question type="{{ q.type }}">
    <name>
        <text>
        <![CDATA[
            {{ r.fragment(q.name) }}
        ]]>
        </text>
    </name>
    <questiontext format="html">
        <text>
        <![CDATA[
            {{ r.fragment(q.text) }}
        ]]>
        </text>
    </questiontext>
    <generalfeedback format="html">
        <text>
        <![CDATA[
            {{ r.fragment(q.generalfeedback) }}
        ]]>
        </text>
    </generalfeedback>
    <penalty>{{ q.penalty }}</penalty>
    <hidden>{{ 1 if q.hidden else 0 }}</hidden>
    {{ r._render_tags() }}
    {{ r._render_rest() }}
</question>
        """

    def jinja(self, t: str) -> str:
        template = Template(t)
        return template.render(q=self.q, r=self)

    def image(self, filepath: str, tag: str = "img", *args, **kwargs) -> str:
        with open(self.q.res_dir + "/" + filepath, "rb") as f:
            _, ext = os.path.splitext(filepath)
            kwargs["src"] = base64_embed(f, f"data:image/{ ext }")
        return Template(
            """
<{{ tag }} {% for k, v in attr.items() %} {{ k }}="{{ v }}" {% endfor %} />
""").render(tag=tag, filepath=filepath, attr=kwargs)

    @render_jinja
    def _render_tags(self) -> str:
        return """
<tags>
{% for tag in q.tags %}
    <tag>
        <text>
        <![CDATA[
            {{ r.fragment(tag) }}
        ]]>
        </text>
    </tag>
{% endfor %}
</tags>
"""

    @render_jinja
    def _render_rest(self) -> str:
        if isinstance(self.q, MultipleChoiceQuestion):
            return self._render_rest_multiplechoice()
        if isinstance(self.q, NumericalQuestion):
            return self._render_rest_numerical()
        if isinstance(self.q, ShortAnswerQuestion):
            return self._render_rest_shortanswer()
        if isinstance(self.q, TrueFalseQuestion):
            return self._render_rest_truefalse()
        raise NotImplementedError(
            "unknown question type for MoodleXMLHTMLRenderer")

    def _render_rest_multiplechoice(self) -> str:
        if not self.q.answernumbering in ["none", "abc", "ABCD", "123"]:
            raise ValueError("invalid answernumbering")

        return """
<shuffleanswers>{{ 1 if q.shuffleanswers else 0 }}</shuffleanswers>
<single>{{ "true" if q.single else "false" }}</single>
<correctfeedback format="html">
    <text>
    <![CDATA[
        {{ r.fragment(q.correctfeedback) }}
    ]]>
    </text>
</correctfeedback>
<partiallycorrectfeedback format="html">
    <text>
    <![CDATA[
        {{ r.fragment(q.partiallycorrectfeedback) }}
    ]]>
    </text>
</partiallycorrectfeedback>
<incorrectfeedback format="html">
    <text>
    <![CDATA[
        {{ r.fragment(q.incorrectfeedback) }}
    ]]>
    </text>
</incorrectfeedback>
<answernumbering>{{ q.answernumbering }}</answernumbering>
{% for answer, fraction, feedback in q.answers %}
<answer fraction="{{ fraction }}">
    <text>
    <![CDATA[
        {{ r.fragment(answer) }}
    ]]>
    </text>
    <feedback>
        <text>
        <![CDATA[
            {{ r.fragment(feedback) }}
        ]]>
        </text>
    </feedback>
</answer>
{% endfor %}
        """

    def _render_rest_numerical(self) -> str:
        return """
<answer fraction="{{ r.fragment(q.answer[1]) }}" format="moodle_auto_format">
    <text>
    <![CDATA[
        {{ r.fragment(q.answer[0]) }}
    ]]>
    </text>
    <feedback>
        <text>
        <![CDATA[
            {{ r.fragment(q.answer[3]) }}
        ]]>
        </text>
    </feedback>
    <tolerance>
        {{ r.fragment(q.answer[2]) }}
    </tolerance>
</answer>
<units>
{% for multiplier, name in q.units %}
    <unit>
        <multiplier>{{ r.fragment(multiplier) }}</multiplier>
        <unit_name>{{ r.fragment(name) }}</unit_name>
    </unit>
{% endfor %}
</units>
<unitgradingtype>{{ r.fragment(q.unitgradingtype) }}</unitgradingtype>
<unitpenalty>{{ r.fragment(q.unitpenalty) }}</unitpenalty>
<showunits>{{ r.fragment(q.showunits) }}</showunits>
<unitsleft>{{ r.fragment(q.unitsleft) }}</unitsleft>
        """

    def _render_rest_shortanswer(self) -> str:
        return """
{% for answer, feedback in q.answers %}
<answer fraction="100">
    <text>
    <![CDATA[
        {{ r.fragment(answer) }}
    ]]>
    </text>
    <feedback>
        <text>
        <![CDATA[
            {{ r.fragment(feedback) }}
        ]]>
        </text>
    </feedback>
</answer>
{% endfor %}
        """

    def _render_rest_truefalse(self) -> str:
        if q.trueans is None or q.falseans is None:
            raise ValueError("true and/or false answers not present")
        return """
<answer fraction="{{ 100 if q.correctone else 0 }}">
    <text>
    <![CDATA[
        {{ r.fragment(q.trueans[0]) }}
    ]]>
    </text>
    <feedback>
        <text>
        <![CDATA[
            {{ r.fragment(q.trueans[1]) }}
        ]]>
        </text>
    </feedback>
</answer>
<answer fraction="{{ 0 if q.correctone else 100 }}">
    <text>
    <![CDATA[
        {{ r.fragment(q.falseans[0]) }}
    ]]>
    </text>
    <feedback>
        <text>
        <![CDATA[
            {{ r.fragment(q.falseans[1]) }}
        ]]>
        </text>
    </feedback>
</answer>
        """
