"""Robot repository."""

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

    def get_all_for_owner(self, owner_id: int) -> list[Robot]:
        """Get all robots belonging to a specific owner."""
        return self.db.query(Robot).filter(Robot.owner_id == owner_id).all()

    def get_for_owner(self, robot_id: int, owner_id: int) -> Robot | None:
        """Get a single robot by id, only if it belongs to owner_id."""
        return (
            self.db.query(Robot)
            .filter(Robot.id == robot_id, Robot.owner_id == owner_id)
            .first()
        )

    def create_for_owner(self, robot_data: RobotCreate, owner_id: int) -> Robot:
        """Create a robot explicitly assigned to owner_id."""
        obj_data = robot_data.model_dump(exclude_unset=True)
        robot = Robot(**obj_data, owner_id=owner_id)
        self.db.add(robot)
        self.db.commit()
        self.db.refresh(robot)
        return robot
