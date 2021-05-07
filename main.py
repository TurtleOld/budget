from nalog_python import result_receipt as ticket
from settings import *
import json


date_time = ticket()["ticket"]["document"]["receipt"]["dateTime"]
print(f"Дата продажи: {convert_date(date_time)}")
print(f"Время продажи: {convert_time(date_time)}")
for item in ticket()["ticket"]["document"]["receipt"]["items"]:
    print(f"Название: {item['name']} Цена: {get_result_price(item['price'])}, "
          f"Количество: {item['quantity']}, Сумма: {get_result_price(item['sum'])}")
totalSum = ticket()["ticket"]["document"]["receipt"]["totalSum"]
print(f"Итог по чеку: {get_result_price(totalSum)}")
company = ticket()["ticket"]["document"]["receipt"]["user"]
print(f"Компания: {company}")


ticket()
