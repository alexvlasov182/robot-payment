"""Model for the Robots"""

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import JSON, DateTime, ForeignKey, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class RobotType(StrEnum):
    """Robot type enumeration"""

    T1 = "T1"  # Single terminal tester
    T4 = "T4"  # Four terminal tester
    ATM = "ATM"  # ATM tester
    MOBILE = "MOBILE"  # Mobile terminal tester


class RobotStatus(StrEnum):
    """Robot status enumeration"""

    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class Robot(Base):
    """Robot model for the testing platform"""

    __tablename__ = "robots"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    robot_type: Mapped[RobotType] = mapped_column(
        SQLEnum(
            RobotType,
            name="robot_type",
        ),
        default=RobotType.T1,
        nullable=False,
    )

    status: Mapped[RobotStatus] = mapped_column(
        SQLEnum(
            RobotStatus,
            name="robot_status",
        ),
        default=RobotStatus.OFFLINE,
        nullable=False,
    )

    serial_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    capabilities: Mapped[dict] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
        default=dict,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="robots",
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<Robot(id={self.id}, serial={self.serial_number})>"
