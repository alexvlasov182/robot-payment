from re import S

from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, null
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class RobotType(str, enum.Enum):
    T1 = "T1"  # tests one terminal
    T4 = "T4"  # tests four terminals
    ATM = "ATM"  # tests ATM machines
    MOBILE = "MOBILE"  # tests wireless terminals


class Robot(Base):
    __tablename__ = "robots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    robot_type: Column = Column(SQLEnum(RobotType), default=RobotType.T1)
    status = Column(String, default="offline")
    serial_number = Column(String, unique=True, nullable=False)
    capabilities = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
