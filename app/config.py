import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    DB_URL: str = os.getenv("DB_URL", "postgresql+asyncpg://user:pass@localhost:5432/shop_bot")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Admin IDs
    ADMIN_IDS: list = None

    def __post_init__(self):
        if self.ADMIN_IDS:
            self.ADMIN_IDS = [int(x) for x in self.ADMIN_IDS.split(',')]


config = Config()