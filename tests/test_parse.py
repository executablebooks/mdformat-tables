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
    output = mdformat.text(text, extensions={"tables"})
    print(output)
    assert output.rstrip() == expected.rstrip(), output


FIXTURES_COMPACT_PATH = Path(__file__).parent / "fixtures-compact.md"
fixtures_compact = read_fixture_file(FIXTURES_COMPACT_PATH)


@pytest.mark.parametrize(
    "line,title,text,expected", fixtures_compact, ids=[f[1] for f in fixtures_compact]
)
def test_fixtures_compact(line, title, text, expected):
    output = mdformat.text(
        text, extensions={"tables"}, options={"compact_tables": True}
    )
    print(output)
    assert output.rstrip() == expected.rstrip(), output
