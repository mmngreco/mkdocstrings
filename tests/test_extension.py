"""Tests for the extension module."""
from textwrap import dedent

from markdown import Markdown

from mkdocstrings.extension import MkdocstringsExtension
from mkdocstrings.handlers.base import Handlers

_DEFAULT_CONFIG = {  # noqa: WPS407 (mutable constant)
    "theme_name": "material",
    "mdx": [],
    "mdx_configs": {},
    "mkdocstrings": {"default_handler": "python", "custom_templates": None, "watch": [], "handlers": {}},
}


def test_render_html_escaped_sequences():
    """Assert HTML-escaped sequences are correctly parsed as XML."""
    config = dict(_DEFAULT_CONFIG)
    config["mdx"].append(MkdocstringsExtension(config, Handlers(config)))
    md = Markdown(extensions=config["mdx"])

    md.convert("::: tests.fixtures.html_escaped_sequences")


def test_multiple_footnotes():
    """Assert footnotes don't get added to subsequent docstrings."""
    config = dict(_DEFAULT_CONFIG, mdx=["footnotes"])
    config["mdx"].append(MkdocstringsExtension(config, Handlers(config)))
    md = Markdown(extensions=config["mdx"])

    output = md.convert(
        dedent(
            """
            Top.[^aaa]

            ::: tests.fixtures.footnotes.func_a

            ::: tests.fixtures.footnotes.func_b

            ::: tests.fixtures.footnotes.func_c

            [^aaa]: Top footnote
            """
        )
    )
    assert output.count("Footnote A") == 1
    assert output.count("Footnote B") == 1
    assert output.count("Top footnote") == 1


def test_reference_inside_autodoc():
    """Assert cross-reference Markdown extension works correctly."""
    config = dict(_DEFAULT_CONFIG)
    config["mdx"].append(MkdocstringsExtension(config, Handlers(config)))
    md = Markdown(extensions=config["mdx"])

    output = md.convert("::: tests.fixtures.cross_reference")
    snippet = 'Link to <span data-mkdocstrings-identifier="something.Else">something.Else</span>.'
    assert snippet in output
