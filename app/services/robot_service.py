"""Robot service layer."""

from sqlalchemy.orm import Session

from app.core.redis_client import cache
from app.models.robot import Robot
from app.models.user import User
from app.repositories.robot_repository import RobotRepository
from app.schemas.robot import RobotCreate, RobotUpdate


class RobotService:
    """Service layer for robot operations."""

    def __init__(self, db: Session):
        self.robot_repo = RobotRepository(db)

    def create_robot(self, robot_data: RobotCreate, current_user: User) -> Robot:
        """Create a new robot, owned by current_user."""
        if self.robot_repo.get_by_serial_number(robot_data.serial_number):
            raise ValueError("Robot with this serial number already exists")

        robot = self.robot_repo.create_for_owner(robot_data, current_user.id)

        cache.delete(f"all_robots_{current_user.id}")

        return robot

    def get_all_robots(self, current_user: User) -> list[Robot]:
        """Return only robots owned by current_user, with Redis cache support."""
        cache_key = f"all_robots_{current_user.id}"
        cached_robots = cache.get(cache_key)
        if cached_robots is not None:
            return [Robot(**item) for item in cached_robots]

        robots = self.robot_repo.get_all_for_owner(current_user.id)

        robots_data = [
            {
                "id": r.id,
                "name": r.name,
                "robot_type": r.robot_type,
                "status": r.status,
                "serial_number": r.serial_number,
                "capabilities": r.capabilities,
                "owner_id": r.owner_id,
            }
            for r in robots
        ]

        cache.set(cache_key, robots_data, expire=60)
        return robots

    def get_robot(self, robot_id: int, current_user: User) -> Robot | None:
        """Return a robot by ID, only if it belongs to current_user."""
        cache_key = f"robot_{robot_id}_{current_user.id}"
        cached_robot = cache.get(cache_key)
        if cached_robot is not None:
            return Robot(**cached_robot)

        robot = self.robot_repo.get_for_owner(robot_id, current_user.id)

        if robot:
            robot_data = {
                "id": robot.id,
                "name": robot.name,
                "robot_type": robot.robot_type,
                "status": robot.status,
                "serial_number": robot.serial_number,
                "capabilities": robot.capabilities,
                "owner_id": robot.owner_id,
            }
            cache.set(cache_key, robot_data, expire=60)

        return robot

    def update_robot(
        self,
        robot_id: int,
        robot_data: RobotUpdate,
        current_user: User,
    ):
        """Update robot, only if it belongs to current_user."""
        robot = self.robot_repo.get_for_owner(robot_id, current_user.id)

        if not robot:
            return None

        update_data = robot_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(robot, field, value)

        self.robot_repo.db.commit()
        self.robot_repo.db.refresh(robot)

        cache.delete(f"all_robots_{current_user.id}")
        cache.delete(f"robot_{robot_id}_{current_user.id}")

        return robot

    def update_robot_status(
        self, robot_id: int, data: RobotUpdate, current_user: User
    ) -> Robot | None:
        """Update robot status, only if it belongs to current_user."""
        robot = self.robot_repo.get_for_owner(robot_id, current_user.id)
        if not robot:
            return None

        robot = self.robot_repo.update(robot_id, data)

        if robot:
            cache.delete(f"all_robots_{current_user.id}")
            cache.delete(f"robot_{robot_id}_{current_user.id}")

        return robot

    def delete_robot(self, robot_id: int, current_user: User) -> bool:
        """Delete a robot, only if it belongs to current_user."""
        robot = self.robot_repo.get_for_owner(robot_id, current_user.id)
        if not robot:
            return False

        result = self.robot_repo.delete(robot_id)

        if result:
            cache.delete(f"all_robots_{current_user.id}")
            cache.delete(f"robot_{robot_id}_{current_user.id}")

        return result
