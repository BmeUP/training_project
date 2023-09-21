import pytest
from sqlalchemy import select

from src.db.models.user import User

@pytest.mark.asyncio
async def test_create_user(get_session):
    async with get_session() as session:
        user = User(name="TestUserDB", email="testdb@user.com", phone="77777777777", password="test_password")
        session.add(user)
        await session.commit()

@pytest.mark.asyncio
async def test_select_user(get_session):
    stmt = select(User).where(User.name == "TestUserDB")
    async with get_session() as session:
        result = await session.execute(stmt)
        test_user = result.scalars(stmt).one()
    assert test_user.phone == "77777777777"
    assert test_user.phone != "777777777"
    assert test_user.email == "testdb@user.com"