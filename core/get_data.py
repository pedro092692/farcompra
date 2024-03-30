import ftplib
import pandas
import sys
from database import Aux


PATH = 'core/data/wholesalers_inventory'
MEDICINES_PATH = 'core/data/wholesalers_inventory/medicine_list/all.csv'
class Getdata:

    def __init__(self, wholesalers, db):
        self.wholesalers = wholesalers
        self.aux = Aux(db.db)
        self.supplier_errors = {}



    def update_data(self) -> pandas.DataFrame:
        self.download_data()
        self.create_medicine_list_for_db()
        medicines_data_frame = self.load_data_frame(MEDICINES_PATH)
        medicines_data_frame_str_barcode = self.converting_columns_to_str(df=medicines_data_frame, column_name='barcode')
        return medicines_data_frame_str_barcode

    def update_price_list(self, dollar_value) -> pandas.DataFrame:
        self.create_supplier_list_for_database(self.wholesalers)
        products_info = self.set_product_prices(dollar_value=dollar_value)
        return products_info

    def download_data(self):
        if self.wholesalers:
            self.supplier_errors.clear()
            for wholesaler_name in self.wholesalers:

                ftp_server = self.wholesalers[wholesaler_name]['url']
                username = self.wholesalers[wholesaler_name]['user']
                password = self.wholesalers[wholesaler_name]['password']
                path = self.wholesalers[wholesaler_name]['path']
                filename = self.wholesalers[wholesaler_name]['file_name']
                wholesaler_name = self.wholesalers[wholesaler_name]['name']
                headers = self.wholesalers[wholesaler_name]['headers']

                conn = self.connect_from_ftp(ftp_server, username, password, wholesaler_name)

                if not conn:
                    print(f"There was a connection problem with {wholesaler_name}: "
                          f"{self.supplier_errors[wholesaler_name]['error']}")
                    continue

                if wholesaler_name not in self.supplier_errors:

                    if path:
                        conn.cwd(path)
                        with open(f"{PATH}/{wholesaler_name}_inventory.csv", "wb") as file:
                            conn.retrbinary(f'RETR {filename}', file.write)

                    if self.wholesalers[wholesaler_name]['fix_data']:
                        self.fix_data(self.wholesalers[wholesaler_name]['fix_path'])

                    if self.wholesalers[wholesaler_name]['fix_header']:
                        self.fix_header(path=f'core/data/wholesalers_inventory/{wholesaler_name}_inventory.csv', headers=\
                            self.wholesalers[wholesaler_name]['header'])

                    self.create_medicine_list(wholesaler_name, headers)

                    # Fixing barcodes
                    if self.wholesalers[wholesaler_name]['fix_barcode']:
                        dataframe = self.load_data_frame(path= \
                                                             f'core/data/wholesalers_inventory/medicine_list/{wholesaler_name}_medicine_list.csv')
                        self.fix_barcode(dataframe, column_name=\
                            headers[0], path= \
                                             f'core/data/wholesalers_inventory/medicine_list/{wholesaler_name}_medicine_list.csv',)



    def connect_from_ftp(self, server, username, password, name) -> ftplib.FTP:
        try:
            ftp_conn = ftplib.FTP(server)
            ftp_conn.login(username, password)
            ftp_conn.encoding = 'utf-8'
            return ftp_conn
        except ftplib.all_errors as e:
            self.supplier_errors[name] = {"error": f"{e}"}
            return False

    @staticmethod
    def fix_data(path):
        #open data to be fixed
        with open(path, mode='r') as file:
            new_file = []
            i = 0
            for line in file.readlines():
                if i == 0:
                    new_line = line.split(' ')
                    new_line_ = [f'{line}' for line in new_line if line != '']
                    for info_line in range(len(new_line_) - 1):
                        new_line_[info_line] = new_line_[info_line] + ';'
                    new_file.append(new_line_)
                else:
                    new_line = line.split('  ')
                    new_line = [f'{item}' for item in new_line if item != '']
                    for info in range(len(new_line) - 1):
                        new_line[info] = new_line[info] + ';'
                    new_file.append(new_line)

                i += 1

        #save new data
        with open(path, mode='w') as data:
            for lines in new_file:
                for line in lines:
                    data.write(line)

    @staticmethod
    def fix_header(path, headers):
        with open(path, mode='r+') as file:
            lines = file.readlines()
            lines.insert(0, f'{headers}\n' )
            file.seek(0)
            file.writelines(lines)

    @staticmethod
    def create_medicine_list(name, headers:list):
        data = pandas.read_csv(f'{PATH}/{name}_inventory.csv', encoding='utf-8',
                               encoding_errors='ignore', sep=';', on_bad_lines='skip')

        new_data = data[headers]
        new_data = new_data.dropna()
        new_data.to_csv(f'{PATH}/medicine_list/{name}_medicine_list.csv', index=False, sep=';')

    @staticmethod
    def fix_barcode(dataframe, column_name, path=None):
        df = dataframe
        new_column_as_string = df[column_name].astype('Int64').astype('str')
        df[column_name] = new_column_as_string
        if path:
            df.to_csv(path, index=False, sep=';')
        else:
            return df

    @staticmethod
    def load_data_frame(path, sep=';', skip='skip', header='infer', skip_rows=None) -> pandas.DataFrame:
        df = pandas.read_csv(path, sep=sep, on_bad_lines=skip, header=header, skiprows=skip_rows, encoding='utf8',
                             encoding_errors='ignore')
        return df

    def create_medicine_list_for_db(self):
        data_frames = self.load_wholesalers_list_data()
        # concat dataframe
        df = self.contact_data_frame(data_frames)
        # Adding columns to dataframe
        df.columns=['barcode', 'name']
        # converting barcode column in str
        df = self.converting_columns_to_str(df, 'barcode')
        #deleting duplicates
        no_duplicates = self.delete_duplicate_columns(df, 'barcode')
        #save file
        copy_df = no_duplicates.copy()
        no_duplicates_str = self.converting_columns_to_str(copy_df, 'barcode')
        self.save_dataframe_csv(no_duplicates_str, path='core/data/wholesalers_inventory/medicine_list/all.csv')

    def load_wholesalers_list_path(self):
        wholesalers_paths = []
        for name in self.wholesalers:
            if name not in self.supplier_errors:
                path = f'core/data/wholesalers_inventory/medicine_list/{name}_medicine_list.csv'
                wholesalers_paths.append(path)
        return wholesalers_paths

    def load_wholesalers_list_data(self):
        paths = self.load_wholesalers_list_path()
        dataframes = []
        for i in range(len(paths)):
            df = self.load_data_frame(path=paths[i], header=None, skip_rows=[0])
            dataframes.append(df)
        return dataframes

    @staticmethod
    def save_dataframe_csv(df: pandas.DataFrame, path):
        df.to_csv(path, sep=';', index=False)

    @staticmethod
    def contact_data_frame(dataframes: list) -> pandas.DataFrame:
        df = pandas.concat(dataframes, ignore_index=True)
        return df

    @staticmethod
    def converting_columns_to_str(df: pandas.DataFrame, column_name) -> pandas.DataFrame:
        new_barcode_column_str = df[column_name].astype('str')
        df[column_name] = new_barcode_column_str
        return df

    @staticmethod
    def delete_duplicate_columns(df:pandas.DataFrame, subset) -> pandas.DataFrame:
        new_no_duplicates = df.drop_duplicates(subset=subset)
        return new_no_duplicates


    # Create supplier list for database
    def create_supplier_list_for_database(self, suppliers: dict):
        for supplier_name in suppliers:
            list_path = f'core/data/wholesalers_inventory/{supplier_name}_inventory.csv'
            headers = suppliers[supplier_name]['database_headers']
            # Save list
            self.refactor_supplier_list(list_path=list_path, headers=headers, supplier_name=supplier_name)

    # refactor suppliers lists
    def refactor_supplier_list(self, list_path, headers: list, supplier_name):
        data: pandas.DataFrame = self.load_data_frame(list_path)
        new_df = data[headers]
        # save dataframe
        save_path = f'core/data/wholesalers_inventory/list_db/{supplier_name}.csv'
        # change columns
        new_df.columns = ['barcode', 'price', 'due_data', 'stock']
        df_no_nan = new_df.dropna(axis=0, how='any', subset=['barcode', 'stock'])
        # converting barcode into str
        df_full_stock = df_no_nan[(df_no_nan != 0).all(1)]
        if supplier_name == 'drocerca':
            df_fix_int = df_full_stock.copy()
            df_fix_int = self.fix_barcode(df_fix_int, column_name='barcode')
            df_full_stock = df_fix_int
        #save file
        self.save_dataframe_csv(df_full_stock, save_path)



    # Product prices

    # Load refactored list for suppliers

    def set_product_prices(self, dollar_value):
        dataframes = []
        for name in self.wholesalers:
            df_path = f'core/data/wholesalers_inventory/list_db/{name}.csv'
            dataframe = self.load_data_frame(df_path)
            # Adding supplier id column
            dataframe.insert(4, 'supplier_id', self.wholesalers[name]['supplier_id'])
            # Converting barcode column into string
            barcodes = self.converting_columns_to_str(dataframe, 'barcode')
            barcodes_list = barcodes['barcode'].tolist()
            #getting products id from db
            products = self.aux.select_barcodes(barcodes=barcodes_list)
            products_id = [product_id.id for product_id in products]
            # Drop barcode column
            new_df = dataframe.drop(columns=['barcode'])
            new_df.insert(0, 'product_id', products_id)
            if not self.wholesalers[name]['price_dollar']:
                new_df['price'] = round(new_df['price'] / dollar_value, 2)
            dataframes.append(new_df)
        return self.contact_data_frame(dataframes)




















