import asyncio
import os
from dotenv import load_dotenv

from clients.fapi.s3 import S3Client
from clients.tg.api import TgClient
from clients.lms.api import LmsClient
from clients.fapi.tg import TgClientWithFile

load_dotenv()


async def cli():
    async with TgClient(os.getenv('BOT_TOKEN')) as tg_cli:
        pass
    # res = await tg_cli.get_me()
    # up = await tg_cli.get_updates()
    #     print(f'getMe: {res}')
    #     await tg_cli.send_message(
    #         chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='test')
    #
    # async with LmsClient(os.getenv('LMS_TOKEN')) as lms_cli:
    #     await lms_cli.get_user_current()
    #     await lms_cli.login(email=os.getenv('EMAIL'),
    #                         password=os.getenv('PASSWORD'))

    dist_p = os.path.abspath(os.curdir)
    async with TgClientWithFile(os.getenv('BOT_TOKEN')) as tg_cli:
        data = await tg_cli.get_file('BQACAgIAAxkBAAIQbmKMpg3tT67j83WmQzc4zq5e6xxVAAKcGQAC7GVhSAyFIUETi_HyJAQ')
        await tg_cli.download_file(file_path=data.file_path, destination_path=dist_p)
        file = os.path.join(dist_p, 'documents\\1.txt')
        await tg_cli.send_document(document_path=file, chat_id=os.getenv('TELEGRAM_CHAT_ID'))


async def s3():
    cr = dict(
        endpoint_url=os.getenv("MINIO_SERVER_URL"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD"),
        aws_access_key_id=os.getenv("MINIO_ROOT_USER")
    )
    s3cli = S3Client(**cr)

    await s3cli.stream_upload(
        'test',
        'bbab2323.mov',
        'https://lms-metaclass-prod.hb.bizmrg.com/media/019c3374-9099-4c49-9037-bbabae8bcbce.mov'
    )


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(s3())
