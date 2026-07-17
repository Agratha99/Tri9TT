from __future__ import annotations

import re
from typing import Final

from .models import ParsedDocument, ParsedNode

_HEADING_RE: Final = re.compile(
    r"^(#{1,4})[ \t]+(.+?)\s*$"
)

_SECTION_RE: Final = re.compile(
    r"^((?:\d+\.)*\d+)\s+(.*)$"
)


class CT200MarkdownParser:
    """
    Deterministic line-based parser for CT-200 manuals.

    Parsing rules:

    * Only ATX headings (# through ####) create structural nodes.
    * Heading hierarchy comes ONLY from heading level.
    * Numeric prefixes are preserved but never interpreted.
    * Duplicate headings remain separate nodes.
    * Missing numeric parents are never synthesized.
    * Body text is preserved exactly.
    """

    def parse(self, markdown: str) -> ParsedDocument:
        if not markdown:
            raise ValueError("Markdown document is empty.")

        lines = markdown.splitlines()

        root: ParsedNode | None = None
        current_node: ParsedNode | None = None

        # Stack always contains the active heading chain.
        stack: list[ParsedNode] = []

        source_order = 0

        for line in lines:
            heading = self._parse_heading(line)

            if heading is None:
                if current_node is not None:
                    self._append_body_line(current_node, line)
                continue

            level, raw_heading, section_number, title = heading

            node = ParsedNode(
                raw_heading=raw_heading,
                title=title,
                section_number=section_number,
                level=level,
                source_order=source_order,
            )
            source_order += 1

            if root is None:
                if level != 1:
                    raise ValueError(
                        "Document must begin with an H1 heading."
                    )

                root = node
                current_node = node
                stack = [node]
                continue

            while stack and stack[-1].level >= level:
                stack.pop()

            if stack:
                stack[-1].add_child(node)

            stack.append(node)
            current_node = node

        if root is None:
            raise ValueError("No H1 heading found.")

        return ParsedDocument(root=root)

    @staticmethod
    def _parse_heading(
        line: str,
    ) -> tuple[int, str, str | None, str] | None:
        """
        Parse an ATX heading.

        Returns:
            (
                markdown_level,
                raw_heading,
                section_number,
                display_title,
            )
        """

        match = _HEADING_RE.match(line)

        if match is None:
            return None

        hashes = match.group(1)
        raw_heading = match.group(2)

        level = len(hashes)

        section_number: str | None = None
        display_title = raw_heading

        section_match = _SECTION_RE.match(raw_heading)

        if section_match is not None:
            section_number = section_match.group(1)
            display_title = section_match.group(2).strip()

        return (
            level,
            raw_heading,
            section_number,
            display_title,
        )

    @staticmethod
    def _append_body_line(
        node: ParsedNode,
        line: str,
    ) -> None:
        """
        Preserve body exactly.

        Blank lines, HTML comments, tables,
        ordered lists and ordinary prose are
        retained without normalization.
        """

        if node.body:
            node.body += "\n"

        node.body += line
    
    
    def parse_file(self, path: str) -> ParsedDocument:
        """
        Parse a UTF-8 Markdown file.
        """

        with open(path, encoding="utf-8") as fp:
            return self.parse(fp.read())

    @staticmethod
    def flatten(root: ParsedNode) -> list[ParsedNode]:
        """
        Return every node in source order.

        Since children are appended in encounter order,
        a preorder traversal preserves the document order.
        """
        return root.walk()

    @staticmethod
    def iter_nodes(root: ParsedNode):
        """
        Iterate over every parsed node in source order.
        """
        yield from root.walk()

    @staticmethod
    def print_tree(
        root: ParsedNode,
        indent: int = 0,
    ) -> None:
        """
        Convenience debugging helper.

        Not used by production code.
        """
        prefix = "  " * indent

        if root.section_number:
            label = f"{root.section_number} {root.title}"
        else:
            label = root.title

        print(f"{prefix}H{root.level}: {label}")

        for child in root.children:
            CT200MarkdownParser.print_tree(
                child,
                indent + 1,
            )


def parse_markdown(markdown: str) -> ParsedDocument:
    """
    Convenience API.
    """
    return CT200MarkdownParser().parse(markdown)


def parse_markdown_file(path: str) -> ParsedDocument:
    """
    Convenience API.
    """
    return CT200MarkdownParser().parse_file(path)