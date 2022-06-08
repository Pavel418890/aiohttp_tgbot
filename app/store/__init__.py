from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from app.store.rabbitmq.logger.accessor import BotLogger
        from app.store.tgbot_api.accessor import TelegramBotAccessor
        from app.store.rabbitmq.consumer.accessor import RabbitAccessor
        from app.store.tgbot_manager.manager import TelegramBotManager
        from app.store.rabbitmq.publisher.publisher import RabbitPublisher
        from app.store.s3.accessor import S3Accessor
        from app.store.postgres.accessor import PostgresAccessor
        from app.store.mongo.accessor import MongoAccessor
        from app.store.rabbitmq.publisher.logger import LoggerPublisher

        self.tg = TelegramBotAccessor(app)
        self.rabbit_publisher = RabbitPublisher(app)
        self.rabbit_consumer = RabbitAccessor(app)
        self.tg_bot_manager = TelegramBotManager(app)
        self.s3 = S3Accessor(app)
        self.pg = PostgresAccessor(app)
        self.mongo = MongoAccessor(app)
        self.bot_logger = BotLogger(app)
        self.logger_publisher = LoggerPublisher(app)


def setup_store(app: "Application"):
    app.store = Store(app)
