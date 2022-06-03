from typing import TYPE_CHECKING

from app.base.base_accessor import BaseAccessor
from app.store.postgres.gino import db
from app.store.postgres.models import User

if TYPE_CHECKING:
    from app.web.app import Application


class PostgresAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)

    async def connect(self, app: "Application"):
        await db.set_bind(bind=app.config.pg.url)
        self.app.logger.info("Connected to postgres db")
        await db.gino.create_all()

    async def add_new_user(self, user_id: int, user_name: str):
        await User.create(id=user_id, username=user_name)

    async def get_user(self, user_id: int) -> User:
        return await User.get(user_id)

    async def disconnect(self, app: "Application"):
        await db.pop_bind().close()
        self.app.logger.info("Postgres disconnected")
