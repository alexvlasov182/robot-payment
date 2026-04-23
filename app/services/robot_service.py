from sqlalchemy.orm import Session
from app.models.robot import Robot
from app.schemas.robot import RobotCreate


def create_robot(db: Session, robot_data: RobotCreate):
    db_robot = Robot(**robot_data.model_dump())
    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)
    return db_robot


def get_robots(db: Session):
    return db.query(Robot).all()
