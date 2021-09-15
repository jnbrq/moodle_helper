from .moodlexmlhtml import MoodleXMLHTMLRenderer
from .renderer_base import RendererBase
from .question_types import QuestionBase
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List, Callable, Dict
import random
import os


class QuestionWrapper(ABC):
    @property
    @abstractmethod
    def author(self) -> str:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def difficulty(self) -> int:
        ...

    @property
    @abstractmethod
    def created(self) -> datetime:
        ...

    @property
    @abstractmethod
    def tags(self) -> List[str]:
        ...

    @property
    @abstractmethod
    def skip(self) -> bool:
        ...

    @abstractmethod
    def question(self) -> QuestionBase:
        ...

    @abstractmethod
    def parameters_list(self) -> List[Dict[str, object]]:
        ...


class Chooser:
    @staticmethod
    def random(l: List[Any]) -> List[Any]:
        return [random.choice(l)]

    @staticmethod
    def all(l: List[Any]) -> List[Any]:
        return l


class QuizBuilder:
    def __init__(self, quiz_tag, renderer: Callable[[QuestionBase], RendererBase] = MoodleXMLHTMLRenderer) -> None:
        self.questions: List[QuestionWrapper] = []
        self.quiz_tag = quiz_tag
        self.renderer: Callable[[QuestionBase], RendererBase] = renderer

    def fetch_question(self, package_name: str, path: str = ".") -> None:
        old_pwd = os.curdir
        os.chdir(path)
        m = __import__("{package_name}.generate", fromlist=[None])
        qws: List[QuestionWrapper] = getattr(m, "generate")()
        for qw in qws:
            if not qw.skip:
                setattr(qw, "_X_res_dir", os.curdir +
                        os.pathsep + package_name)
                self.questions.append(qw)
        os.chdir(old_pwd)

    def fetch_questions(
            self,
            filterfn: Callable[[QuestionWrapper], bool] = lambda x: True,
            path: str = ".") -> None:
        old_pwd = os.curdir
        os.chdir(path)
        package_names = filter(os.path.isdir, os.listdir(os.curdir))
        for package_name in package_names:
            m = __import__(f"{package_name}.generate", fromlist=[None])
            qws: List[QuestionWrapper] = getattr(m, "generate")()
            for qw in qws:
                if filterfn(qw) and not qw.skip:
                    setattr(qw, "_X_res_dir", os.curdir + "/" + package_name)
                    self.questions.append(qw)
        os.chdir(old_pwd)

    def shuffle_questions(self, shuffler=random.shuffle) -> None:
        shuffler(self.questions)

    def trim_quiz(self, question_count: int = 10) -> None:
        self.questions = self.questions[0:question_count]

    def build(self, chooser: Callable[[List[Any]], List[Any]] = Chooser.random) -> str:
        def qs():
            for qq in self.questions:
                question = qq.question()
                renderer = self.renderer()
                params_list = chooser(qq.parameters_list())
                question.tags.append(self.quiz_tag)
                for params in params_list:
                    question.add_params(**params)
                    question.res_dir = qq._X_res_dir
                    yield question
        renderer = self.renderer()
        return renderer.render_quiz(qs())

    def write_file(self, fname: str, *args, **kwargs) -> None:
        with open(fname, "w") as f:
            f.write(self.build(*args, **kwargs))
