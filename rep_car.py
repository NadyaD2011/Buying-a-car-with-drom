import os
import requests
import time
from bs4 import BeautifulSoup


def make_request(url, params=None, max_retries=3, delay=2):
    """Посылает запрос и повторяет при неудаче."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Ошибка запроса: {e}. Попытка {attempt + 1} из {max_retries}")
            time.sleep(delay)
    raise requests.RequestException(
        f"Не удалось получить ответ от {url} после {max_retries} попыток."
    )


def parse_car_brands():
    car_brands = []
    car_links = []
    url = "https://auto.drom.ru/"

    response = make_request(url)
    soup = BeautifulSoup(response.text, "html.parser")
    car_elements = soup.find_all(class_="css-m7q1zs e4ojbx42")

    for element in car_elements:
        car_name = element.find("span", class_="css-1kb7l9z e162wx9x0").text.strip()
        car_link = element.find("a", class_="css-1q66we5 e4ojbx43")["href"]
        car_brands.append(car_name)
        car_links.append(car_link)

    return car_brands[:5], car_links[:5]


def parse_car_details(base_url):
    car_details_list = []
    page = 1  # Начальная страница

    # Создаем папку media, если её нет
    if not os.path.exists("media"):
        os.makedirs("media")

    while True:
        params = {"ph": 1, "unsold": 1}  # Только с фото  # Только не проданные
        url = f"{base_url}/all/page{page}/"  # Форматируем URL с page
        response = make_request(url, params=params)
        soup = BeautifulSoup(response.text, "html.parser")

        car_cards = soup.find_all(class_="css-16kqa8y efwtv890")

        if not car_cards:  # Если не найдено объявлений, выходим из цикла
            break

        for card in car_cards:
            model = card.text.strip()
            engine_volume_element = card.find_next(class_="css-1l9tp44 e162wx9x0")
            engine_volume = (
                engine_volume_element.text.strip()
                if engine_volume_element
                else "Не найден"
            )
            price_element = card.find_next(class_="css-46itwz e162wx9x0")
            price_span = (
                price_element.find("span", {"data-ftid": "bull_price"})
                if price_element
                else None
            )
            price = (
                price_span.text.strip().replace("\xa0", "")
                if price_span
                else "Не найден"
            )
            city_element = card.find_next(class_="css-1488ad e162wx9x0")
            city_name = city_element.text.strip() if city_element else "Не найден"
            image_element = card.find_next(
                class_="emt6rd1", attrs={"data-ftid": "bull_image"}
            )
            image_url = (
                image_element.find("img")["src"]
                if image_element and image_element.find("img")
                else "Не найден"
            )

            fuel_element = card.find_next(
                "span",
                {
                    "data-ftid": "bull_description-item",
                    "class": "css-1l9tp44 e162wx9x0",
                },
            )
            fuel = fuel_element.text.strip() if fuel_element else "Не найден"

            drive_element = (
                fuel_element.find_next(
                    "span",
                    {
                        "data-ftid": "bull_description-item",
                        "class": "css-1l9tp44 e162wx9x0",
                    },
                )
                if fuel_element
                else None
            )
            drive = drive_element.text.strip() if drive_element else "Не найден"

            mileage_element = (
                drive_element.find_next(
                    "span",
                    {
                        "data-ftid": "bull_description-item",
                        "class": "css-1l9tp44 e162wx9x0",
                    },
                )
                if drive_element
                else None
            )
            mileage = (
                mileage_element.text.strip().replace("\xa0", "")
                if mileage_element
                else "Не найден"
            )

            car_details = {
                "model": model,
                "engine_volume": engine_volume,
                "price": price,
                "city": city_name,
                "image_url": image_url,
                "fuel": fuel,
                "drive": drive,
                "mileage": mileage,
            }
            car_details_list.append(car_details)

            print(f"\nМодель: {car_details['model']}")
            print(f"Объем двигателя: {car_details['engine_volume']}")
            print(f"Цена: {car_details['price']}")
            print(f"Город: {car_details['city']}")
            print(f"Ссылка на изображение: {car_details['image_url']}")
            print(f"Топливо: {car_details['fuel']}")
            print(f"Привод: {car_details['drive']}")
            print(f"Пробег: {car_details['mileage']}")

            image_filename = f"media/{car_details['model'].replace(' ', '_')}.jpg"
            download_image(car_details["image_url"], image_filename)

        page += 1  # Переход к следующей странице

    return car_details_list


def download_image(url, filepath):
    """Скачивает изображение по указанному URL и сохраняет по пути filepath."""
    response = requests.get(url)
    with open(filepath, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
    print(f"Изображение сохранено: {filepath}")


def main():
    brands, links = parse_car_brands()
    print("Список марок автомобилей и их ссылки:\n")

    for brand, link in zip(brands, links):
        if not link.startswith("http"):
            link = "https://auto.drom.ru" + link

        brand_name = link.split("/")[-2]
        filtered_url = f"https://spb.drom.ru/{brand_name}"  # Указываем субдомен города
        print(
            f"{brand}: {filtered_url}/all/?ph=1&unsold=1\n"
        )  # Форматируем вывод ссылки

        try:
            car_details_list = parse_car_details(filtered_url)
        except Exception as e:
            print(f"Ошибка при получении деталей для {brand}: {e}")


if __name__ == "__main__":
    main()
