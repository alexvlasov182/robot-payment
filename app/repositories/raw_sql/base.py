"""Repositories"""

from typing import Generic, TypeVar

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import Base

ModelTypeT = TypeVar("ModelTypeT", bound=Base)  # type: ignore
CreateSchemaT = TypeVar("CreateSchemaT")
UpdateSchemaT = TypeVar("UpdateSchemaT")


class BaseRepository(Generic[ModelTypeT, CreateSchemaT, UpdateSchemaT]):
    """Base repository with common CRUD operations (raw SQL version)"""

    def __init__(self, model: type[ModelTypeT], db: Session) -> None:
        self.model = model
        self.db = db

        # Get the actual table name from the model, e.g. "robots", "users"
        self.table = model.__tablename__

    def get(self, record_id: int) -> ModelTypeT | None:
        """Get entity by ID"""
        sql = text(f"SELECT * FROM {self.table} WHERE id = :id")
        row = self.db.execute(sql, {"id": record_id}).mappings().first()
        if not row:
            return None
        return self._row_to_model(row)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelTypeT]:
        """Get all entities with pagination"""
        sql = text(f"SELECT * FROM {self.table} OFFSET :skip LIMIT :limit")
        rows = self.db.execute(sql, {"skip": skip, "limit": limit}).mappings().all()

        return [self._row_to_model(row) for row in rows]

    def create(self, obj_in: CreateSchemaT) -> ModelTypeT:
        """Create new entity"""
        obj_data = obj_in.model_dump(exclude_unset=True)  # type: ignore

        columns = ", ".join(obj_data.keys())  # "name, status, serial_number"
        placeholders = ", ".join(
            f":{k}" for k in obj_data.keys()
        )  # ":name, :status, :serial_number"

        sql = text(
            f"INSERT INTO {self.table ({columns})} "
            f"VALUES ({placeholders}) "
            f"RETURNING *"
        )
        row = self.db.execute(sql, obj_data).mappings().first()
        self.db.commit()
        return self._row_to_model(row)

    def update(self, record_id: int, obj_in: UpdateSchemaT) -> ModelTypeT | None:
        """Update existing entity"""
        update_data = obj_in.model_dump(exclude_unset=True)  # type: ignore
        if not update_data:
            return self.get(record_id)

        # Build: "name = :name, status = :status"
        set_clause = ", ".join(f"{k} = :{k}" for k in update_data.keys())

        sql = text(
            f"Update {self.table} "
            f"SET {set_clause} "
            f"WHERE id = :id "
            f"RETURNING *"
        )
        update_data["id"] = record_id
        row = self.db.execute(sql, update_data).mappings().first()
        if not row:
            return None
        self.db.commit()
        return self._row_to_model(row)

    def delete(self, record_id: int) -> bool:
        """Delete entity by ID"""
        sql = text(f"DELETE FROM {self.table} WHERE id = :id RETURNING id")
        row = self.db.execute(sql, {"id": record_id}).first()
        self.db.commit()
        return row is not None

    def exists(self, **kwargs) -> bool:
        """Check if entity exists with given filters"""
        # Build "name = :name AND status = :status"
        where_clause = " AND ".join(f"{k} = :{k}" for k in kwargs)
        sql = text(f"SELECT 1 FROM {self.table} WHERE {where_clause} LIMIT 1")
        row = self.db.execute(sql, kwargs).first()
        return row is not None

    def _row_to_model(self, row) -> ModelTypeT:
        """Convert a raw SQL row (mapping) back to a SQLAlchemy model instance"""
        obj = self.model(**dict(row))
        # Mark as "persistent" so SQLAlchemy knows it exists in DB
        self.db.enable_relationship_loading(obj)
        return obj
