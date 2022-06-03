from typing import Optional

from aiohttp import web

from app.web.config import setup_config
from app.web.logger import setup_logging
from app.web.config import Config
from app.store import Store, setup_store


class Application(web.Application):
    config: Optional[Config] = None
    store: Optional[Store] = None


app = Application()


def setup_app(config_path: str) -> Application:
    setup_logging(app)
    setup_config(app, config_path)
    setup_store(app)
    return app
