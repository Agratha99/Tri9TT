from __future__ import annotations

from datetime import datetime

from alembic.environment import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.node_version import NodeVersion

class DocumentVersion(Base):
    """Immutable snapshot of a document."""

    __tablename__ = "document_versions"
    __table_args__ = (
        UniqueConstraint("document_id", "version", name="uq_document_versions_document_id_version"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    document: Mapped["Document"] = relationship(back_populates="document_versions")
    node_versions: Mapped[list["NodeVersion"]] = relationship(
        back_populates="document_version",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )