
from sqlalchemy import Boolean, Column, ForeignKey, Integer, LargeBinary, String, Table, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)


class group_user_m2m_table(Base):
    __tablename__ = 'group_user'
    __table_args__ = (
        UniqueConstraint(
            "group_id",
            "user_id",
            name="name_group_user"
        ),
    )
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('groups.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))


class User(Base):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    subscribe: Mapped[bool] = mapped_column(Boolean, default=True)
    
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="owner")
    
    groups: Mapped[list["Group"]] = relationship("Group", secondary='group_user', back_populates="users")
    

class Task(Base):
    __tablename__ = 'tasks'
    
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    priority: Mapped[str] = mapped_column(String, default="low")
    
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"))
    
    owner = relationship("User", back_populates="tasks")
    group: Mapped["Group"] = relationship("Group", back_populates="tasks")
    

class Group(Base):
    __tablename__ = 'groups'
    
    name: Mapped[str] = mapped_column(String)
    
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="group")
    users: Mapped[list["User"]] = relationship("User", secondary='group_user', back_populates="groups")

    
    