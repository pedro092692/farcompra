import sqlalchemy.exc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey, select
from typing import List
from flask import Flask
import pandas

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
                                                        cascade='all, delete, delete-orphan',
                                                        order_by="ProductPrice.price.asc()")

class Supplier(Base):
    __tablename__ = "suppliers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    prices: Mapped[List["ProductPrice"]] = relationship(back_populates="supplier_info")

class ProductPrice(Base):
    __tablename__ = "product_prices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    product_info: Mapped["Product"] = relationship(back_populates="prices")
    price: Mapped[float] = mapped_column(Float, nullable=False)
    due_date: Mapped[str] = mapped_column(String(250), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey("suppliers.id"))
    supplier_info: Mapped["Supplier"] = relationship(back_populates="prices")


class User(Base, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    pharmacy: Mapped[List["Pharmacy"]] = relationship(back_populates='user_info',
                                                      cascade='all, delete, delete-orphan')

class Pharmacy(Base):
    __tablename__ = "pharmacies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rif: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(1000), nullable=False)
    address: Mapped[str] = mapped_column(String(1000), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user_info: Mapped["User"] = relationship(back_populates='pharmacy')



class Database:

    def __init__(self, app: Flask ):
        self.db = db
        self.app = app

        # DATABASE INIT
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farcompra.db'
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
        data.to_sql('product_prices', engine, index=False, if_exists='append', chunksize=3000)

    def show_products(self, per_page=20):
        # products = self.db.session.execute(self.db.select(Product).order_by(Product.name)).scalars().all()
        products = self.db.paginate(self.db.select(Product).filter(Product.prices.any()).order_by(Product.name),
                                    per_page=per_page)
        return products

    def search_products(self, q):
        products = self.db.paginate(self.db.select(Product).filter(Product.prices.any()).\
                                    filter(Product.name.icontains(q) |
                                     Product.barcode.icontains(q)).order_by(Product.name))
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
        self.db.session.query(ProductPrice).delete()
        self.db.session.commit()


    def get_product(self, product_id):
        product = self.db.get_or_404(Product, product_id)
        return product

    def delete_product(self, product_id):
        product = self.get_product(product_id)
        if product:
            self.db.session.delete(product)
            self.db.session.commit()


    ### Users ###
    def add_user(self, name, last_name, email, password):
        new_user = User(
            name=name,
            last_name=last_name,
            email=email,
            password=password
        )
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user

    def all_users(self):
        all_users = self.db.session.execute(self.db.select(User)).scalars().all()
        return all_users


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

    @staticmethod
    def check_user(email):
        return User.query.filter_by(email=email).first()

    def all_pharmacies(self):
        all_pharmacies = self.db.session.execute(self.db.select(Pharmacy)).scalars().all()
        return all_pharmacies

    def all_suppliers(self):
        all_suppliers = self.db.session.execute(self.db.select(Supplier)).scalars().all()
        return all_suppliers








