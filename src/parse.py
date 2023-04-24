from bs4 import BeautifulSoup
import json
import yaml

class Parser:
    def __init__(self, source):
        self.source = source
    def parse(self):
        name = []
        price = []
        goods = { }
        with open(self.source, "r") as f:
            soup = BeautifulSoup(f, "html.parser").find_all("div", attrs={"class": "catalog-card"})

        for item in soup:

            a = item.find('a', attrs={"class": "catalog-card__title"}).text

            b = item.b.text
            b = b.replace('от ', '')
            b = b.replace(' ₽', '')
            b = b.replace(' ', '')

            price.append(int(b))

            name.append(a)

        goods = {name[i]: price[i] for i in range(len(name))}

        return goods

    def save(self, path, format="json"):
        if format == "json":
            with open(path, "w") as f:
                a = self.parse()
                json.dump(a, f, ensure_ascii=True)

        elif format == "yaml":
            with open(path, "w") as f:
                yaml.dump(self.parse(), f)

        else:
            raise ValueError("Неподдерживаемый формат: {}".format(format))


