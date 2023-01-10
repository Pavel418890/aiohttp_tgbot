from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

import yaml

if TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class TGBotConfig:
    token: str


@dataclass
class RabbitConfig:
    url: str
    queue_name: str
    capacity: int


@dataclass
class S3Config:
    service_name: str
    bucket: str


@dataclass
class PostgresConfig:
    url: str


@dataclass
class MongoConfig:
    url: str


@dataclass
class Config:
    tg: TGBotConfig
    rabbit: RabbitConfig
    s3: S3Config
    pg: PostgresConfig
    mongo: MongoConfig


def setup_config(app: "Application", config_path: str):
    with open(config_path) as f:
        raw_config = yaml.safe_load(f)
    app.config = Config(
        tg=TGBotConfig(token=raw_config["telegram"]["bot_token"]),
        rabbit=RabbitConfig(
            url=raw_config["rabbit"]["cloudamqp"],
            queue_name=raw_config["rabbit"]["queue_name"],
            capacity=raw_config["rabbit"]["capacity"]
        ),
        s3=S3Config(
            service_name=raw_config["s3"]["service_name"],
            bucket=raw_config["s3"]["bucket_name"],
        ),
        pg=PostgresConfig(
            url=raw_config["postgres"]["database_url"],
        ),
        mongo=MongoConfig(
            url=raw_config["mongo"]["mongo_url"],
        )
    )
