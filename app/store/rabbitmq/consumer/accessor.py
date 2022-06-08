import asyncio
from typing import TYPE_CHECKING, Optional

import aio_pika
from app.base.base_accessor import BaseAccessor

if TYPE_CHECKING:
    from app.web.app import Application


class RabbitAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self._consumer_task: Optional[asyncio.Task] = None
        self.conn: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.RobustChannel] = None

    async def connect(self, app: "Application"):
        self.conn = await aio_pika.connect_robust(app.config.rabbit.url)
        self.channel = await self.conn.channel()
        await self.channel.set_qos(prefetch_count=app.config.rabbit.capacity)
        await self.start()

    async def start(self):
        queue = await self.channel.declare_queue(
            self.app.config.rabbit.queue_name,
            durable=True
        )
        self.app.logger.info("Starting rabbit consumer")
        self._consumer_task = asyncio.create_task(queue.consume(
            self.app.store.tg_bot_manager.handle_updates
        ))

    async def disconnect(self, app: "Application"):
        if self._consumer_task and not self._consumer_task.done():
            await self._consumer_task
        await self.channel.close()
        await self.conn.close()
