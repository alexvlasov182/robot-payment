from sqlalchemy.orm import Session

from app.models.robot import Robot, RobotType
from app.repositories.base import BaseRepository
from app.schemas.robot import RobotCreate, RobotUpdate


class RobotRepository(BaseRepository[Robot, RobotCreate, RobotUpdate]):
    """Repository for Robot entity"""

    def __init__(self, db: Session):
        super().__init__(Robot, db)

    def get_by_serial_number(self, serial_number: str) -> Robot | None:
        """Get robot by serial number"""
        return self.db.query(Robot).filter(Robot.serial_number == serial_number).first()

    def get_by_type(self, robot_type: RobotType) -> list[Robot]:
        """Get robots by type"""
        return self.db.query(Robot).filter(Robot.robot_type == robot_type).all()

    def get_by_status(self, status: str) -> list[Robot]:
        """Get robots by status"""
        return self.db.query(Robot).filter(Robot.status == status).all()
