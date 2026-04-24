"""Main file for the robot schemas"""

from typing import Optional
from pydantic import BaseModel  # type: ignore[reportMissingImports]  # pylint: disable=import-error
from app.models.robot import RobotType


class RobotCreate(BaseModel):
    """Schema for the creating Robot"""

    name: str
    serial_number: str
    robot_type: Optional[RobotType] = RobotType.T1
    capabilities: Optional[str] = None


class RobotResponse(BaseModel):
    """Schema for the response from the robot"""

    id: int
    name: str
    robot_type: RobotType
    status: str
    serial_number: str
    capabilites: Optional[str]

    class Config:
        """Class config"""

        from_attributes = True


# type: ignore[reportMissingImports]  # pylint: disable=import-error
