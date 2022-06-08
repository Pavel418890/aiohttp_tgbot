from typing import TYPE_CHECKING
from logging import getLogger

if TYPE_CHECKING:
    from app.web.app import Application


class BaseAccessor:
    def __init__(self, app: "Application", *args, **kwargs):
        self.app = app
        self.logger = getLogger("accessor")
        app.on_startup.append(self.connect)
        app.on_shutdown.append(self.disconnect)

    async def connect(self, app: "Application"):
        raise NotImplemented

    async def disconnect(self, app: "Application"):
        raise NotImplemented
