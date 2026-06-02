"""Model for the Robots"""

import enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, DateTime, func
from app.core.database import Base


class RobotType(str, enum.Enum):
    """Robot type enumeration"""

    T1 = "T1"  # Single terminal tester
    T4 = "T4"  # Four terminal tester
    ATM = "ATM"  # ATM tester
    MOBILE = "MOBILE"  # Mobile terminal tester


class Robot(Base):
    """Robot model for payment terminal testing"""

    __tablename__ = "robots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    robot_type: Column = Column(SQLEnum(RobotType), default=RobotType.T1)
    status = Column(String, default="offline")
    serial_number = Column(String, unique=True, nullable=False)
    capabilities = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
