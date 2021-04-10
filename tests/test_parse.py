from pathlib import Path

from markdown_it.utils import read_fixture_file
import mdformat
import pytest

FIXTURE_PATH = Path(__file__).parent / "fixtures.md"
fixtures = read_fixture_file(FIXTURE_PATH)


@pytest.mark.parametrize(
    "line,title,text,expected", fixtures, ids=[f[1] for f in fixtures]
)
def test_fixtures(line, title, text, expected):
    if title in {"Escaped table 1", "Escaped table 2", "Escaped table 3"}:
        pytest.xfail("TODO: Fix escaped tables")
    output = mdformat.text(text, extensions={"tables"})
    print(output)
    assert output.rstrip() == expected.rstrip(), output
