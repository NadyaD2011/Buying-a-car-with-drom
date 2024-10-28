import requests
from bs4 import BeautifulSoup


def parse_car_brands():
    car_brands = []
    car_links = []
    url = "https://auto.drom.ru/"

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    car_elements = soup.find_all(class_="css-m7q1zs e4ojbx42")

    for element in car_elements:
        car_name = element.find("span", class_="css-1kb7l9z e162wx9x0").text.strip()
        car_link = element.find("a", class_="css-1q66we5 e4ojbx43")["href"]
        car_brands.append(car_name)
        car_links.append(car_link)

    return car_brands[:5], car_links[:5]


def parse_car_details(base_url):
    page = 1
    car_details_list = []

    while True:
        url = f"{base_url}&page={page}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        car_cards = soup.find_all(
            class_="css-16kqa8y efwtv890"
        )  # Локатор карточки авто

        if not car_cards:
            break  # Прерываем, если карточек на странице нет

        for card in car_cards:
            model = card.text.strip() if card else "Не найден"
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
            city = city_element.text.strip() if city_element else "Не найден"
            image_element = card.find_next(
                class_="emt6rd1", attrs={"data-ftid": "bull_image"}
            )
            image_url = (
                image_element.find("img")["src"]
                if image_element and image_element.find("img")
                else "Не найден"
            )

            car_details_list.append(
                {
                    "model": model,
                    "engine_volume": engine_volume,
                    "price": price,
                    "city": city,
                    "image_url": image_url,
                }
            )

        page += 1  # Переход на следующую страницу

    return car_details_list


def main():
    brands, links = parse_car_brands()
    print("Список марок автомобилей и их ссылки:\n")

    for brand, link in zip(brands, links):
        if not link.startswith("http"):
            link = "https://auto.drom.ru" + link

        brand_name = link.split("/")[-2]
        filtered_url = f"https://spb.drom.ru/{brand_name}/all/?ph=1&unsold=1"
        print(f"{brand}: {filtered_url}")

        try:
            car_details_list = parse_car_details(filtered_url)
            for car_details in car_details_list:
                print(car_details)
        except Exception as e:
            print(f"Ошибка при получении деталей для {brand}: {e}")


if __name__ == "__main__":
    main()
