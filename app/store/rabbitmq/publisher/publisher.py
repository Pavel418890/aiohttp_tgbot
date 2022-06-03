from typing import TYPE_CHECKING

from aio_pika import connect_robust, Message

if TYPE_CHECKING:
    from app.web.app import Application


class RabbitPublisher:
    def __init__(self, app: "Application"):
        self.app = app

    async def put(self, update: str):
        conn = await connect_robust(self.app.config.rabbit.url)
        async with conn:
            channel = await conn.channel()
            await channel.default_exchange.publish(
                Message(f"{update}".encode()),
                routing_key=self.app.config.rabbit.queue_name
            )
            self.app.logger.info(
                f"[{self.__class__.__name__}]:Publisher send message"
            )
