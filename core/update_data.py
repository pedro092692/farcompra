from .FTP.ftp import FTP
from .file_manipulator.file_manipulator import FileHandler
from .dataframe_manipulator.dataframe_manipulator import DataFrameHandler
from database import Database
from core.wholesalers import wholesalers
from flask import url_for, redirect
import os

PATH = 'core/data'
MANUAL_PATH = 'core/data/manual_uploads'


class UpdateData:
    def __init__(self, wholesalers: dict, db: Database, dollar=1):
        self.wholesalers = wholesalers
        self.list_files = os.listdir(PATH)
        self.valid_extensions = ('.csv', '.xlsx', '.txt')
        self.db = db
        self.df_handler = DataFrameHandler(db_=db)
        self.errors = []
        self.failed = []
        self.checking_errors()

    def download(self):
        # clear failed downloads list
        self.failed.clear()
        # download new data
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
                print(f'downloading: {alias}')
                new_connection.download_file()
                # store errors
                if new_connection.error_log:
                    e = new_connection.error_log
                    self.errors.append(e)
                    self.failed.append(self.wholesalers[wholesaler]['supplier_id'])

        if len(self.errors) < len(self.wholesalers) - 3:
            file_handler = FileHandler()
            file_handler.convert_all_to_csv()
            self.add_new_products_to_db()
            self.add_new_products_prices_to_db()
            file_handler.remove_all_files(path=PATH)

    def add_new_products_to_db(self):
        csv_files_list = FileHandler(mode='auto').csv_file_list()
        self.check_df_diff_products(csv_files_list=csv_files_list, path=PATH)

    def add_new_products_prices_to_db(self):
        csv_files_list = FileHandler(mode='auto').csv_file_list()
        new_prices_list = self.df_handler.dataframe_products_prices(csv_file_list=csv_files_list, path=PATH)
        self.db.add_product_prices(new_prices_list, failed=self.failed)

    def manually_upload(self, file):
        file_handler = FileHandler(mode='manual', path=MANUAL_PATH)
        file_name = file.filename.split('.')[0]

        list_of_files = os.listdir(MANUAL_PATH)

        # checking for files in path
        for file_path in list_of_files:
            if file_path.split('.')[1] in ['csv', 'txt', 'xlsx', 'xls']:
                print(file_path)
                file_handler.remove_all_files(path=MANUAL_PATH)

        if file_name in self.wholesalers.keys():

            allowed_file = ['csv', 'txt', 'xlsx', 'xls']
            if file.filename.split('.')[1] not in allowed_file:
                self.errors.append('File Upload No Valid Format')
            else:
                file.save(os.path.join(MANUAL_PATH, file.filename))
                self.manually_update(filename=file_name)

    def manually_update(self, filename=''):
        file_handler = FileHandler(mode='manual', path=MANUAL_PATH)
        file_handler.convert_all_to_csv()
        csv_files_list = FileHandler(mode='manual', path=MANUAL_PATH).csv_file_list()
        # updating products manually
        add_new_products = self.check_df_diff_products(csv_files_list=csv_files_list, path=MANUAL_PATH)
        if add_new_products:
            # updating products prices manually
            new_prices_list = self.df_handler.dataframe_products_prices(csv_file_list=csv_files_list, path=MANUAL_PATH)
            # check for old products in the list
            # 1) get supplier id
            try:
                supplier_id = wholesalers[filename]['supplier_id']
                # check for products on the price list
                count_products = self.db.products_by_supplier(supplier_id=supplier_id, count=True)
                if count_products > 0:
                    self.db.drop_products_by_supplier(supplier_id=supplier_id)
                    self.db.add_product_prices(new_prices_list, mode='manual')
                else:
                    self.db.add_product_prices(new_prices_list, mode='manual')

            except KeyError:
                print('Error with file name no supplier found')

            # remove all files in manual uploads
            file_handler.remove_all_files(path=MANUAL_PATH)

    def check_df_diff_products(self, csv_files_list, path):
        new_product_list = self.df_handler.dataframe_products(csv_file_list=csv_files_list, path=path)
        products_from_db = self.df_handler.load_dataframe_from_db(columns=['barcode', 'name'],
                                                                  table_name='products')
        if not self.df_handler.errors:
            diff_df_products = self.df_handler.dataframe_diff(df_1=products_from_db, df_2=new_product_list,
                                                              column='barcode')
            if len(diff_df_products):
                self.db.add_products(diff_df_products)
                self.errors.append('New products added')
            else:
                self.errors.append('Database updated successfully.')
            return True
        else:
            self.errors.append(self.df_handler.errors)

    def checking_errors(self):
        if self.df_handler.errors:
            self.errors.append(self.df_handler.errors)

    def testing(self):
        pass
        # df = self.df_handler.read_excel(path=PATH, filename='drovencentro_1.xlsx')
        # print(df)