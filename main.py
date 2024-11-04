from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import json
from urllib.parse import urljoin
import os

env = Environment(
    loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)


def rebuild():
    template = env.get_template("html/blog-base.html")

    with open("cars_data.json", "r", encoding="utf8") as file:
        cars = json.load(file)

    rendered_page = template.render(cars=cars)

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)


def create_brand_file():
    template = env.get_template("html/blog-base_brand.html")

    with open("cars_data.json", "r", encoding="utf8") as file:
        cars = json.load(file)

    index_path = "index_path/"
    os.makedirs(index_path, exist_ok=True)

    for brand_name in cars:
        card_list = cars[brand_name]
        rendered_page = template.render(brand_name=brand_name, card_list=card_list)
        name_file = urljoin(index_path, f"index_{brand_name}.html")
        with open(name_file, "w", encoding="utf8") as file:
            file.write(rendered_page)


create_brand_file()
rebuild()

server = Server()
server.watch("html/blog-base_brand.html", rebuild)
server.serve(root=".")
