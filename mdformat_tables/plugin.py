from collections import OrderedDict
from typing import List, Mapping, MutableMapping

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Postprocess, Render


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, e.g. by adding a plugin: `mdit.use(myplugin)`"""
    mdit.enable("table")


def _to_string(
    rows: List[List[str]], align: List[List[str]], widths: Mapping[int, int]
) -> List[str]:
    lines = []
    lines.append(
        "| "
        + " | ".join(
            f"{{:{al or '<'}{widths[i]}}}".format(text)
            for i, (text, al) in enumerate(zip(rows[0], align[0]))
        )
        + " |"
    )
    lines.append(
        "| "
        + " | ".join(
            (":" if al in ("<", "^") else "-")
            + "-" * (widths[i] - 2)
            + (":" if al in (">", "^") else "-")
            for i, al in enumerate(align[0])
        )
        + " |"
    )
    for row, als in zip(rows[1:], align[1:]):
        lines.append(
            "| "
            + " | ".join(
                f"{{:{al or '<'}{widths[i]}}}".format(text)
                for i, (text, al) in enumerate(zip(row, als))
            )
            + " |"
        )
    return lines


def _render_table(node: RenderTreeNode, context: RenderContext) -> str:
    """Render a `RenderTreeNode` of type "table"."""
    # gather rendered cell content into row * column array
    rows: List[List[str]] = []
    align: List[List[str]] = []

    def _gather_cells(node: RenderTreeNode) -> None:
        """Recursively gather cell content and alignment to `rows` and
        `align`."""
        for child in node.children:
            if child.type == "tr":
                rows.append([])
                align.append([])
            elif child.type in ("th", "td"):
                style = child.attrs.get("style") or ""
                if "text-align:right" in style:
                    align[-1].append(">")
                elif "text-align:left" in style:
                    align[-1].append("<")
                elif "text-align:center" in style:
                    align[-1].append("^")
                else:
                    align[-1].append("")
                inline_node = child.children[0]
                rows[-1].append(inline_node.render(context))
            _gather_cells(child)

    _gather_cells(node)

    # work out the widths for each column
    widths: MutableMapping[int, int] = OrderedDict()
    for row in rows:
        for j, cell_text in enumerate(row):
            widths[j] = max(widths.get(j, 3), len(cell_text))

    # write content
    # note: assuming always one header row
    lines = _to_string(rows, align, widths)

    return "\n".join(lines)


def _escape_tables(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    # Escape the first "-" character of a line if every character on that line
    # is one of {" ", "|", "-"}. Lines like this could otherwise be parsed
    # as a delimiter row of a table.
    return "\n".join(
        line.replace("-", "\\-", 1) if all(c in "|-: " for c in line) else line
        for line in text.split("\n")
    )


RENDERERS: Mapping[str, Render] = {"table": _render_table}
POSTPROCESSORS: Mapping[str, Postprocess] = {"paragraph": _escape_tables}
