"""An mdformat plugin for rendering tables."""

__version__ = "0.4.1"

from .plugin import (  # noqa: F401
    POSTPROCESSORS,
    RENDERERS,
    add_cli_options,
    update_mdit,
)
