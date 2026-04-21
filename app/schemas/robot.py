from pydantic import BaseModel
from typing import Optional
from app.models.robot import RobotType


class RobotCreate(BaseModel):
    name: str
    serial_number: str
    robot_type: Optional[RobotType] = RobotType.T1
    capabilities: Optional[str] = None


class RobotResponse(BaseModel):
    id: int
    name: str
    robot_type: RobotType
    status: str
    serial_number: str
    capabilites: Optional[str]

    class Config:
        from_attributes = True
