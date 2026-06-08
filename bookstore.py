import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class Bookstore:
    def __init__(self):
        self.inventory_file = "inventory.csv"
        self.sales_file = "sales.csv"

        try:
            self.inventory_df = pd.read_csv(self.inventory_file)
        except:
            self.inventory_df = pd.DataFrame(
                columns=["Title", "Author", "Genre", "Price", "Quantity"]
            )

        try:
            self.sales_df = pd.read_csv(self.sales_file)
        except:
            self.sales_df = pd.DataFrame(
                columns=["Date", "Title", "Quantity Sold", "Total Revenue"]
            )

    def save_inventory(self):
        self.inventory_df.to_csv(self.inventory_file, index=False)

    def save_sales(self):
        self.sales_df.to_csv(self.sales_file, index=False)

    def add_book(self, title, author, genre, price, quantity):
        new_book = pd.DataFrame(
            [[title, author, genre, price, quantity]],
            columns=["Title", "Author", "Genre", "Price", "Quantity"]
        )
        self.inventory_df = pd.concat([self.inventory_df, new_book], ignore_index=True)
        self.save_inventory()

    def record_sale(self, title, qty):
        mask = self.inventory_df["Title"].str.lower() == title.lower()
        if not mask.any():
            return

        idx = self.inventory_df[mask].index[0]
        stock = self.inventory_df.loc[idx, "Quantity"]

        if stock < qty:
            return

        price = self.inventory_df.loc[idx, "Price"]
        revenue = qty * price

        self.inventory_df.loc[idx, "Quantity"] -= qty

        sale = pd.DataFrame(
            [[datetime.now(), title, qty, revenue]],
            columns=["Date", "Title", "Quantity Sold", "Total Revenue"]
        )

        self.sales_df = pd.concat([self.sales_df, sale], ignore_index=True)

        self.save_inventory()
        self.save_sales()

store = Bookstore()
