from os import getenv
from dotenv import load_dotenv
from aiogram import Dispatcher


load_dotenv()

dp = Dispatcher()
TOKEN = getenv("BOT_TOKEN")



