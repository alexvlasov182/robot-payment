"""Robots Endpoints"""

from fastapi import APIRouter, Depends  # type: ignore[reportMissingImports]  # pylint: disable=import-error
from sqlalchemy.orm import Session  # type: ignore[reportMissingImports]  # pylint: disable=import-error
from app.core.database import get_db
from app.services.robot_service import create_robot, get_robots
from app.schemas.robot import RobotCreate, RobotResponse

router = APIRouter(prefix="/robots", tags=["Robots"])


@router.post("/", response_model=RobotResponse)
def create_new_robot(robot: RobotCreate, db: Session = Depends(get_db)):
    """Create one Robot"""
    return create_robot(db, robot)


@router.get("/", response_model=list[RobotResponse])
def list_robots(db: Session = Depends(get_db)):
    """Get list of all robots"""
    robots = get_robots(db)
    return robots
