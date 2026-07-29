"""Robot Repository"""

from typing import Optional, List, TypeVar
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.robot import Robot
from app.schemas.robot import RobotCreate, RobotUpdate
from app.repositories.base import BaseRepository
from app.core.database import Base

ModelTypeT = TypeVar("ModelTypeT", bound=Base)  # type: ignore


class RobotRepository(BaseRepository[Robot, RobotCreate, RobotUpdate]):
    """Repository for Robot entity"""

    def __init__(self, db: Session):
        super().__init__(Robot, db)

    def get_by_serial_number(self, serial_number: str) -> Optional[Robot]:
        """Get robot by serial number"""
        sql = text("SELECT * FROM robots WHERE serial_number = :serial_number")

        row = self.db.execute(sql, {"serial_number": serial_number}).mappings().first()
        if not row:
            return None
        return self._row_to_model(row)  # type: ignore

    def get_by_status(self, status: str) -> List[Robot]:
        """Get robots by status"""
        sql = text("SELECT * FROM robots WHERE status = :status")

        rows = self.db.execute(sql, {"status": status}).mappings().all()
        return [self._row_to_model(row) for row in rows]

    def _row_to_model(self, row) -> ModelTypeT:  # type: ignore
        """Convert a raw SQL row (mapping) back to a SQLAlchemy model instance"""
        obj = self.model(**dict(row))
        # Mark as "persistent" so SQLAlchemy knows it exists in DB
        self.db.enable_relationship_loading(obj)
        return obj
