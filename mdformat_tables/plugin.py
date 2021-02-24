from collections import OrderedDict
from typing import List

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdformat.renderer import MDRenderer


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, e.g. by adding a plugin: `mdit.use(myplugin)`"""
    mdit.enable("table")


def _parse_cells(
    rows: List[List[List[Token]]], options: dict, env: dict
) -> List[List[str]]:
    """Convert tokens in each cell to strings."""
    for i, row in enumerate(rows):
        for j, cell_tokens in enumerate(row):
            rows[i][j] = MDRenderer().render(
                cell_tokens,
                options,
                env,
                finalize=False,
            )
    return rows


def _to_string(rows: List[List[str]], align: List[str], widths: dict) -> List[str]:
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


def _render_table(node, renderer_funcs, options, env):
    # gather all cell tokens into row * column array
    rows = []
    align = []

    def _traverse(node):
        for child in node.children:
            if child.type_ == "tr":
                rows.append([])
                align.append([])
            elif child.type_ in ("th", "td"):
                rows[-1].append([])
                style = child.opening.attrGet("style") or ""
                if "text-align:right" in style:
                    align[-1].append(">")
                elif "text-align:left" in style:
                    align[-1].append("<")
                elif "text-align:center" in style:
                    align[-1].append("^")
                else:
                    align[-1].append("")
                inline_token = child.children[0].token
                rows[-1][-1].append(inline_token)

            _traverse(child)

    _traverse(node)

    # parse all cells
    rows = _parse_cells(rows, options, env)

    # work out the widths for each column
    widths = OrderedDict()
    for row in rows:
        for j, cell_text in enumerate(row):
            widths[j] = max(widths.get(j, 3), len(cell_text))

    # write content
    # note: assuming always one header row
    lines = _to_string(rows, align, widths)

    return "\n".join(lines)


RENDERERS = {"table": _render_table}
