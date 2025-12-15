from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.groups import GroupCreate
from app.db.models import Group, User



async def create_group(
    group: GroupCreate,
    db: AsyncSession,
    user: User
):
    stmt = (
        select(Group)
        .join(Group.users)
        .where(Group.name == group.name)
    )
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Группа с таким именем уже существует"
        )
    
    db_group = Group(**group.model_dump())
    db_group.users.append(user)
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)
    return {
        "user": user,
        "group": db_group
    }