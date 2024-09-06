import os
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Вставьте сюда ваш токен Telegram-бота
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
# Вставьте сюда ваш API-ключ OpenWeatherMap
WEATHER_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("weather_bot.log"),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    logger.info("Received /start command")
    await message.reply("Привет! Напиши мне название города, и я пришлю сводку погоды.")

@dp.message_handler()
async def get_weather(message: types.Message):
    city = message.text
    logger.info(f"Received city name: {city}")
    weather = fetch_weather(city)
    if weather:
        await message.reply(weather)
        logger.info(f"Sent weather info for {city}")
    else:
        await message.reply("Не удалось получить данные о погоде. Проверьте название города и попробуйте снова.")
        logger.error(f"Failed to get weather for {city}")

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"Погода в {city}: {weather_description}, температура: {temperature}°C"
    else:
        logger.error(f"Error fetching weather data: {response.status_code}")
        return None

if __name__ == '__main__':
    logger.info("Starting bot")
    executor.start_polling(dp)
