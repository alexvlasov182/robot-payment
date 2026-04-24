"""Services for robots"""

from sqlalchemy.orm import Session  # type: ignore[reportMissingImports]  # pylint: disable=import-error
from app.models.robot import Robot
from app.schemas.robot import RobotCreate


def create_robot(db: Session, robot_data: RobotCreate):
    """Add robot to the database"""
    db_robot = Robot(**robot_data.model_dump())
    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)
    return db_robot


def get_robots(db: Session):
    """Query to get all robots"""
    return db.query(Robot).all()
