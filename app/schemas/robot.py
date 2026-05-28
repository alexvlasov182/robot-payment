"""Main file for the robot schemas"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.robot import RobotType


class RobotCreate(BaseModel):
    """Schema for the creating Robot"""

    name: str = Field(..., min_length=2, max_length=100, description="Robot name")
    serial_number: str = Field(..., min_length=3, description="Unique serial number")
    robot_type: Optional[RobotType] = Field(
        default=RobotType.T1, description="Robot type"
    )
    capabilities: Optional[str] = Field(
        None, description="Comma-separated capabilities"
    )


class RobotUpdate(BaseModel):
    """Request schema for update a robot"""

    name: Optional[str] = None
    status: Optional[str] = None
    capabilities: Optional[str] = None


class RobotResponse(BaseModel):
    """Response schema for robot data"""

    id: int
    name: str
    robot_type: RobotType
    status: str
    serial_number: str
    capabilities: Optional[str]

    model_config = ConfigDict(from_attributes=True)
