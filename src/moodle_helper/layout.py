from typing import *
import math
from dataclasses import dataclass


@dataclass
class Text:
    # TODO support aligment as well
    text: str

    def render(self):
        return self.text


@dataclass
class Image:
    # TODO support alignment as well
    file_path: str
    width: str = "90%"
    max_width: str = "600px"

    def render(self):
        rest_style = "" # "display: block; margin-left: auto; margin-right: auto; "
        if self.max_width:
            return '{{{{ q.image("{}", style="width: {}; max-width: {}; {}") }}}}' \
                .format(self.file_path, self.width, self.max_width, rest_style)
        return '{{{{ q.image("{}", style="width: {}; {}") }}}}'\
            .format(self.file_path, self.width, rest_style)


class SimpleLayout:
    def __init__(self, proportions: List[float] = [1.0]):
        self._cells = [[]]
        self._proportions = proportions

    def render(self) -> str:
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

    def image(self, file_path: str, width: str = "90%", max_width: str = ""):
        self._cells[-1].append(Image(file_path, width, max_width))
        return self
    
    def done(self):
        pass # just for cosmetic purposes

