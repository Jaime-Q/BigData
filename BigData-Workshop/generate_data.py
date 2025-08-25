import csv
import datetime
import random
import pandas as pd
import matplotlib.pyplot as plt

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


def cargar_datos(ruta="sales.csv"):
    df = pd.read_csv(ruta, parse_dates=["date"])
    df["month"] = df["date"].dt.month
    return df

def ventas_por_categoria(df):
    category_totals = df.groupby("category")["total"].sum()
    category_totals.plot(kind="bar", color=["skyblue", "salmon", "lightgreen"])
    plt.title("Total de ventas por categoría")
    plt.ylabel("Ventas ($)")
    plt.xlabel("Categoría")
    plt.tight_layout()
    plt.show()

def ventas_mensuales(df):
    monthly_sales = df.groupby("month")["total"].sum()
    monthly_sales.plot(kind="line", marker="o", color="purple")
    plt.title("Ventas mensuales en 2025")
    plt.xlabel("Mes")
    plt.ylabel("Ventas ($)")
    plt.xticks(range(1,13))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def productos_mas_vendidos(df):
    top_products = df.groupby("product")["quantity"].sum().sort_values(ascending=True)
    top_products.plot(kind="barh", color="orange")
    plt.title("Productos más vendidos por cantidad")
    plt.xlabel("Cantidad vendida")
    plt.ylabel("Producto")
    plt.tight_layout()
    plt.show()

def menu():
    df = cargar_datos()
    while True:
        print("\n📊 Menú de visualización de ventas")
        print("1. Ventas por categoría")
        print("2. Ventas mensuales")
        print("3. Productos más vendidos")
        print("4. Salir")
        opcion = input("Selecciona una opción (1-4): ")

        if opcion == "1":
            ventas_por_categoria(df)
        elif opcion == "2":
            ventas_mensuales(df)
        elif opcion == "3":
            productos_mas_vendidos(df)
        elif opcion == "4":
            print("¡Hasta pronto, Jaime!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()