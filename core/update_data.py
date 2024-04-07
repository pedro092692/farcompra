from .FTP.ftp import FTP
from .file_manipulator.file_manipulator import FileHandler
from .dataframe_manipulator.dataframe_manipulator import DataFrameHandler
from database import Database
from flask import url_for, redirect
import os

PATH = 'core/data'
MANUAL_PATH = 'core/data/manual_uploads'

class UpdateData:
    def __init__(self, wholesalers: dict , db: Database):
        self.wholesalers = wholesalers
        self.list_files = os.listdir(PATH)
        self.valid_extensions = ('.csv', '.xlsx', '.txt')
        self.df_handler = DataFrameHandler()
        self.db = db
        self.errors = []
        self.checking_errors()

    def download(self):
        for wholesaler in self.wholesalers:
            # get data from ftps server
            url = self.wholesalers[wholesaler]['url']
            user = self.wholesalers[wholesaler]['user']
            password = self.wholesalers[wholesaler]['password']
            path = self.wholesalers[wholesaler]['path']
            file_name = self.wholesalers[wholesaler]['file_name']
            alias = wholesaler

            # download data and filter for manually uploads
            if url:
                new_connection = FTP(url=url, user=user, password=password, path=path, file_name=file_name, alias=alias)
                new_connection.download_file()
                # store errors
                if new_connection.error_log:
                    self.errors.append(new_connection.error_log)

        file_handler = FileHandler()
        file_handler.convert_all_to_csv()

        self.add_new_products_to_db()
        self.add_new_products_prices_to_db()


    def add_new_products_to_db(self):

        new_product_list = self.df_handler.dataframe_products()
        products_from_db = self.df_handler.load_dataframe_from_db(columns=['barcode', 'name'], table_name='products')
        diff_df_products = self.df_handler.dataframe_diff(df_1=products_from_db, df_2=new_product_list,
                                                          column='barcode')
        if len(diff_df_products):
            self.db.add_products(diff_df_products)
        else:
            self.errors.append('No New products to add in database.')

    def add_new_products_prices_to_db(self):
        new_prices_list = self.df_handler.dataframe_products_prices()
        self.db.add_product_prices(new_prices_list)


    def manually_upload(self, file):
        file_name = file.filename.split('.')[0]

        allowed_file = ['csv', 'txt', 'xlsx', 'xls']

        if file.filename.split('.')[1] not in allowed_file:
            self.errors.append(['File Upload No Valid Format'])
        else:
            file.save(os.path.join(MANUAL_PATH, file.filename))




    def checking_errors(self):
        if self.df_handler.errors:
            self.errors.append(self.df_handler.errors)



