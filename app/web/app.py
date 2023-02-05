import asyncio

import uvloop
from aiohttp import web

from app.web.config import setup_config
from app.web.logger import setup_logging
from app.web.config import Config
from app.store import Store, setup_store


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Application(web.Application):
    config: Config
    store: Store


app = Application()


def setup_app(config_path: str) -> Application:
    setup_logging(app)
    setup_config(app, config_path)
    setup_store(app)
    return app
