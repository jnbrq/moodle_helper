from .common import *
import base64
import os


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

    @template
    def render_fragment(self, text):
        if type(text) is str:
            return text
        return text.render()

    @template
    def render_tags(self):
        return """
<tags>
{% for tag in q.tags %}
    <tag>
        <text>
        <![CDATA[
            {{ q.render_fragment(tag) }}
        ]]>
        </text>
    </tag>
{% endfor %}
</tags>
        """

    def image(self, filepath, tag="img", **kwargs):
        with open(self.res_dir + "/" + filepath, "rb") as f:
            # TODO maybe somehow make faster
            image = base64.b64encode(f.read()).decode("utf-8")
        _, ext = os.path.splitext(filepath)
        kwargs["src"] = f"data:image/{ ext };base64,{ image }"
        return Template(
            """
<{{ tag }} {% for k, v in attr.items() %} {{ k }}="{{ v }}" {% endfor %} />
""").render(tag=tag, filepath=filepath, image=image, attr=kwargs)

    @template
    def render(self):
        return """
<question type="{{ q.type }}">
    <name>
        <text>
        <![CDATA[
            {{ q.render_fragment(q.name) }}
        ]]>
        </text>
    </name>
    <questiontext format="html">
        <text>
        <![CDATA[
            {{ q.render_fragment(q.text) }}
        ]]>
        </text>
    </questiontext>
    <generalfeedback format="html">
        <text>
        <![CDATA[
            {{ q.render_fragment(q.generalfeedback) }}
        ]]>
        </text>
    </generalfeedback>
    <penalty>{{ q.penalty }}</penalty>
    <hidden>{{ 1 if q.hidden else 0 }}</hidden>
    {{ q.rest() }}
</question>
        """

    def add_param(self, param, value):
        setattr(self, param, value)

    def add_params(self, **kwargs):
        for k, v in kwargs:
            self.add_param(k, v)

    @template
    def rest(self):
        return ""
