import pytest
from testcontainers.mongodb import MongoDbContainer

from app.users import service
from app.users.models import CreateUser, Login


@pytest.fixture(scope="module")
def db():
    with MongoDbContainer("mongodb/mongodb-community-server:7.0.0-ubuntu2204") as mongo:
        client = mongo.get_connection_client()
        yield client["test"]


def test_create(db):
    user = CreateUser(
        username="meir",
        password="123456",
    )

    assert service.create(db, user).username == user.username

    with pytest.raises(Exception, match=f"{user.username} is taken"):
        assert service.create(db, user).username


def test_login(db):
    login = Login(username="meir", password="11111")

    with pytest.raises(Exception, match="Invalid username or password"):
        assert service.login(db, login)

    login = Login(username="meir", password="123456")

    assert service.login(db, login)
