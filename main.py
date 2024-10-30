from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import json

env = Environment(
  loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)


def rebuild():
  template = env.get_template("html/blog-base.html")

  with open("my.json", "r", encoding="utf8") as file:
    cars = json.load(file)

  rendered_page = template.render(cars=cars)

  with open("index.html", "w", encoding="utf8") as file:
    file.write(rendered_page)


rebuild()

server = Server()
server.watch("html/blog-base.html", rebuild)
server.serve(root=".")
