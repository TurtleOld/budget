import time

from settings import get_result_price, convert_date, convert_time
import asyncio
import json
from aiogram import Bot, Dispatcher, executor, types
import os
from settings_database import cursor
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
admin_id = os.getenv("admin_id")
loop = asyncio.get_event_loop()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot, loop=loop)


# Сообщение для администратора, что бот запущен
async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен!\n")


@dp.message_handler(content_types=['document'])
async def get_receipt(message: types.Message):
    file_info = await bot.get_file(message.document.file_id)
    if file_info.file_id:
        await message.answer("Спасибо, файл добавлен в базу данных!")
    file = await file_info.download("receipt")

    with open(f"{file.name}", 'r', encoding="utf-8", closefd=True) as file_read:
        files = json.load(file_read)

        date_time = files["dateTime"]
        converting_date = convert_date(date_time)
        converting_time = f'{convert_time(date_time)}'
        seller = files['user']
        totalSum = str(get_result_price(files["totalSum"]))

        for item in files["items"]:
            name_product = item["name"]
            price = str(get_result_price(item["price"]))
            quantity = str(item["quantity"])
            amount = str(get_result_price(item["sum"]))

            cursor.execute(
                "INSERT INTO receipt(date_receipt, time_receipt, name_seller, name_product, price, quantity, amount , total_sum) VALUES ('" + converting_date + "', '" + converting_time + "', '" + seller + "', '" + name_product + "', '" + price + "', '" + quantity + "', '" + amount + "', '" + totalSum + "')")

        if not file_read.closed:
            file_read.close()
    path_to_file = "receipt/documents/"
    files = os.listdir(path_to_file)
    for file_r in files:
        os.remove(path_to_file + file_r)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=send_to_admin, skip_updates=True)
