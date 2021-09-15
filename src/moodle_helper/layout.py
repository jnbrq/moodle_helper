from typing import *
import math
from dataclasses import dataclass


@dataclass
class Text:
    # TODO support aligment as well
    text: str

    def render(self, *args, **kwargs):
        return self.text


@dataclass
class Image:
    # TODO support alignment as well
    filepath: str
    width: str = "90%"
    max_width: str = "600px"

    def render(self, *args, **kwargs):
        rest_style = "" # "display: block; margin-left: auto; margin-right: auto; "
        if self.max_width:
            return '{{{{ r.image("{}", style="width: {}; max-width: {}; {}") }}}}' \
                .format(self.filepath, self.width, self.max_width, rest_style)
        return '{{{{ r.image("{}", style="width: {}; {}") }}}}'\
            .format(self.filepath, self.width, rest_style)


class SimpleLayout:
    def __init__(self, proportions: List[float] = [1.0]):
        self._cells = [[]]
        self._proportions = proportions

    def render(self, *args, **kwargs) -> str:
        num_cols = len(self._proportions)
        num_rows = math.ceil((len(self._cells) - 1) / num_cols)
        out_html = []
        # first, add the header
        for e in self._cells[0]:
            out_html.append(e.render())
            out_html.append("<br />")

        # now, create a table
        column_props = [
            f"style=\"width: { x * 100 }%;\"" for x in self._proportions]

        out_html.append("<table style=\"border: none;\">")

        for i in range(num_rows):
            out_html.append("<tr style=\"border: none;\">")
            for j in range(num_cols):
                out_html.append(
                    f"<td style=\"width: { self._proportions[j] * 100 }%; border: none;\">")
                idx = i * num_cols + j + 1
                if idx < len(self._cells):
                    for e in self._cells[idx]:
                        out_html.append(e.render())
                        out_html.append("<br />")
                out_html.append("</td>")
            out_html.append("</tr>")

        out_html.append("</table>")

        return "\n".join(out_html)

    def next_cell(self):
        self._cells.append([])
        return self

    def text(self, text: str):
        self._cells[-1].append(Text(text))
        return self

    def image(self, filepath: str, width: str = "90%", max_width: str = ""):
        self._cells[-1].append(Image(filepath, width, max_width))
        return self
    
    def done(self):
        pass # just for cosmetic purposes

