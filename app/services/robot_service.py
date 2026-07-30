"""Robot service layer."""

from sqlalchemy.orm import Session

from app.core.redis_client import cache
from app.models.robot import Robot
from app.repositories.robot_repository import RobotRepository
from app.schemas.robot import RobotCreate, RobotUpdate


class RobotService:
    """Service layer for robot operations."""

    def __init__(self, db: Session):
        self.robot_repo = RobotRepository(db)

    def create_robot(self, robot_data: RobotCreate) -> Robot:
        """Create a new robot."""
        if self.robot_repo.get_by_serial_number(robot_data.serial_number):
            raise ValueError("Robot with this serial number already exists")

        robot = self.robot_repo.create(robot_data)

        # Clear the cache after creating a robot.
        cache.delete("all_robots")

        return robot

    def get_all_robots(self) -> list[Robot]:
        """Return all robots with Redis cache support."""
        cached_robots = cache.get("all_robots")
        if cached_robots is not None:
            # Convert cached data back to Robot objects.
            return [Robot(**item) for item in cached_robots]

        robots = self.robot_repo.get_all()

        robots_data = [
            {
                "id": r.id,
                "name": r.name,
                "robot_type": r.robot_type,
                "status": r.status,
                "serial_number": r.serial_number,
                "capabilities": r.capabilities,
            }
            for r in robots
        ]

        # Store robot data in the cache for 60 seconds.
        cache.set("all_robots", robots_data, expire=60)
        return robots

    def get_robot(self, robot_id: int) -> Robot | None:
        """Return a robot by ID."""

        cache_key = f"robot_{robot_id}"
        cached_robot = cache.get(cache_key)
        if cached_robot is not None:
            return Robot(**cached_robot)

        robot = self.robot_repo.get(robot_id)

        if robot:
            robot_data = {
                "id": robot.id,
                "name": robot.name,
                "robot_type": robot.robot_type,
                "status": robot.status,
                "serial_number": robot.serial_number,
                "capabilities": robot.capabilities,
            }
            cache.set(cache_key, robot_data, expire=60)

        return robot

    def update_robot(
        self,
        robot_id: int,
        robot_data: RobotUpdate,
    ):
        """Update robot"""

        robot = self.robot_repo.get(robot_id)

        if not robot:
            return None

        update_data = robot_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(robot, field, value)

        self.robot_repo.db.commit()
        self.robot_repo.db.refresh(robot)

        return robot

    def update_robot_status(self, robot_id: int, data: RobotUpdate) -> Robot | None:
        """Update robot information."""

        robot = self.robot_repo.update(robot_id, data)

        if robot:
            cache.delete("all_robots")
            cache.delete(f"robot_{robot_id}")

        return robot

    def delete_robot(self, robot_id: int) -> bool:
        """Delete a robot"""
        result = self.robot_repo.delete(robot_id)

        # Clear the cache after deleting
        if result:
            # Clear outdated cache data after deleting.
            cache.delete("all_robots")
            cache.delete(f"robot_{robot_id}")

        return result
