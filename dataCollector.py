import requests
from datetime import date, timedelta
import time
import json

url = "https://ads-api.ru/main/api"

headers = {
    "Content-Type": "application/json"
}

def log_request():
    with open('logs.txt', 'a') as f:
        f.write(f"{payload['date1']} → {payload['date2']}: {response.status_code}" + '\n')

def send_request(current_date, next_date, city):
    global payload, response
    try:
        payload = {
            "user": "andreas1901@mail.ru",
            "token": "e65f5a1b45f72d805fb59ad2ad7c5085",
            "date1": str(current_date),
            "date2": str(next_date),
            "city": city,
            "nedvigimost_type": "1, 2",
            "category_id": 7,
            "source": "1,3,4,11,6"
        }

        response = requests.get(url, headers=headers, params=payload)
        log_request()

        if response.status_code == 200:
            with open(fileName, "a", encoding='utf-8') as f:
                json.dump(response.json(), f, ensure_ascii=False)
                f.write("\n")
        else:
            print("Ошибка:", response.text)

        time.sleep(5)

    except Exception as e:
        print(f"Ошибка на {year}-{month}-{day1}–{day2}: {e}")

# cities = [
#     "Москва", "Санкт-Петербург", "Севастополь", "Адыгея", "Алтай", "Алтайский край", "Амурская область",
#     "Архангельская область", "Астраханская область", "Башкортостан", "Белгородская область", "Брянская область",
#     "Бурятия", "Владимирская область", "Волгоградская область", "Вологодская область", "Воронежская область",
#     "Дагестан", "Еврейская автономная область", "Забайкальский край", "Ивановская область", "Ингушетия",
#     "Иркутская область", "Кабардино-Балкария", "Калининградская область", "Калмыкия", "Калужская область",
#     "Камчатский край", "Карачаево-Черкесия", "Карелия", "Кемеровская область", "Кировская область", "Коми",
#     "Костромская область", "Краснодарский край", "Красноярский край", "Крым", "Курганская область",
#     "Курская область", "Ленинградская область", "Липецкая область", "Магаданская область", "Марий Эл", "Мордовия",
#     "Московская область", "Мурманская область", "Нижегородская область", "Новгородская область",
#     "Новосибирская область", "Омская область", "Оренбургская область", "Орловская область", "Пензенская область",
#     "Пермский край", "Приморский край", "Псковская область", "Ростовская область", "Рязанская область",
#     "Самарская область", "Саратовская область", "Саха (Якутия)", "Сахалинская область", "Свердловская область",
#     "Северная Осетия", "Смоленская область", "Ставропольский край", "Тамбовская область", "Татарстан",
#     "Тверская область", "Томская область", "Тульская область", "Тыва", "Тюменская область", "Удмуртия",
#     "Ульяновская область", "Хабаровский край", "Хакасия", "Ханты-Мансийский АО", "Челябинская область",
#     "Чеченская Республика", "Чувашия", "Чукотский АО", "Ямало-Ненецкий АО", "Ярославская область"
# ]

# city = cities[0]
# fileName = city + ".json"
# start_date = date(2025, 3, 1)
# end_date = date.today() - timedelta(days=1)  # вчерашняя дата
#
# current_date = start_date
#
# while current_date <= end_date:
#     next_date = current_date + timedelta(days=4)  # интервал по 5 дней
#     if next_date > end_date:
#         next_date = end_date
#
#     send_request(current_date, next_date, city)
#
#     current_date = next_date + timedelta(days=1)

# cities = [
#     "Москва",
#     "Санкт-Петербург",
#     "Новосибирская область",
#     "Свердловская область",         # Екатеринбург
#     "Татарстан",                    # Казань
#     "Челябинская область",
#     "Красноярский край",
#     "Башкортостан",                 # Уфа
#     "Ростовская область",
#     "Самарская область"
#     # "Пермский край",
#     # "Воронежская область",
#     # "Волгоградская область",
#     # "Краснодарский край",
#     # "Саратовская область",
#     # "Тюменская область",
#     # "Иркутская область",
#     # "Кемеровская область",
#     # "Нижегородская область",
#     # "Омская область"
# ]

cities = ["Санкт-Петербург"]

for city in cities:
    year = 2025
    fileName = city + "_" + str(year) + ".json"

    if year == 2025:
        start_date = date(year, 1, 1)
        end_date = date.today() - timedelta(days=1)
    elif year == 2022:
        start_date = date(year, 3, 1)
        end_date = date(year, 12, 31)
    else:
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)


    current_date = start_date

    while current_date <= end_date:
        next_date = current_date + timedelta(days=4)  # интервал по 5 дней
        if next_date > end_date:
            next_date = end_date

        send_request(current_date, next_date, city)

        current_date = next_date + timedelta(days=1)
