import sqlalchemy.exc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, ForeignKey
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

    def delete_products_prices(self):
        self.db.session.query(ProductPrice).delete()
        self.db.session.commit()


    def get_product(self, product_id):
        product = self.db.get_or_404(Product, product_id)
        return product

