# python built-in imports
from dataclasses import dataclass, field
from datetime import date, datetime, time

# python external modules
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, select, func, Date, ForeignKey
from sqlalchemy.orm import registry, relationship

# app imports
from codeapp import db, login_manager

mapper_registry: registry = registry(metadata=db.metadata)


@login_manager.user_loader
def load_user(user_id: int) -> UserMixin:
    stmt = select(User).where(User.id == user_id).limit(1)
    return db.session.execute(stmt).scalars().first()


@mapper_registry.mapped
@dataclass
class User(UserMixin):
    __tablename__ = "user"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(
        init=False,
        metadata={"sa": Column(Integer(), primary_key=True, autoincrement=True)},
    )
    name: str = field(repr=False, metadata={"sa": Column(String(128), nullable=False)})
    email: str = field(
        metadata={"sa": Column(String(128), unique=True, nullable=False)}
    )
    password: str = field(
        repr=False, metadata={"sa": Column(String(128), nullable=False)}
    )
    folders = relationship('Folder', cascade="all,delete")


@mapper_registry.mapped
@dataclass
class Category:
    __tablename__ = "category"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(
        init=False,
        metadata={"sa": Column(Integer(), primary_key=True, autoincrement=True)},
    )
    name: str = field(repr=False, metadata={"sa": Column(String(128), nullable=False)})
    folders = relationship('Folder')


@mapper_registry.mapped
@dataclass
class Folder:
    __tablename__ = "folder"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(
        init=False,
        metadata={"sa": Column(Integer(), primary_key=True, autoincrement=True)},
    )
    name: str = field(repr=False, metadata={"sa": Column(String(128), nullable=False)})
    user_id: int = field(
        metadata={"sa": Column(Integer(), ForeignKey('user.id'))},
    )
    category_id: int = field(
        metadata={"sa": Column(Integer(), ForeignKey('category.id'), nullable=False)},
    )
    notes = relationship('Note', cascade="all,delete")


@mapper_registry.mapped
@dataclass
class Note:
    __tablename__ = "note"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(
        init=False,
        metadata={"sa": Column(Integer(), primary_key=True, autoincrement=True)},
    )
    data: String = field(
        metadata={"sa": Column(String(1000), nullable=False)},
    )
    folder_id: int = field(
        metadata={"sa": Column(Integer, ForeignKey('folder.id'), nullable=False)},
    )
