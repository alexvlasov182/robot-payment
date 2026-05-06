"""Services for robots"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.robot import Robot
from app.repositories.robot_repository import RobotRepository
from app.schemas.robot import RobotCreate, RobotUpdate


class RobotService:
    """Robot service with dependency injection"""

    def __init__(self, db: Session):
        self.robot_repo = RobotRepository(db)

    def create_robot(self, robot_data: RobotCreate) -> Robot:
        """Create a new robot"""
        if self.robot_repo.get_by_serial_number(robot_data.serial_number):
            raise ValueError("Robot with this serial number already exists")

        return self.robot_repo.create(robot_data)

    def get_all_robots(self) -> List[Robot]:
        """Get all robots"""
        return self.robot_repo.get_all()

    def get_robot(self, robot_id: int) -> Optional[Robot]:
        """Get robot by ID"""
        return self.robot_repo.get(robot_id)

    def update_robot_status(self, robot_id: int, status: str) -> Optional[Robot]:
        """Update robot status"""
        update_data = RobotUpdate(status=status)
        return self.robot_repo.update(robot_id, update_data)

    def delete_robot(self, robot_id: int) -> bool:
        """Delete robot"""
        return self.robot_repo.delete(robot_id)
