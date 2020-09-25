from typing import List, Optional, Tuple

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdformat.renderer import MDRenderer


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, e.g. by adding a plugin: `mdit.use(myplugin)`"""
    pass


def render_token(
    renderer: MDRenderer,
    tokens: List[Token],
    index: int,
    options: dict,
    env: dict,
) -> Optional[Tuple[str, int]]:
    """Convert token(s) to a string, or return None if no render method
    available.

    :returns: (text, index) where index is of the final "consumed" token
    """
    return None
