import hashlib

from pymongo.database import Database

from app.users.models import CreateUser, Login, User


def _hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def create(db: Database, user: CreateUser) -> User:
    if db.users.find_one({"username": user.username}) is not None:
        raise Exception(f"{user.username} is taken")

    result = db.users.insert_one(
        {
            "username": user.username,
            "password": _hash_password(user.password),
        }
    )

    created_user = db.users.find_one({"_id": result.inserted_id})

    return User.model_validate(created_user)


def login(db: Database, login: Login) -> User:
    if (
        user := db.users.find_one(
            {
                "username": login.username,
                "password": _hash_password(login.password),
            }
        )
    ) is None:
        raise Exception("Invalid username or password")

    return User.model_validate(user)
