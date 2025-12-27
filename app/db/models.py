from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, LargeBinary, String, Table, UniqueConstraint, Enum as SAEnum, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.enums import GlobalRoleEnum, GroupRoleEnum, PriorityEnum

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)


class GroupUserAssociation(Base):
    __tablename__ = 'group_user'
    __table_args__ = (
        UniqueConstraint(
            "group_id",
            "user_id",
            name="name_group_user"
        ),
    )
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    
    role_in_group: Mapped[GroupRoleEnum] = mapped_column(SAEnum(GroupRoleEnum), default=GroupRoleEnum.MEMBER)
    
    group: Mapped["Group"] = relationship("Group", back_populates="user_associations")
    user: Mapped["User"] = relationship("User", back_populates="group_associations")
    


class User(Base):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    subscribe: Mapped[bool] = mapped_column(Boolean, default=True)
    last_active_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )
    global_role: Mapped[GlobalRoleEnum] = mapped_column(SAEnum(GlobalRoleEnum), default=GlobalRoleEnum.USER)
    
    
    tasks: Mapped[list["Task"]] = relationship(
        "Task", 
        back_populates="owner", 
        foreign_keys="Task.owner_id",
    )
    assigned_tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="for_user", 
        foreign_keys="Task.for_user_id"
    )
    group_associations: Mapped[list["GroupUserAssociation"]] = relationship(
        "GroupUserAssociation", 
        back_populates="user",
    )
    created_groups: Mapped[list["Group"]] = relationship(
        "Group", 
        back_populates="creator",
        foreign_keys="Group.creator_id"
    )
    

class Task(Base):
    __tablename__ = 'tasks'
    
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    priority: Mapped[PriorityEnum] = mapped_column(SAEnum(PriorityEnum), default=PriorityEnum.LOW)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )
    
    owner_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    for_user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id", ondelete="CASCADE"))
    
    
    for_user: Mapped["User | None"] = relationship("User", back_populates="assigned_tasks", foreign_keys=[for_user_id])
    owner: Mapped["User | None"] = relationship("User", back_populates="tasks", foreign_keys=[owner_id])
    group: Mapped["Group"] = relationship("Group", back_populates="tasks")
    

class Group(Base):
    __tablename__ = 'groups'
    
    name: Mapped[str] = mapped_column(String)
    creator_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    
    tasks: Mapped[list["Task"]] = relationship(
        "Task", 
        back_populates="group",
    )
    user_associations: Mapped[list["GroupUserAssociation"]] = relationship(
        "GroupUserAssociation", 
        back_populates="group",
    )
    creator: Mapped["User | None"] = relationship(
        "User", 
        back_populates="created_groups",
        foreign_keys=[creator_id]
    )

    
    