from moodle_helper.htmlpreview import HTMLPreview
from .moodlexmlhtml import MoodleXMLHTMLRenderer
from .renderer_base import RendererBase
from .question_types import QuestionBase
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List, Callable, Dict, Optional
import random
import os
import sys


class QuestionWrapper(ABC):
    """
    Children of this class should have the following properties:

        @property
        def author(self) -> str:
            ...

        @property
        def name(self) -> str:
            ...

        @property
        def difficulty(self) -> int:
            ...

        @property
        def created(self) -> datetime:
            ...

        @property
        def tags(self) -> List[str]:
            ...

        @property
        def skip(self) -> bool:
            ...

        def question(self) -> QuestionBase:
            ...

        def parameters_list(self) -> List[Dict[str, object]]:
            ...
    """


class Chooser:
    @staticmethod
    def random(k: int = 1) -> Callable[[List], List]:
        def f(l: List[Any]) -> List[Any]:
            random.shuffle(l)
            return l[0:k]
        return f

    @staticmethod
    def all(l: List[Any]) -> List[Any]:
        return l
    
    @staticmethod
    def explode(l: List[Any]) -> List[Any]:
        return l * 100


class QuizBuilder:
    def __init__(self, quiz_tag) -> None:
        self.questions: List[QuestionWrapper] = []
        self.quiz_tag = quiz_tag

    def fetch_question(self, package_name: str, path: str = ".") -> None:
        sys.path.append(path)
        m = __import__("{package_name}.generate", fromlist=[None])
        qws: List[QuestionWrapper] = getattr(m, "generate")()
        for qw in qws:
            if not qw.skip:
                self.questions.append(qw)
        sys.path.remove(path)

    def fetch_questions(
            self,
            filterfn: Callable[[QuestionWrapper], bool] = lambda x: True,
            path: str = ".") -> None:
        sys.path.append(path)
        package_names = filter(lambda p: os.path.isdir(path + "/" + p), os.listdir(path + "/"))
        for package_name in package_names:
            m = __import__(f"{package_name}.generate", fromlist=[None])
            qws: List[QuestionWrapper] = getattr(m, "generate")()
            for qw in qws:
                if filterfn(qw) and not qw.skip:
                    self.questions.append(qw)
        sys.path.remove(path)
                

    def shuffle_questions(self, shuffler=random.shuffle) -> None:
        shuffler(self.questions)

    def trim_quiz(self, question_count: int = 10) -> None:
        self.questions = self.questions[0:question_count]

    def build(self,
              renderer_factory: Callable[[QuestionBase],
                                         RendererBase] = MoodleXMLHTMLRenderer,
              chooser: Callable[[List[Any]], List[Any]] = Chooser.random(1)) -> str:
        def qs():
            for qq in self.questions:
                question = qq.question()
                params_list = chooser(qq.parameters_list())
                question.tags.append(self.quiz_tag)
                for params in params_list:
                    question.add_params(**params)
                    yield question
        renderer = renderer_factory()
        return renderer.render_quiz(qs())
    
    def begin(self, question_tag: Optional[str] = None) -> None:
        if question_tag is not None:
            self._question_tag = f"{self.quiz_tag}+{question_tag}"
        else:
            self._question_tag = None
        self._added_questions = 0
        print(f"Current tag = {self._question_tag}")
    
    def add(self, qws: List[QuestionWrapper]) -> None:
        if self._question_tag is not None:
            for qw in qws:
                qw.tags.append(self._question_tag)
        self.questions.extend(qws)
        self._added_questions = self._added_questions + len(qws)

    def end(self) -> None:
        print(f"Done adding {self._added_questions} question(s).")

    def output_moodle_xml(self, fname: str, *args, **kwargs) -> None:
        with open(fname, "w") as f:
            f.write(self.build(renderer_factory=MoodleXMLHTMLRenderer, *args, **kwargs))
    
    def output_html_preview(self, fname: str, *args, **kwargs) -> None:
        with open(fname, "w") as f:
            f.write(self.build(renderer_factory=HTMLPreview, *args, **kwargs))
