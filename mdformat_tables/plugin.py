from typing import List, Mapping, Sequence

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Postprocess, Render


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, e.g. by adding a plugin: `mdit.use(myplugin)`"""
    mdit.enable("table")


def _to_string(
    rows: Sequence[Sequence[str]], align: Sequence[Sequence[str]], widths: Sequence[int]
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
    for descendant in node.walk(include_self=False):
        if descendant.type == "tr":
            rows.append([])
            align.append([])
        elif descendant.type in ("th", "td"):
            style = descendant.attrs.get("style") or ""
            assert isinstance(style, str)
            if "text-align:right" in style:
                align[-1].append(">")
            elif "text-align:left" in style:
                align[-1].append("<")
            elif "text-align:center" in style:
                align[-1].append("^")
            else:
                align[-1].append("")
            rows[-1].append(descendant.render(context))

    # work out the widths for each column
    widths = [
        max(3, *(len(row[col_idx]) for row in rows)) for col_idx in range(len(rows[0]))
    ]

    # write content
    # note: assuming always one header row
    lines = _to_string(rows, align, widths)

    return "\n".join(lines)


def _render_cell(node: RenderTreeNode, context: RenderContext) -> str:
    inline_node = node.children[0]
    text = inline_node.render(context)
    return text.replace("|", "\\|")


def _escape_tables(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    # Escape the first "-" character of a line if every character on that line
    # is one of {" ", "|", "-"}. Lines like this could otherwise be parsed
    # as a delimiter row of a table.
    return "\n".join(
        line.replace("-", "\\-", 1) if all(c in "|-: " for c in line) else line
        for line in text.split("\n")
    )


RENDERERS: Mapping[str, Render] = {
    "table": _render_table,
    "td": _render_cell,
    "th": _render_cell,
}
POSTPROCESSORS: Mapping[str, Postprocess] = {"paragraph": _escape_tables}
