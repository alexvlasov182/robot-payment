"""Model for the Robots"""

from enum import StrEnum

from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base


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

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    robot_type = Column(
        SQLEnum(RobotType, name="robot_type"),
        default=RobotType.T1,
        nullable=False,
    )

    status = Column(
        SQLEnum(RobotStatus, name="robot_status"),
        default=RobotStatus.OFFLINE,
        nullable=False,
    )

    serial_number = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    capabilities = Column(
        JSONB,
        nullable=False,
        default=dict,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<Robot(id={self.id}, serial={self.serial_number})>"
