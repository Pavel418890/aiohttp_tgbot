from typing import Optional, TYPE_CHECKING

from aiohttp import ClientSession, StreamReader

from app.base.base_accessor import BaseAccessor
from app.store.tgbot_api.schemas import GetUpdatesResponse, Update, \
    GetFileResponse, File, MessageResponse
from app.store.tgbot_api.poller import Poller

if TYPE_CHECKING:
    from app.web.app import Application


class TelegramBotAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.poller: Optional[Poller] = None
        self.offset = 0
        self.timeout = 25

    async def connect(self, app: "Application"):
        app.logger.info("Starting telegram client")
        self.session = ClientSession()
        bot_conn = await self.get_me()
        if bot_conn["ok"]:
            app.logger.info("{}[{}]: Connected successfully".format(
                bot_conn["result"]["username"], bot_conn["result"]["id"])
            )
        self.poller = Poller(self.app.store)
        await self.poller.start()

    async def disconnect(self, _: "Application"):
        if self.session and not self.session.closed:
            await self.session.close()
        if self.poller and self.poller.is_running:
            await self.poller.stop()

    def get_base_query(self, method: str):
        return self._build_query(
            host="https://api.telegram.org",
            method=method,
            params={
                "bot": self.app.config.tg.token
            }
        )

    @staticmethod
    def _build_query(host: str, method: Optional[str], params: dict) -> str:
        url = host.strip("/") + "/"
        url += "".join([f"{key}{value}" for key, value in params.items()])
        url += "/" + method
        return url

    async def get_me(self) -> dict:
        async with self.session.get(url=self.get_base_query('getMe')) as resp:
            return await resp.json()

    async def get_updates(self) -> Optional[str]:
        async with self.session.get(
                url=self.get_base_query("getUpdates"),
                params={
                    "offset": self.offset,
                    "timeout": self.timeout
                }
        ) as response:
            data = await response.json()
            if data.get("result"):
                self.offset = data["result"][-1]["update_id"] + 1
                return data["result"]

    async def send_message(
            self, chat_id: int, message: str, parse_mode: Optional[str] = None
    ):
        params = None
        if parse_mode:
            params = {"parse_mode": parse_mode}
        async with self.session.post(
                url=self.get_base_query("sendMessage"),
                json={"chat_id": chat_id, "text": message},
                params=params
        ) as response:
            result = await response.text()
            return MessageResponse.Schema().loads(result).result

    async def edit_message(self, chat_id: int, message_id: str, message: str):
        async with self.session.post(
                url=self.get_base_query("editMessageText"),
                json={
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "text": message
                }
        ) as response:
            data = await response.text()
            return MessageResponse.Schema().loads(data).result

    async def get_file(self, file_id: str) -> StreamReader:
        async with self.session.get(
                url=self.get_base_query("getFile"),
                params={
                    "file_id": file_id
                }
        ) as response:
            file_info = await response.json()
            file_url = self._build_query(
                host="https://api.telegram.org",
                method=file_info["result"]["file_path"],
                params={
                    "file": "/",
                    "bot": self.app.config.tg.token,
                }
            )
        response = await self.session.get(file_url)
        return response.content
