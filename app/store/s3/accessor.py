from pprint import pprint
from typing import TYPE_CHECKING, Optional

from aiobotocore.session import get_session, AioSession
from aiohttp import StreamReader, web

from app.base.base_accessor import BaseAccessor
from app.store.s3.multipart_uploader import MultipartUploader
from app.store.s3.schemas import ListFilesResponse, Content
from app.utils.part_iterator import reader_iterator

if TYPE_CHECKING:
    from app.web.app import Application


class S3Accessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self._session: AioSession = get_session()

    async def connect(self, app: "Application"):
        async with self._session.create_client(
                service_name=app.config.s3.service_name,
                region_name=app.config.s3.region_name,
                aws_access_key_id=app.config.s3.aws_access_key,
                aws_secret_access_key=app.config.s3.aws_secret_key
        ) as s3:
            response = await s3.list_buckets()
            is_present = False
            if response:
                available_buckets = response["Buckets"]
                for bucket in available_buckets:
                    if bucket["Name"] == app.config.s3.bucket:
                        is_present = True
                        break
                if not is_present:
                    raise web.HTTPInternalServerError
            else:
                raise web.HTTPInternalServerError

    async def get_files(self) -> list[Content]:
        async with self._session.create_client(
                service_name=self.app.config.s3.service_name,
                region_name=self.app.config.s3.region_name,
                aws_access_key_id=self.app.config.s3.aws_access_key,
                aws_secret_access_key=self.app.config.s3.aws_secret_key
        ) as s3:
            paginator = s3.get_paginator('list_objects')
            async for result in paginator.paginate(
                    Bucket=self.app.config.s3.bucket
            ):
                response = ListFilesResponse.Schema().load(result)
                return response.Contents

    async def upload(
            self,
            path: str,
            reader: StreamReader,
            upload_callback: Optional[callable]
    ):
        async with self._session.create_client(
                service_name=self.app.config.s3.service_name,
                region_name=self.app.config.s3.region_name,
                aws_access_key_id=self.app.config.s3.aws_access_key,
                aws_secret_access_key=self.app.config.s3.aws_secret_key
        ) as s3:
            async with MultipartUploader(
                    client=s3,
                    bucket=self.app.config.s3.bucket,
                    key=path
            ) as mpu:
                async for chunk in reader_iterator(reader):
                    await mpu.upload_part(chunk)
                    if upload_callback:
                        await upload_callback(mpu.uploaded_size)

            return mpu.result
