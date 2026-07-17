from __future__ import annotations

from alembic.environment import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.document_version import DocumentVersion
    from app.models.logical_node import LogicalNode


class NodeVersion(Base):
    """Immutable version-specific snapshot of a logical node."""

    __tablename__ = "node_versions"
    __table_args__ = (
        UniqueConstraint(
            "logical_node_id",
            "document_version_id",
            name="uq_node_versions_logical_node_id_document_version_id",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    logical_node_id: Mapped[int] = mapped_column(
        ForeignKey("logical_nodes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    document_version_id: Mapped[int] = mapped_column(
        ForeignKey("document_versions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    markdown_level: Mapped[int] = mapped_column(Integer, nullable=False)
    section_number: Mapped[str | None] = mapped_column(String(64), nullable=True)

    logical_node: Mapped["LogicalNode"] = relationship(back_populates="node_versions")
    document_version: Mapped["DocumentVersion"] = relationship(back_populates="node_versions")