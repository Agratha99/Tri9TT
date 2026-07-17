from __future__ import annotations

from pathlib import Path

import pytest

from app.parser import CT200MarkdownParser

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_fixture(name: str) -> str:
    return (DATA_DIR / name).read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def parser() -> CT200MarkdownParser:
    return CT200MarkdownParser()


@pytest.fixture(scope="module")
def v1_document(parser: CT200MarkdownParser):
    return parser.parse(load_fixture("ct200_manual.md"))


@pytest.fixture(scope="module")
def v2_document(parser: CT200MarkdownParser):
    return parser.parse(load_fixture("ct200_manual_v2.md"))


def test_root_node_is_h1(v1_document):
    root = v1_document.root

    assert root.level == 1
    assert root.parent is None
    assert root.is_root


def test_duplicate_headings_are_preserved(v1_document):
    matches = v1_document.find_titles("Error Codes")

    assert len(matches) == 2
    assert matches[0] is not matches[1]
    assert matches[0].source_order < matches[1].source_order


def test_source_order_is_preserved(v1_document):
    nodes = v1_document.nodes

    orders = [node.source_order for node in nodes]

    assert orders == sorted(orders)


def test_hierarchy_comes_from_heading_level(v1_document):
    for node in v1_document:
        if node.parent is not None:
            assert node.parent.level < node.level


def test_missing_numeric_parent_is_not_created(v1_document):
    section = next(
        node
        for node in v1_document
        if node.section_number == "2.1.1.1"
    )

    assert section.level == 4
    assert section.parent is not None
    assert section.parent.level == 3

    synthesized = [
        node
        for node in v1_document
        if node.section_number == "2.1.1"
    ]

    assert synthesized == []


def test_out_of_order_section_numbers_preserved(v1_document):
    sections = [
        node.section_number
        for node in v1_document
        if node.section_number is not None
    ]

    assert sections.index("3.4") < sections.index("3.3")


def test_html_comments_preserved(v1_document):
    assert any(
        "<!--" in node.body
        for node in v1_document
    )


def test_tables_preserved(v1_document):
    assert any(
        "|" in node.body
        for node in v1_document
    )


def test_ordered_lists_preserved(v1_document):
    assert any(
        "\n1." in ("\n" + node.body)
        for node in v1_document
    )


def test_body_boundaries(v1_document):
    nodes = list(v1_document)

    for node in nodes[:-1]:
        assert not node.body.rstrip().endswith("#")


def test_v1_contains_expected_special_headings(v1_document):
    assert (
        v1_document.find_first("Bluetooth Sync")
        is not None
    )

    assert (
        v1_document.find_first("Error Codes")
        is not None
    )


def test_v2_contains_data_export(v2_document):
    node = next(
        n
        for n in v2_document
        if n.section_number == "5.3"
    )

    assert node.title == "Data Export"


def test_v1_expected_node_count(v1_document):
    #
    # Replace EXPECTED_V1_NODE_COUNT with the
    # agreed CT-200 structural-analysis value.
    #
    EXPECTED_V1_NODE_COUNT = 28

    assert len(v1_document) == EXPECTED_V1_NODE_COUNT


def test_v2_expected_node_count(v2_document):
    #
    # Replace EXPECTED_V2_NODE_COUNT with the
    # agreed CT-200 structural-analysis value.
    #
    EXPECTED_V2_NODE_COUNT = 29

    assert len(v2_document) == EXPECTED_V2_NODE_COUNT