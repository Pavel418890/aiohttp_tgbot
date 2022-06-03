import asyncio
import json
from typing import TYPE_CHECKING, Optional

import aio_pika
import bson

from app.base.base_accessor import BaseAccessor
from app.store.tgbot_api.schemas import Update

if TYPE_CHECKING:
    from app.web.app import Application


class Logger(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.conn: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.RobustChannel] = None
        self._logger_task: Optional[asyncio.Task] = None
        self.exchange: Optional[aio_pika.Exchange] = None

    async def connect(self, app: "Application"):
        self.conn = await aio_pika.connect_robust(self.app.config.rabbit.url)
        self.channel = await self.conn.channel()
        self.exchange = await self.channel.declare_exchange(
            name="logs",
            type=aio_pika.ExchangeType.DIRECT
        )
        await self.start()

    async def disconnect(self, app: "Application"):
        if self.conn and self.channel and not self._logger_task.done():
            await self.channel.close()
            await self.conn.close()

    async def start(self):
        queue = await self.channel.declare_queue(exclusive=True)
        await queue.bind(self.exchange, routing_key="info")
        await queue.bind(self.exchange, routing_key="critical")
        self._logger_task = asyncio.create_task(
            queue.consume(self.log_handler)
        )

    async def log_handler(self, message: aio_pika.abc.AbstractIncomingMessage):
        logs_levels = {
            "info": self.handle_info,
            "debug": self.handle_debug,
            "critical": self.handle_critical
        }
        async with message.process():
            handler = logs_levels.get(message.routing_key)
            if handler:
                await handler(data=message)

    async def handle_info(self, data: aio_pika.abc.AbstractIncomingMessage):
        raise NotImplemented

    async def handle_debug(self, data: aio_pika.abc.AbstractIncomingMessage):
        raise NotImplemented

    async def handle_critical(self, data: aio_pika.abc.AbstractIncomingMessage):
        raise NotImplemented


class BotLogger(Logger):
    async def handle_info(self, data: aio_pika.abc.AbstractIncomingMessage):
        update = json.loads(data.body.decode())
        await self.app.store.mongo.insert_update_object(update)

