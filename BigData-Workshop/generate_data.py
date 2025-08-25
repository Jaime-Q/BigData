import csv
import datetime
import random

CURRENTLY_YEAR = 2025

categories = ["Ropa", "Hogar", "Electronica"]
products = [
    "Televisor", "Celular", "Laptop", "Camisa", "Pantalon", 
    "Zapatos", "Sofa", "Mesa", "Silla"
]
with open("sales.csv", "w", newline="", encoding="utf-8") as file: 
    writer = csv.writer(file)
    writer.writerow([
        "id", "date", "product", "category", "price",
        "quantity", "total"
    ])

    for i in range(1, 100001):
        date = datetime.date(CURRENTLY_YEAR, random.randint(1,12), random.randint(1,28))
        product = random.choice(products)
        category = "Electronica" if product in ["Televisor", "Celular", "Laptop"] else ("Ropa" if product in ["Camisa", "Pantalon", "Zapatos"] else "Hogar")
        price = round(random.uniform(10, 2000), 2)
        quantity = random.randint(1,10)
        total = round(price * quantity, 2)
        writer.writerow((i, date, product, category, price, quantity, total))