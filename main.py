from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

cars = [
    {
        "image": "картинка",
        "model": "модель",
        "price": "цена",
        "year": "год",
        "horsepower": "лошадиные силы",
        "transmission": "коробка",
        "gear": "передача",
        "engine": "двигатель",
        "mileage": "пробег"
    },
    {
        "image": "картинка",
        "model": "модель",
        "price": "цена",
        "year": "год",
        "horsepower": "лошадиные силы",
        "transmission": "коробка",
        "gear": "передача",
        "engine": "двигатель",
        "mileage": "пробег"
    },
    {
        "image": "картинка",
        "model": "модель",
        "price": "цена",
        "year": "год",
        "horsepower": "лошадиные силы",
        "transmission": "коробка",
        "gear": "передача",
        "engine": "двигатель",
        "mileage": "пробег"
    }
]

rendered_page = template.render(cars=cars)

with open('index.html', 'w', encoding="utf8") as file:
  file.write(rendered_page)
