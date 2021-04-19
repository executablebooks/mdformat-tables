from pathlib import Path

from markdown_it.utils import read_fixture_file
import mdformat._cli
import pytest

FIXTURE_PATH = Path(__file__).parent / "fixtures.md"
fixtures = read_fixture_file(FIXTURE_PATH)


@pytest.mark.parametrize(
    "line,title,text,expected", fixtures, ids=[f[1] for f in fixtures]
)
def test_fixtures__cli(line, title, text, expected, tmp_path):
    """Test fixtures in tests/fixtures.md."""
    file_path = tmp_path / "test_markdown.md"
    file_path.write_text(text)
    assert mdformat._cli.run([str(file_path)]) == 0
    md_new = file_path.read_text()
    assert md_new == expected


@pytest.mark.parametrize(
    "line,title,text,expected", fixtures, ids=[f[1] for f in fixtures]
)
@pytest.mark.parametrize("wrap", ["keep", "no", 60])
def test_fixtures__cli_opts(line, title, text, expected, wrap, tmp_path):
    """Check that validation error does not trigger when using
    various CLI options."""
    file_path = tmp_path / "test_markdown.md"
    file_path.write_text(text)
    assert mdformat._cli.run([str(file_path), f"--wrap={wrap}"]) == 0
