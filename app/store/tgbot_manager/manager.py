from typing import TYPE_CHECKING, Optional

from aio_pika import IncomingMessage
import prettytable as pt

from app.store.tgbot_api.schemas import Update, Message, Document

if TYPE_CHECKING:
    from app.web.app import Application


class TelegramBotManager:
    def __init__(self, app: "Application"):
        self.app = app

    async def handle_updates(self, message: IncomingMessage):
        self.app.logger.info(f"[{message.message_id}] Starting task ")
        async with message.process():
            update = Update.Schema().loads(message.body.decode())
            existing_user = await self.app.store.pg.get_user(
                update.message.from_.id
            )
            if not existing_user:
                await self._greetings(
                    user_id=update.message.from_.id,
                    user_name=update.message.chat.username
                )
            elif update.message.document:
                await self._upload_to_bucket(
                    file_id=update.message.document.file_id,
                    chat_id=update.message.chat.id,
                    file_name=update.message.document.file_name,
                    file_size=update.message.document.file_size,
                )
            elif update.message.text == "/files":
                return await self._get_files(update.message.chat.id)
            else:
                await self.app.store.tg.send_message(
                    chat_id=update.message.chat.id,
                    message="[Please send me a file]"
                )

        self.app.logger.info(f"[{message.message_id}] Finish task")

    def _create_upload_callback(
            self, chat_id: int, message_id: int, file_name: str, file_size: int
    ):
        async def upload_callback(uploaded_size: float):
            message = "[%s] Processing... %.2fMB/%.2fMB" % (
                file_name,
                uploaded_size,
                file_size / 1024 / 1024
            )
            await self.app.store.tg.edit_message(
                chat_id=chat_id, message_id=message_id, message=message
            )

        return upload_callback

    async def _get_files(self, chat_id: int):
        table = pt.PrettyTable(["Name", "Size", "LastModified"])
        table.align["Name"] = "l"
        table.align["Size"] = "r"
        table.align["LastModified"] = "r"
        contents = await self.app.store.s3.get_files()
        for content in contents:
            table.add_row(
                [
                    content.Key,
                    f"{content.Size / 1024 / 1024:.2f}MB",
                    content.LastModified.strftime("%y-%m-%d %H:%M:%S %Z")
                ]
            )
        return await self.app.store.tg.send_message(
            chat_id, f"<pre>{table}</pre>", parse_mode="HTML"
        )

    async def _greetings(self, user_id: int, user_name: str) -> Message:
        await self.app.store.pg.add_new_user(user_id, user_name)
        await self.app.store.tg.send_message(
            user_id, f"Hello, {user_name}"
        )
        message = await self.app.store.tg.send_message(
            user_id, "[Please send me a file]"
        )
        return message

    async def _upload_to_bucket(
            self,
            file_id: int,
            chat_id: int,
            file_name: str,
            file_size: int,
    ):
        stream_reader = await self.app.store.tg.get_file(file_id=file_id)
        upload = await self.app.store.tg.send_message(
            chat_id=chat_id, message=f"[%s] Starting upload..." % file_name
        )
        upload_chunk_handler = self._create_upload_callback(
            chat_id=chat_id,
            message_id=upload.message_id,
            file_name=file_name,
            file_size=file_size
        )
        response = await self.app.store.s3.upload(
            reader=stream_reader,
            path=file_name,
            upload_callback=upload_chunk_handler
        )
        if response.ResponseMetadata.HTTPStatusCode == 200:
            await self.app.store.tg.edit_message(
                chat_id=chat_id,
                message_id=upload.message_id,
                message="[%s] Uploaded successfully" % file_name
            )
