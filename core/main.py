from database import Database
from get_data import Getdata
from wholesalers import wholesalers

# Create DataBase
database = Database()
list_path = 'data/wholesalers_inventory/medicine_list/all.csv'

# Getdata from ftp servers
get_data = Getdata(wholesalers)
# Download data from drugstores
# get_data.download_data()
# Create data List
# get_data.create_medicine_list_for_db()

# load data list
# medicines = get_data.load_data_frame(path=list_path)

# Populate database
# database.add_products(medicines)

# add suppliers
# database.add_supplier(wholesalers)
# product = database.get_product(526)
# for info_product in product.prices:
#     print(f'price for {info_product.medicine_info.name} in {info_product.supplier_info.name}: '
#           f'${info_product.price} due date: {info_product.due_data} stock: {info_product.stock}')

#Create supplier list for database
# get_data.create_supplier_list_for_database(wholesalers)

# Add data to product_prices
# product_info_price = get_data.set_product_prices(price_dollar=36.31)
# database.add_product_prices(product_info_price)


# product = database.get_product(4119)
# print(product.name)


# product_info = [f'${price.price} en {price.supplier_info.name}\
# , Stock: {price.stock}, Fecha de vencimiento: {price.due_data}' for price in product.prices]
# product_info.sort()

# product_info = [[price.price, product] for price in product.prices]
# product_info.sort()
#
# for info in product_info:
#     print(info)


