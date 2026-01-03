# app/telegram/client.py
from aiogram import Bot
from app.config import settings

bot = Bot(token=settings.telegram_bot_token)
