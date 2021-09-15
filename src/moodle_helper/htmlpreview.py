from .renderer_base import *
from .question_types import *
from .module_resources import ModuleResources
import os
from jinja2 import Template

resources = ModuleResources(__file__)


class HTMLPreview(RendererBase):
    def __init__(self) -> None:
        super().__init__()
        self.q = None
        self.qs = None

    @render_jinja
    def render_quiz(self, qs: Iterable[QuestionBase], *args, **kwargs) -> str:
        self.qs = qs
        self.n = 0
        return resources.text("render_quiz.html")

    @render_jinja
    def render_question(self, q: QuestionBase) -> str:
        self.q = q
        self.n = self.n + 1
        return resources.text("render_question.html")

    def jinja(self, t: str) -> str:
        template = Template(t)
        return template.render(q=self.q, qs=self.qs, r=self)

    def image(self, filepath: str, tag: str = "img", *args, **kwargs) -> str:
        with open(self.q.res_dir + "/" + filepath, "rb") as f:
            _, ext = os.path.splitext(filepath)
            kwargs["src"] = base64_embed(f, f"data:image/{ ext }")
        return Template(resources.text("image.html")).render(tag=tag, filepath=filepath, attr=kwargs)

    @render_jinja
    def _render_tags(self) -> str:
        return resources.text("render_tags.html")

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
            "unknown question type for HTMLPreview")

    def _render_rest_multiplechoice(self) -> str:
        if not self.q.answernumbering in ["none", "abc", "ABCD", "123"]:
            raise ValueError("invalid answernumbering")

        return resources.text("render_rest_multiplechoice.html")

    def _render_rest_numerical(self) -> str:
        return resources.text("render_rest_numerical.html")

    def _render_rest_shortanswer(self) -> str:
        return resources.text("render_rest_shortanswer.html")

    def _render_rest_truefalse(self) -> str:
        if self.q.trueans is None or self.q.falseans is None:
            raise ValueError("true and/or false answers not present")
        return resources.text("render_rest_truefalse.html")
