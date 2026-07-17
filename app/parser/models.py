from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ParsedNode:
    """
    Represents a single structural node parsed from a Markdown document.

    Notes:
    - Hierarchy is determined ONLY from Markdown heading level.
    - Section numbers are preserved but never used to determine structure.
    - Body text is preserved exactly as encountered.
    """

    raw_heading: str
    title: str
    level: int
    source_order: int

    section_number: str | None = None
    body: str = ""

    parent: "ParsedNode" | None = field(default=None, repr=False)
    children: list["ParsedNode"] = field(default_factory=list)

    def add_child(self, child: "ParsedNode") -> None:
        child.parent = self
        self.children.append(child)

    @property
    def is_root(self) -> bool:
        return self.parent is None

    def walk(self) -> list["ParsedNode"]:
        """
        Return all nodes in source order using a preorder traversal.

        Since children are always appended in encounter order,
        preorder preserves original source ordering.
        """
        nodes = [self]

        for child in self.children:
            nodes.extend(child.walk())

        return nodes


@dataclass(slots=True)
class ParsedDocument:
    """
    Result returned by the Markdown parser.
    """

    root: ParsedNode

    def walk(self) -> list[ParsedNode]:
        return self.root.walk()

    @property
    def nodes(self) -> list[ParsedNode]:
        return self.walk()

    def headings(self) -> list[ParsedNode]:
        return self.walk()

    def find_titles(self, title: str) -> list[ParsedNode]:
        return [node for node in self.walk() if node.title == title]

    def find_first(self, title: str) -> ParsedNode | None:
        for node in self.walk():
            if node.title == title:
                return node
        return None

    def __iter__(self):
        return iter(self.walk())

    def __len__(self) -> int:
        return len(self.walk())