"""Repositories"""

from typing import Generic, List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from app.core.database import Base


ModelTypeT = TypeVar("ModelTypeT", bound=Base)  # type: ignore
CreateSchemaT = TypeVar("CreateSchemaT")
UpdateSchemaT = TypeVar("UpdateSchemaT")


class BaseRepository(Generic[ModelTypeT, CreateSchemaT, UpdateSchemaT]):
    """Base repository with common CRUD opertaions"""

    def __init__(self, model: Type[ModelTypeT], db: Session):
        self.model = model
        self.db = db

    def get(self, record_id: int) -> Optional[ModelTypeT]:
        """Get entity by ID"""
        return self.db.query(self.model).filter(self.model.id == record_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelTypeT]:
        """Get all entities with pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: CreateSchemaT) -> ModelTypeT:
        """Create new entity"""
        obj_data = obj_in.model_dump(exclude_unset=True)  # type: ignore
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, record_id: int, obj_in: UpdateSchemaT) -> Optional[ModelTypeT]:
        """Update existing entity"""
        db_obj = self.get(record_id)
        if not db_obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)  # type: ignore
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, recodrd_id: int) -> bool:
        """Delete entity by ID"""
        db_obj = self.get(recodrd_id)
        if not db_obj:
            return False
        self.db.delete(db_obj)
        self.db.commit()
        return True

    def exists(self, **kwargs) -> bool:
        """Check if entity exists with given filters"""
        query = self.db.query(self.model)
        for key, value in kwargs.items():
            query = query.filter(getattr(self.model, key) == value)
        return query.count() > 0
