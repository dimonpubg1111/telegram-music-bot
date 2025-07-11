import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, FSInputFile
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
import yt_dlp

API_TOKEN = '7736223243:AAHYINkXsaXTxTmrLlFnwEnl7dQmweL1fMY'

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("🎵 Привет! Напиши название песни, и я пришлю тебе mp3-файл.")

@dp.message()
async def download_music(message: Message):
    query = message.text.strip()
    await message.answer(f"🔍 Ищу: {query}...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '64',
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            video = info['entries'][0]
            title = video['title']
            filename = title + ".mp3"

        await message.answer(f"🎶 Готово! Отправляю <b>{title}</b>...")

        audio = FSInputFile(path=filename)
        await message.answer_audio(audio=audio, title=title)

        os.remove(filename)
    except Exception as e:
        await message.answer("⚠️ Не удалось скачать музыку. Попробуй другое название.")
        print(f"Ошибка: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
