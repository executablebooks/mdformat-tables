from collections import OrderedDict
from typing import Any, List, Mapping, MutableMapping

from markdown_it import MarkdownIt
from mdformat.renderer import RenderTreeNode
from mdformat.renderer.typing import RendererFunc


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, e.g. by adding a plugin: `mdit.use(myplugin)`"""
    mdit.enable("table")


def _parse_cells(
    rows: List[List[RenderTreeNode]],
    renderer_funcs: Mapping[str, RendererFunc],
    options: Mapping[str, Any],
    env: MutableMapping,
) -> List[List[str]]:
    """Convert tokens in each cell to strings."""
    return [[cell.render(renderer_funcs, options, env) for cell in row] for row in rows]


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


def _render_table(
    node: RenderTreeNode,
    renderer_funcs: Mapping[str, RendererFunc],
    options: Mapping[str, Any],
    env: MutableMapping,
) -> str:
    # gather all cell tokens into row * column array
    rows: List[List[RenderTreeNode]] = []
    align: List[List[str]] = []

    def _traverse(node: RenderTreeNode) -> None:
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
                rows[-1].append(inline_node)
            _traverse(child)

    _traverse(node)

    # parse all cells
    parsed_rows = _parse_cells(rows, renderer_funcs, options, env)

    # work out the widths for each column
    widths: MutableMapping[int, int] = OrderedDict()
    for row in parsed_rows:
        for j, cell_text in enumerate(row):
            widths[j] = max(widths.get(j, 3), len(cell_text))

    # write content
    # note: assuming always one header row
    lines = _to_string(parsed_rows, align, widths)

    return "\n".join(lines)


RENDERER_FUNCS: Mapping[str, RendererFunc] = {"table": _render_table}
