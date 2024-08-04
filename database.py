import sqlalchemy.exc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey, select, delete, join, func, case, and_, DateTime
from typing import List
from flask import Flask
from datetime import datetime
from flask_login import UserMixin
import pandas
import os


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


# CREATE EXTENSIONS
db = SQLAlchemy(model_class=Base)



# CONFIGURE TABLES

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    barcode: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    prices: Mapped[List["ProductPrice"]] = relationship(back_populates="product_info",
                                                        cascade='all, delete',
                                                        order_by="ProductPrice.price.asc()")

    def serialize(self):
        serialize_products = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        serialize_prices = [{'price': price.price,
                             'supplier_name': price.supplier_info.name,
                             'due_date': price.due_date,
                             'stock': price.stock} for price in self.prices]
        serialize_products['prices'] = serialize_prices
        return serialize_products


class Supplier(Base):
    __tablename__ = "suppliers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    prices: Mapped[List["ProductPrice"]] = relationship(back_populates="supplier_info")


class ProductPrice(Base, db.Model):
    __tablename__ = "product_prices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id", ondelete='CASCADE'))
    product_info: Mapped["Product"] = relationship(back_populates="prices")
    price: Mapped[float] = mapped_column(Float, nullable=False)
    due_date: Mapped[str] = mapped_column(String(250), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey("suppliers.id"))
    supplier_info: Mapped["Supplier"] = relationship(back_populates="prices")
    internal_code_product: Mapped[str] = mapped_column(String(250), nullable=True)


class User(Base, UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(200), nullable=False)
    active: Mapped[str] = mapped_column(String(20), nullable=False)
    pharmacy: Mapped[List["Pharmacy"]] = relationship(back_populates='user_info',
                                                      cascade='all, delete, delete-orphan')
    discount: Mapped[List["PharmacyDiscount"]] = relationship(back_populates='user_info',
                                                              cascade='all, delete, delete-orphan')


class Pharmacy(Base, db.Model):
    __tablename__ = "pharmacies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rif: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(1000), nullable=False)
    address: Mapped[str] = mapped_column(String(1000), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user_info: Mapped["User"] = relationship(back_populates='pharmacy')


class Cart(Base, db.Model):
    __tablename__ = "shoppingcart"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    product_price_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_info: Mapped["Product"] = relationship()
    supplier_id: Mapped[int] = mapped_column(Integer, nullable=False)
    supplier_name: Mapped[str] = mapped_column(String(250), nullable=False)
    product_name: Mapped[str] = mapped_column(String(250), nullable=False)
    product_price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    internal_code_product: Mapped[str] = mapped_column(String(250), nullable=True)

    def __repr__(self):
        return f'<CartItem {self.user_id}, {self.product_price_id}, {self.quantity}>'


class PharmacyDiscount(Base):
    __tablename__ = "pharmacy_discount"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey("suppliers.id"), nullable=False)
    discount: Mapped[float] = mapped_column(Float, nullable=False)
    user_info: Mapped["User"] = relationship(back_populates="discount")


class OrderHistory(Base, db.Model):
    __tablename__ = "order_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey("suppliers.id"), nullable=False)
    supplier_info: Mapped["Supplier"] = relationship()
    product_name: Mapped[str] = mapped_column(String(500), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())


class DollarPrice(Base, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())


