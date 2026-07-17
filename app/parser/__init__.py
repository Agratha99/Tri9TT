"""
CT-200 Markdown parser package.

This package contains the in-memory parser used during
Phase 2 – Milestone 3.

Responsibilities:
- Parse Markdown documents into a hierarchical structure.
- Preserve document structure and body text exactly.
- Expose convenient parsing APIs.

Non-responsibilities:
- Database persistence
- ORM integration
- Version matching
- Content hashing
- LogicalNode assignment
- Ingestion services
- API endpoints
"""

from .markdown_parser import (
    CT200MarkdownParser,
    parse_markdown,
    parse_markdown_file,
)
from .models import (
    ParsedDocument,
    ParsedNode,
)

__all__ = [
    "CT200MarkdownParser",
    "ParsedDocument",
    "ParsedNode",
    "parse_markdown",
    "parse_markdown_file",
]