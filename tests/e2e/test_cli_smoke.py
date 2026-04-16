"""CLI smoke tests.

These tests check importability and parser creation without starting a real
stdio session.
"""

from tavily_fastmcp.server import build_arg_parser


def test_arg_parser_accepts_transport_override() -> None:
    """The CLI parser should parse a transport override."""
    parser = build_arg_parser()
    namespace = parser.parse_args(["--transport", "stdio"])
    assert namespace.transport == "stdio"
