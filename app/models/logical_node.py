from __future__ import annotations

from datetime import datetime

from alembic.environment import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.node_version import NodeVersion

class LogicalNode(Base):
    """Stable identity for a document section across revisions."""

    __tablename__ = "logical_nodes"
    __table_args__ = (
        UniqueConstraint("document_id", "node_key", name="uq_logical_nodes_document_id_node_key"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    node_key: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    document: Mapped["Document"] = relationship(back_populates="logical_nodes")
    node_versions: Mapped[list["NodeVersion"]] = relationship(
        back_populates="logical_node",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )