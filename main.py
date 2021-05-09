from settings import *
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
    file = await file_info.download("E:\MyProject\\budget\\receipt")
    print(file)
    file_name = file_info.file_path[10:]
    print(file_name)
    with open(f"receipt/documents/{file_name}", 'r', encoding="utf-8") as file_read:
        files = json.load(file_read)
        print(files)

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
                "INSERT INTO receipt(\"Date\", \"Time\", \"name_seller\", \"name_product\", \"price\", \"quantity\", \"amount\", \"totalSum\") VALUES ('" + converting_date + "', '" + converting_time + "', '" + seller + "', '" + name_product + "', '" + price + "', '" + quantity + "', '" + amount + "', '" + totalSum + "')")
        list_file_name = f"./receipt/{file_info.file_path[:10]}"
        for path in os.listdir(list_file_name):
            os.remove(f"./receipt/documents/{path}")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=send_to_admin, skip_updates=True)
