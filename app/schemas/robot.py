"""Main file for the robot schemas"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.robot import RobotType


class RobotCreate(BaseModel):
    """Schema for creating Robot"""

    name: str = Field(..., min_length=2, max_length=100, description="Robot name")
    serial_number: str = Field(..., min_length=3, description="Unique serial number")
    robot_type: RobotType | None = Field(default=RobotType.T1, description="Robot type")
    capabilities: dict[str, Any] = Field(
        default_factory=dict, description="Robot capabilities configuration"
    )


class RobotUpdate(BaseModel):
    """Request schema for updating a robot"""

    name: str | None = None
    status: str | None = None
    capabilities: dict[str, Any] | None = None


class RobotResponse(BaseModel):
    """Response schema for robot data"""

    id: int
    name: str
    robot_type: RobotType
    status: str
    serial_number: str
    capabilities: dict[str, Any]

    model_config = ConfigDict(from_attributes=True)
