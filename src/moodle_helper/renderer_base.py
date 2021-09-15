from abc import ABC, abstractmethod
import base64
from io import FileIO
from typing import Iterable, List
from .question_types import QuestionBase

def render_jinja(f, *args, **kwargs):
    def closure(self, *_args, **_kwargs):
        r = f(self, *_args, **_kwargs)
        if r is None:
            return "@@NONE@@"
        return self.jinja(r, *args, **kwargs)
    return closure

def base64_embed(f: FileIO, data_type: str="data:image/png") -> str:
    data = base64.b64encode(f.read()).decode("utf-8")
    return f"{ data_type };base64,{ data }"

class RendererBase(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def render_quiz(self, qs: Iterable[QuestionBase], *args, **kwargs) -> str:
        ...

    @abstractmethod
    def render_question(self, q: QuestionBase, *args, **kwargs) -> str:
        ...
    
    @abstractmethod
    def jinja(self, t: str, *args, **kwargs) -> str:
        ...
    
    @abstractmethod
    def image(self, filepath: str, *args, **kwargs) -> str:
        ...
    
    @render_jinja
    def fragment(self, obj: object, *args, **kwargs) -> str:
        if hasattr(obj, "render"):
            return obj.render(q=self.q)
        return str(obj)
    
    def raw(self, obj: object, *args, **kwargs) -> str:
        # not supposed to be rendered by jinja
        if hasattr(obj, "render"):
            return obj.render(q=self.q, r=self)
        return str(obj)