class Database:

    def __init__(self, app: Flask):
        self.db = db
        self.app = app

        # DATABASE INIT
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///farcompra.db')
        self.db.init_app(self.app)



    def create_tables(self):
        with self.app.app_context():
            self.db.create_all()


    ### PRODUCTS ###
    def add_products(self, data:pandas.DataFrame):
        engine = self.db.engine
        data.to_sql('products', engine, index=False, if_exists='append', index_label='barcode', chunksize=1000)

    def add_product_prices(self, data: pandas.DataFrame, mode='auto'):
        if mode == 'auto':
            # before add new list delete anterior
            self.delete_products_prices()
        engine = self.db.engine
        # Add new data
        data.to_sql('product_prices', engine, index=False, if_exists='append', chunksize=7000)

    def show_products(self, per_page=20):
        products = self.db.paginate(self.db.select(Product).filter(Product.prices.any()).order_by(Product.name),
                                    per_page=per_page)
        return products

    def search_products(self, q, per_page=10):
        products = self.db.paginate(self.db.select(Product).filter(Product.name.icontains(q) | Product.barcode.icontains(q)).order_by(Product.name), per_page=per_page)

        return products

    def products_by_supplier(self, supplier_id, count=False):
        if count:
            total_products = self.db.session.execute(
                select(func.count(ProductPrice.id)).filter(ProductPrice.supplier_id == supplier_id)
            ).scalar()
            return total_products

    def drop_products_by_supplier(self, supplier_id):
        ProductPrice.query.filter(ProductPrice.supplier_id == supplier_id).delete()
        self.db.session.commit()

    def discount(self, q):

        discount_rate = 0.5  # 5% discount

        query = self.db.session.query(Product, ProductPrice) \
            .join(ProductPrice, Product.id == ProductPrice.product_id) \
            .filter(ProductPrice.supplier_id == 1) \
            .with_entities(Product, func.round((ProductPrice.price * (1 - discount_rate)), 2).label(
            "discounted_price"))  # Round to 2 decimal places

        products = self.db.paginate(self.db.select(Product).filter(Product.name.icontains(q) | Product.barcode.icontains(q)).order_by(Product.name), per_page=15)
        return products

    def last_products(self):
        last_products = self.db.session.execute(self.db.select(Product).order_by(Product.name.asc()).limit(8)).scalars().all()
        return last_products

    def show_all_product(self, per_page):
        all_products = self.db.paginate(
            self.db.select(Product).order_by(Product.name.asc()), per_page=per_page
        )
        return all_products



    def delete_products_prices(self):
        # Delete all products not for not auto-update suppliers
        statement = delete(ProductPrice).where(ProductPrice.supplier_id.notin_([6]))
        self.db.session.execute(statement)
        self.db.session.commit()

    def delete_all_products(self):
        self.db.session.query(Product).delete()
        self.db.session.commit()

    # delete all shopping cart items
    def delete_all_shopping_cart_items(self):
        self.db.session.query(Cart).delete()
        self.db.session.commit()

    def get_product(self, product_id):
        product = self.db.get_or_404(Product, product_id)
        return product

    def get_product_price(self, product_price_id):
        return self.db.get_or_404(ProductPrice, product_price_id)


    def delete_product(self, product_id):
        product = self.get_product(product_id)
        if product:
            self.db.session.delete(product)
            self.db.session.commit()

    def delete_supplier(self, supplier_id):
        supplier = self.get_supplier(supplier_id)
        if supplier:
            self.db.session.delete(supplier)
            self.db.session.commit()

    ### Users ###
    def add_user(self, name, last_name, email, password, role='user'):
        new_user = User(
            name=name,
            last_name=last_name,
            email=email,
            password=password,
            role=role,
            active='yes'
        )
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user

    def edit_user(self, user_id, name, last_name, email, password, role, active):
        user = self.get_user(user_id)
        user.name = name
        user.last_name = last_name
        user.email = email
        user.password = password
        user.role = role
        user.active = active
        self.db.session.commit()

    def all_users(self):
        all_users = self.db.session.execute(self.db.select(User).order_by(User.id.desc()).limit(8)).scalars().all()
        return all_users

    def last_users(self):
        last_users = self.db.session.execute(self.db.select(User).order_by(User.id.desc()).limit(8)).scalars().all()
        return last_users

    def delete_user(self, user_id):
        user = self.get_user(user_id=user_id)
        self.db.session.delete(user)
        self.db.session.commit()


    def add_pharmacy(self, rif, name, email, address, user_id):
        new_pharmacy = Pharmacy(
            rif=rif,
            name=name,
            email=email,
            address=address,
            user_id=user_id
        )

        self.db.session.add(new_pharmacy)
        self.db.session.commit()
        return new_pharmacy

    def edit_pharmacy(self, pharmacy_id, name, rif, email, address, user_email):
        user_id = self.check_user(user_email)
        pharmacy = self.get_pharmacy(pharmacy_id)
        pharmacy.name = name
        pharmacy.rif = rif
        pharmacy.email = email
        pharmacy.address = address
        pharmacy.user_id = user_id.id
        self.db.session.commit()

    def add_discount(self, user_id, supplier_id, discount):
        new_discount = PharmacyDiscount(
            user_id=user_id,
            supplier_id=supplier_id,
            discount=discount,
        )
        self.db.session.add(new_discount)
        self.db.session.commit()

    def get_user_discount(self, user_id, supplier_id):
        supplier_discount = self.db.session.execute(select(PharmacyDiscount).
                                                    filter_by(user_id=user_id, supplier_id=supplier_id)).first()
        return supplier_discount

    def get_user_discounts(self, user_id):
        user_discount = self.db.session.execute(select(PharmacyDiscount).filter_by(user_id=user_id)).scalars().all()

        # all_discount = {'supplier': supplier.supplier_id, 'discount': supplier.discount} for supplier in user_discount
        all_discount = {supplier.supplier_id: {'discount': supplier.discount} for supplier in user_discount}
        return all_discount

    def edit_user_discount(self, discount_item, new_discount):
        discount_item.discount = new_discount
        self.db.session.commit()

    def delete_user_discount(self, user_discount):
        self.db.session.delete(user_discount)
        self.db.session.commit()

    ### Cart ###

    def add_to_cart(self, user_id, product_price_id, quantity, supplier_id, supplier_name, product_name, product_price,
                    product_id, internal_code_product):
        new_cart_item = Cart(
            user_id=user_id,
            product_price_id=product_price_id,
            quantity=quantity,
            supplier_id=supplier_id,
            supplier_name=supplier_name,
            product_name=product_name,
            product_price=product_price,
            product_id=product_id,
            internal_code_product=internal_code_product
        )
        self.db.session.add(new_cart_item)
        self.db.session.commit()

    def view_cart(self, user_id):
        shopping_cart = {}
        cart = self.db.session.execute(select(Cart).filter(Cart.user_id == user_id)).scalars().all()
        for item in cart:
            if item.supplier_name not in shopping_cart:
                shopping_cart[item.supplier_name] = {
                    "supplier_id": item.supplier_id,
                    "products": {},
                    "total": 0
                }
            shopping_cart[item.supplier_name]["products"][item.product_name] = {
                "id": item.product_price_id,
                "price": item.product_price,
                "quantity": item.quantity,
                "id_cart": item.id
            }

            shopping_cart[item.supplier_name]["total"] += round(
                shopping_cart[item.supplier_name]["products"][item.product_name]["price"] *
                shopping_cart[item.supplier_name]["products"][item.product_name]["quantity"], 2
            )
        return shopping_cart

    def view_history(self, user_id):
        history = {}
        order_history = self.db.session.execute(select(OrderHistory).filter(OrderHistory.user_id == user_id)).scalars().all()

        for item in order_history:
            if item.supplier_info.name not in history:
                history[item.supplier_info.name] = {
                    "id": item.supplier_id,
                    "products": {},
                    "total": 0,
                    "date": item.date
                }
            history[item.supplier_info.name]['products'][item.product_name] = {
                "price": item.price,
                "quantity": item.quantity,
                "total": round(item.price * item.quantity, 2)
            }
            history[item.supplier_info.name]['total'] += \
                history[item.supplier_info.name]['products'][item.product_name]['price'] * \
                history[item.supplier_info.name]['products'][item.product_name]['quantity']

        return history

    def get_supplier_total(self, user_id, supplier_id):
        supplier_list = Cart.query.filter_by(user_id=user_id, supplier_id=supplier_id).all()
        total = 0
        for item in supplier_list:
            total += item.product_price * item.quantity
        return round(total, 2)

    def update_cart(self, cart_item, quantity):
        cart_item.quantity += quantity
        self.db.session.commit()
        return cart_item

    def update_cart_quantity(self, cart_item, quantity):
        cart_item.quantity = quantity
        self.db.session.commit()
        return cart_item

    ### ORDER HISTORY ###
    def add_order_history(self, user_id, supplier_id, product_name, quantity, price):


        new_order = OrderHistory(
            user_id=user_id,
            supplier_id=supplier_id,
            product_name=product_name,
            quantity=quantity,
            price=price,
        )
        self.db.session.add(new_order)
        self.db.session.commit()

    def delete_last_order_history(self, user_id, supplier_id):
        old_order = self.get_history_by_supplier(user_id=user_id, supplier=supplier_id)
        if old_order:
            # Delete last order
            items_to_delete = delete(OrderHistory).filter_by(user_id=user_id, supplier_id=supplier_id)
            self.db.session.execute(items_to_delete)
            self.db.session.commit()

    @staticmethod
    def check_product_cart(product_price_id, user_id):
        return Cart.query.filter_by(product_price_id=product_price_id, user_id=user_id).first()

    def get_car_item(self, cart_item_id):
        return self.db.get_or_404(Cart, cart_item_id)

    def delete_cart_item(self, cart_item):
        self.db.session.delete(cart_item)
        self.db.session.commit()



    def checkout_cart(self, user_id, supplier):
        # Delete cart items
        items_to_delete = delete(Cart).filter_by(user_id=user_id, supplier_id=supplier)
        self.db.session.execute(items_to_delete)
        self.db.session.commit()

    @staticmethod
    def get_cart_by_supplier(user_id, supplier):
        supplier_items = Cart.query.filter_by(user_id=user_id, supplier_id=supplier)
        return supplier_items

    @staticmethod
    def get_history_by_supplier(user_id, supplier):
        supplier_items = OrderHistory.query.filter_by(user_id=user_id, supplier_id=supplier)
        return supplier_items.all()




    @staticmethod
    def check_user(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def check_pharmacy(email):
        return Pharmacy.query.filter_by(email=email).first()

    def get_user(self, user_id):
        return self.db.get_or_404(User, user_id)

    def all_pharmacies(self):
        all_pharmacies = self.db.session.execute(self.db.select(Pharmacy).order_by(Pharmacy.id.desc()).limit(8)).scalars().all()
        return all_pharmacies

    def get_pharmacy(self, pharmacy_id):
        return self.db.get_or_404(Pharmacy, pharmacy_id)


    def all_suppliers(self):
        all_suppliers = self.db.session.execute(self.db.select(Supplier).order_by(Supplier.name)).scalars().all()
        return all_suppliers

    def get_ftp_suppliers(self, suppliers: list):
        ftp_suppliers = self.db.session.execute(self.db.select(Supplier).
                                                filter(Supplier.name.in_(suppliers))).scalars().all()
        return ftp_suppliers

    def get_supplier(self, supplier_id):
        return self.db.get_or_404(Supplier, supplier_id)

    def add_supplier(self, name):
        new_supplier = Supplier(
            name=name
        )
        self.db.session.add(new_supplier)
        self.db.session.commit()

    ### Dollar ###
    def get_dollar_info(self):
        with self.app.app_context():
            dollar_info = DollarPrice.query.first()
            return dollar_info


    def update_dollar_value(self, value):
        with self.app.app_context():
            if not self.get_dollar_info():
                new_dollar_value = DollarPrice(
                    value=value
                )
                self.db.session.add(new_dollar_value)
                self.db.session.commit()
                return new_dollar_value
            else:
                dollar_value = self.db.first_or_404(self.db.select(DollarPrice).filter_by(id=1))
                dollar_value.value = value
                dollar_value.date = datetime.now()
                self.db.session.commit()







