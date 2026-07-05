"""Repository base class"""
from typing import TypeVar, Generic, Type, List, Optional, Any
from sqlalchemy.orm import Session
from uuid import UUID

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations"""

    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def create(self, obj_in: dict) -> T:
        """Create a new record"""
        db_obj = self.model(**obj_in)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def get(self, id: UUID) -> Optional[T]:
        """Get record by ID"""
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all records with pagination"""
        return self.session.query(self.model).offset(skip).limit(limit).all()

    def update(self, id: UUID, obj_in: dict) -> Optional[T]:
        """Update a record"""
        db_obj = self.get(id)
        if not db_obj:
            return None
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, id: UUID) -> bool:
        """Delete a record"""
        db_obj = self.get(id)
        if not db_obj:
            return False
        self.session.delete(db_obj)
        self.session.commit()
        return True

    def count(self) -> int:
        """Get total count of records"""
        return self.session.query(self.model).count()
