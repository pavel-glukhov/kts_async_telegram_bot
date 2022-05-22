import asyncio
import os
from dotenv import load_dotenv

from clients.fapi.s3 import S3Client
from clients.tg.api import TgClient

load_dotenv()


async def cli():
    async with TgClient(os.getenv('BOT_TOKEN')) as tg_cli:
        res = await tg_cli.get_me()
        up = await tg_cli.get_updates()
        print(f'getMe: {res}')
        print(f'getUpdates: {up}')


async def s3():
    cr = dict(
        endpoint_url=os.getenv("MINIO_SERVER_URL"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD"),
        aws_access_key_id=os.getenv("MINIO_ROOT_USER")
    )
    s3cli = S3Client(**cr)
    await s3cli.stream_upload(
        'test_bucket',
        'bbabae8bcbce1.mov',
        'https://lms-metaclass-prod.hb.bizmrg.com/media/019c3374-9099-4c49-9037-bbabae8bcbce.mov'
    )


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(cli())
