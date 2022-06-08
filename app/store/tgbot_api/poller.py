import asyncio
import json
from typing import Optional

from app.store import Store


class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_task: Optional[asyncio.Task] = None

    async def start(self):
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self):
        if self.is_running and self.poll_task:
            self.is_running = False
            await self.poll_task

    async def poll(self):
        while self.is_running:
            updates = await self.store.tg.get_updates()
            if updates:
                for update in updates:
                    json_update = json.dumps(update)
                    await self.store.logger_publisher.info(json_update)
                    await self.store.rabbit_publisher.put(json_update)
