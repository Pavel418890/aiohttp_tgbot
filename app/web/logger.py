import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.web.app import Application


def setup_logging(_: "Application"):
    logging.basicConfig(level=logging.INFO)