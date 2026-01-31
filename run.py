import os
from aiogram import Bot,Dispatcher
import asyncio
import logging
from app.client import client_router
from app.database.models import init_models

from aiogram.fsm.storage.redis import RedisStorage
import  redis.asyncio as aioredis



logging.basicConfig(level=logging.INFO,
                    format= "%(asctime)s - %(levelname)s - %(name)s - %(message)s")


async def main():
    import os
    import aioredis
    from aiogram import Bot, Dispatcher
    from aiogram.fsm.storage.redis import RedisStorage

    from app.client import client_router
    from app.utils.lifecycle import startup, shutdown  # если у тебя так

    async def main():
        # === TG TOKEN ===
        TG_TOKEN = os.getenv("TG_TOKEN")
        if not TG_TOKEN:
            raise RuntimeError("TG_TOKEN is not set")

        bot = Bot(token=TG_TOKEN)

        # === REDIS ===
        redis_host = os.getenv("REDIS_HOST")
        if not redis_host:
            raise RuntimeError("REDIS_HOST is not set")

        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_db = int(os.getenv("REDIS_DB", 0))

        redis = await aioredis.from_url(
            f"redis://{redis_host}:{redis_port}/{redis_db}"
        )

        storage = RedisStorage(redis)

        # === DISPATCHER ===
        dp = Dispatcher(storage=storage)

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