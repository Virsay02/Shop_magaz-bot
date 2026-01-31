import os
from aiogram import Bot,Dispatcher
import asyncio
import logging
from app.client import client_router
from app.database.models import init_models

from dotenv import load_dotenv
from aiogram.fsm.storage.redis import RedisStorage
import  redis.asyncio as aioredis

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format= "%(asctime)s - %(levelname)s - %(name)s - %(message)s")


async def main():
    bot = Bot(token = os.getenv('TG_TOKEN'))

    redis_host = os.getenv("REDIS_HOST","localhost")
    redis_port = os.getenv("REDIS_PORT","6379")
    redis_db = os.environ["REDIS_DB"]

    redis = await aioredis.from_url(f'redis://{redis_host}:{redis_port}/{redis_db}')
    dp = Dispatcher(storage= RedisStorage(redis))

    dp.include_router(client_router)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)

async def startup(dispatcher):
    await init_models()
    logging.info(" Starting up...")

async def shutdown(dispatcher):
    logging.info("Shutting down...")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Bot stopped')