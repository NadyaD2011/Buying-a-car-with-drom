from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

with open("my.json", "r") as file:
  cars = json.load(file)
print(type(cars))

rendered_page = template.render(cars=cars)

with open('index.html', 'w', encoding="utf8") as file:
  file.write(rendered_page)
