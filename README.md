# S3 Bucket Uploader

<a id="content"><h3>Content</h3></a>
- [Short description](#summary)
- [Used technologies](#technologies)
- [Local Install](#local-install)

<a id="summary"><h3>Short description</h3></a>

S3 Bucket Uploader - [Telegram Bot](https://api.telegram.org) for 
asynchronously upload documents to S3 Bucket, using telegram
chat interface. Also provides a list of uploaded files.

Using scenario:
1. In [telegram](https://web.telegram.org/) search @AsyncPythonBot
2. Send command `/start`
3. Upload your document files (24MB max available size for every file)
4. Send command `/files`

[Back](#content)

<a id="technologies"><h3>Used technologies</h3></a>

| Name | Description |
|---|---|
|Python3.10|Programming Language|
|aiohttp|Asynchronous HTTP Client/Server for asyncio and Python|
|aiobotocore|Asynchronous client for Amazon services|
|RabbitMQ(aio_pika)|Message broker implemented AMQP protocol(message orientation, queuing, routing)|
|Postgres|Database|
|Gino|Library for writing and execute raw SQL in asynchronous app with friendly objective API|
|Alembic|Lightweight database migration tool for usage with SQLAlchemy Database Toolkit for Python|
|MongoDB|NoSQL database. Store chat events|
|Motor|Coroutine-based API for non-blocking access to MongoDB|
|Docker/docker compose|Platform for local developing and running app|

[Back](#content)

<a id="local-install"><h3>Local install</h3></a>

Requirements:
- Create [Telegram Bot](https://core.telegram.org/bots)
- Create [Amazon S3 Bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) and add access key in IAM service.
- Create [Mongo cluster](https://www.mongodb.com/docs/atlas/getting-started/) or use local mongo DB 
- Install [Docker and docker compose](https://www.docker.com/products/docker-desktop/) 

Setup App:
1. Add environment variables in `./Dockerfile` 
2. Run `docker compose up -d`

[Back](#content)
