from abc import ABC, abstractmethod
import base64
from io import FileIO
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
    def __init__(self, q: QuestionBase) -> None:
        super().__init__()
        self.q = q

    @abstractmethod
    def render_question(self, *args, **kwargs) -> str:
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
        l = []
        l.append("{{ raw }}")
        if hasattr(obj, "render"):
            l.append(obj.render(q=self.q))
        else:
            l.append(str(obj))
        l.append("{{ endraw }}")
        return "\n".join(l)
