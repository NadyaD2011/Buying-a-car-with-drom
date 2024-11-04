from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import json
from urllib.parse import urljoin
import os

env = Environment(
    loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)


def rebuild(index_path):
    template = env.get_template("html/blog-base.html")
    for brand_name in cars:
        card_list = cars[brand_name]
        cars_list = []
        for card_car in card_list["cars"]:
            cars_list.append(card_list["cars"][card_car])
            rendered_page = template.render(brand_name=brand_name, cars_list=cars_list)
            name_file = urljoin(index_path, 'index.html')
            with open(name_file, "w", encoding="utf8") as file:
                file.write(rendered_page)


def create_brand_file(index_path):
    template = env.get_template("html/blog-base_brand.html")
    for brand_name in cars:
        card_list = cars[brand_name]
        cars_list = []
        for card_car in card_list["cars"]:
            cars_list.append(card_list["cars"][card_car])
            rendered_page = template.render(brand_name=brand_name, cars_list=cars_list)
            name_file = urljoin(index_path, f'index_{brand_name}.html')
            with open(name_file, "w", encoding="utf8") as file:
                file.write(rendered_page)


create_brand_file(index_path)
rebuild(index_path)


server = Server()
server.watch("html/*.html", rebuild, create_brand_file)
server.serve(root="index_path/index.html")