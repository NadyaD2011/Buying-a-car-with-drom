import os
import requests
from bs4 import BeautifulSoup
import json


def parse_car_brands():
    """Парсит ссылки и иконки марок автомобилей."""
    car_brands = {}
    url = 'https://auto.drom.ru/'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    car_elements = soup.find_all(class_='css-m7q1zs e4ojbx42')
    
    icons_folder = "media/icons"
    if not os.path.exists(icons_folder):
        os.makedirs(icons_folder)
    
    for number in range(5):
        car_name = car_elements[number].find('span', class_='css-1kb7l9z e162wx9x0').text.strip()
        car_link = car_elements[number].find('a', class_='css-1q66we5 e4ojbx43')['href']
        
        icon_element = car_elements[number].find(class_='evrha4s0')
        icon_url = icon_element['src']
        icon_filename = f"{icons_folder}/{car_name}.png"
        download_image(icon_url, icon_filename)
        
        car_brands[car_name] = {
            'link': car_link,
            'icon_url': icon_url
        }

    return car_brands


def parse_car_details(base_url):
    if not os.path.exists("media"):
        os.makedirs("media")

    params = {
        'ph': '1',
        'unsold': '1',
        'location': 'spb'
    }
    cars = {}
    for page_number in range(1, 11):
        url = f"{base_url}all/page{page_number}/" if page_number > 1 else f"{base_url}all/"
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        car_cards = soup.find_all(class_='css-1f68fiz ea1vuk60')

        for card in car_cards:
            model = card.find(class_='css-16kqa8y efwtv890').text
            image_element = card.find(class_='emt6rd1', attrs={'data-ftid': 'bull_image'})
            image_url = image_element.find('img')['src'] if image_element else 'Не найден'

            engine_volume_element = card.find(class_='css-1l9tp44 e162wx9x0')
            engine_volume = engine_volume_element.text.strip() if engine_volume_element else 'Не найден'

            description_element = card.find(class_='css-1fe6w6s e162wx9x0')
            description_items = description_element.find_all('span', {'data-ftid': 'bull_description-item'})
            fuel = description_items[1].text.strip() if len(description_items) > 1 else ''
            transmission = description_items[2].text.strip() if len(description_items) > 2 else ''
            drive = description_items[3].text.strip() if len(description_items) > 3 else ''
            mileage = description_items[4].text.strip().replace('\xa0', '') if len(description_items) > 4 else ''

            price_element = soup.find('span', {'data-ftid': 'bull_price'})
            price = price_element.text.replace('\xa0', '') if price_element else 'Не найден'

            location_element = soup.find('span', {'data-ftid': 'bull_location'})
            city = location_element.text.strip() if location_element else 'Не найден'

            link_element = card.find('a', class_='g6gv8w4 g6gv8w8 _1ioeqy90', attrs={'data-ftid': 'bull_title'})
            ad_link = link_element['href'] if link_element else None

            car_details = {
                'model': model,
                'engine_volume': engine_volume,
                'price': price,
                'city': city,
                'ad_link': ad_link,
                'fuel_type': fuel,
                'transmission': transmission,
                'drive': drive,
                'mileage': mileage,
                'image_url': image_url
            }
            cars[model] = car_details

            image_filename = f"media/{model}.jpg"
            download_image(image_url, image_filename)

    return cars


def download_image(url, filepath):
    response = requests.get(url)
    with open(filepath, 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)


def main():
    all_cars = {}
    brands = parse_car_brands()

    for brand_name, brand_info in brands.items():
        brand_cars = parse_car_details(brand_info['link'])
        all_cars[brand_name] = {
            'link': brand_info['link'],
            'icon_url': brand_info['icon_url'],
            'cars': brand_cars
        }
        
    with open("cars_data.json", "w", encoding="utf-8") as json_file:
        json.dump(all_cars, json_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
