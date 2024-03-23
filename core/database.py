from sqlalchemy import create_engine
from sqlalchemy import String, Integer, select, ForeignKey, Float, desc, asc
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import List
import pandas


class Base(DeclarativeBase):
    pass

class Medicine(Base):
    __tablename__ = "medicines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    barcode: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    prices: Mapped[List["MedicinePrice"]] = relationship(back_populates="product_info")


class Supplier(Base):
    __tablename__ = "suppliers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    prices: Mapped[List["MedicinePrice"]] = relationship(back_populates="supplier_info")

class MedicinePrice(Base):
    __tablename__ = "medicine_prices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("medicines.id"))
    product_info: Mapped["Medicine"] = relationship(back_populates="prices")
    price: Mapped[float] = mapped_column(Float, nullable=False)
    due_data: Mapped[str] = mapped_column(String(250), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey("suppliers.id"))
    supplier_info: Mapped["Supplier"] = relationship(back_populates="prices")

class Database:

    def __init__(self):
        self.engine = create_engine("sqlite:///farcompra.db")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)


    def add_products(self, data:pandas.DataFrame):
        engine = self.engine
        old_data = self.read_list_from_db()
        new_data = data
        diff_data = self.compare_dataframe(old_data, new_data)
        if len(diff_data):
            diff_data.to_sql('medicines', engine, index=False, if_exists='append', index_label='barcode', chunksize=1000)


    def read_list_from_db(self, columns=['barcode', 'name']) -> pandas.DataFrame:
        engine = self.engine
        data = pandas.read_sql('medicines', engine, coerce_float=False, columns=columns)

        return data

    def select_barcodes(self, barcodes: list) -> list:
        # products = self.session.query(Medicine.id).filter(Medicine.barcode.in_(barcodes)).order_by(asc(Medicine.barcode)).all()
        return [self.select_barcode(product) for product in barcodes]


    def add_product_prices(self, data: pandas.DataFrame):
        engine = self.engine
        medicine_prices = data
        medicine_prices.to_sql('medicine_prices', engine, index=False, if_exists='append', chunksize=2000)

    @staticmethod
    def compare_dataframe(df_1, df_2) -> pandas.DataFrame:
        diff_df = df_2[~df_2['barcode'].isin(df_1['barcode'])]
        return diff_df

    def add_supplier(self, suppliers):
        for supplier in suppliers:
            new_supplier = Supplier(
                name=supplier
            )
            self.session.add(new_supplier)
            self.session.commit()


    def get_product(self, product_id):
        product = self.session.get_one(Medicine, product_id)
        return product


    def reset_product_prices(self):
        self.session.query(MedicinePrice).delete()
        self.session.commit()

    def select_barcode(self, barcode) -> Medicine:
        product = self.session.query(Medicine).filter(Medicine.barcode == barcode).one()
        return product
    # def add_product(self, df:pandas.DataFrame, headers:list):
    #     for index, row in df.iterrows():
    #         barcode = self.check_if_exist(barcode=row[headers[0]])
    #         if not barcode:
    #             new_product = Medicine(
    #                 barcode=row[headers[0]],
    #                 name=row[headers[1]]
    #             )
    #             self.session.add(new_product)
    #             self.session.commit()
    #
    # def check_if_exist(self, barcode):
    #     with Session(self.engine) as session:
    #         stm = select(Medicine).filter_by(barcode=barcode)
    #         medicine = session.scalars(stm).one_or_none()
    #         if medicine:
    #             return True

    # def update_medicines_database(self, data:dict):
    #     for data_name in data:
    #         path = f"data/wholesalers_inventory/medicine_list/{data_name}_medicine_list.csv"
    #         headers = data[data_name]['database_headers']
    #         medicine_list = self.read_csv(path)
    #         # Add to database
    #         self.add_product(medicine_list, headers)
    #
    #
    # @staticmethod
    # def read_csv(path):
    #     df = pandas.read_csv(path, sep=';', on_bad_lines='skip')
    #     return df
