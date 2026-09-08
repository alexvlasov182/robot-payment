"""Repositories module."""

from typing import Any, TypeVar, cast

from sqlalchemy.orm import Session

from app.core.database import Base

ModelTypeT = TypeVar("ModelTypeT", bound=Base)
CreateSchemaT = TypeVar("CreateSchemaT")
UpdateSchemaT = TypeVar("UpdateSchemaT")


class BaseRepository[ModelTypeT, CreateSchemaT, UpdateSchemaT]:
    """Base repository with common CRUD operations."""

    def __init__(
        self,
        model: type[ModelTypeT],
        db: Session,
    ) -> None:
        self.model = model
        self.db = db

    def get(
        self,
        record_id: int,
    ) -> ModelTypeT | None:
        """Get entity by ID."""

        model = cast(Any, self.model)

        return self.db.query(self.model).filter(model.id == record_id).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ModelTypeT]:
        """Get all entities."""

        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(
        self,
        obj_in: CreateSchemaT,
    ) -> ModelTypeT:
        """Create entity."""

        obj_data = obj_in.model_dump(exclude_unset=True)  # type: ignore[attr-defined]

        db_obj = self.model(**obj_data)

        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)

        return db_obj

    def update(
        self,
        record_id: int,
        obj_in: UpdateSchemaT,
    ) -> ModelTypeT | None:
        """Update entity."""

        db_obj = self.get(record_id)

        if db_obj is None:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)  # type: ignore[attr-defined]

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.db.commit()
        self.db.refresh(db_obj)

        return db_obj

    def delete(
        self,
        record_id: int,
    ) -> bool:
        """Delete entity."""

        db_obj = self.get(record_id)

        if db_obj is None:
            return False

        self.db.delete(db_obj)
        self.db.commit()

        return True

    def exists(
        self,
        **kwargs: Any,
    ) -> bool:
        """Check if entity exists."""

        query = self.db.query(self.model)

        for key, value in kwargs.items():
            query = query.filter(getattr(self.model, key) == value)

        return query.count() > 0
