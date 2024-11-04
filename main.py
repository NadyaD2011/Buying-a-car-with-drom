from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import json
from urllib.parse import urljoin
import os



env = Environment(
    loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)

index_path = "index_path/"
os.makedirs(index_path, exist_ok=True)

with open("cars_data.json", "r", encoding="utf8") as file:
    cars = json.load(file)


def rebuild_base(index_path, cars):
    template = env.get_template("html/blog-base.html")
    brand_names = cars.keys()
    for brand_name in cars:
        card_list = cars[brand_name]
        cars_list = []
        for card_car in card_list["cars"]:
            cars_list.append(card_list["cars"][card_car])
            rendered_page = template.render(
                brand_name=brand_name, cars_list=cars_list, brand_names=brand_names)
            name_file = urljoin(index_path, 'index.html')
            with open(name_file, "w", encoding="utf8") as file:
                file.write(rendered_page)


def rebuild_base_brand(index_path, cars):
    template = env.get_template("html/blog-base_brand.html")
    for brand_name in cars:
        card_list = cars[brand_name]
        cars_list = []
        for card_car in card_list["cars"]:
            cars_list.append(card_list["cars"][card_car])
            rendered_page = template.render(
                brand_name=brand_name, cars_list=cars_list)
            name_file = urljoin(index_path, f'index_{brand_name}.html')
            with open(name_file, "w", encoding="utf8") as file:
                file.write(rendered_page)


rebuild_base(index_path, cars)
rebuild_base_brand(index_path, cars)



server = Server()
server.watch("html/*.html", rebuild_base, rebuild_base_brand)
server.serve(root=".",  default_filename="index_path/index_Changan.html")
