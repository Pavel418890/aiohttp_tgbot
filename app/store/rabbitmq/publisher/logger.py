from typing import TYPE_CHECKING

import aio_pika

if TYPE_CHECKING:
    from app.web.app import Application


class LoggerPublisher:
    def __init__(self, app: "Application"):
        self.app = app

    async def info(self, message: str):
        conn = await aio_pika.connect_robust(self.app.config.rabbit.url)
        async with conn:
            channel = await conn.channel()
            logs_exchange = await channel.declare_exchange("logs")
            await logs_exchange.publish(
                message=aio_pika.Message(f'{message}'.encode()),
                routing_key="info"
            )
            self.app.logger.info("Logger publisher send message")