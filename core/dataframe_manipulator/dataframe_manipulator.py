import pandas
import pandas as pd
from database import db, Product
from core.file_manipulator import file_manipulator as fm
from core.wholesalers import wholesalers

PATH = 'core/data'
class DataFrameHandler:

    def __init__(self, filename=''):
        self.filename = filename
        self.errors = {}
        self.dollar = 36.22


    ### READ DF ####

    def load_data_frame(self, filename='', path=PATH) -> pd.DataFrame:
        if not filename:
            filename = self.filename
        try:
            data_frame = pd.read_csv(f'{path}/{filename}', sep=';', on_bad_lines='skip', skiprows=None,
                                     encoding='utf-8', encoding_errors='ignore')
            return data_frame

        except FileNotFoundError as e:
            print('Sorry File Not Found Try again.')
            self.errors['Error': f'{e}']

    def read_excel(self, path=PATH) -> pd.DataFrame:
        new_dataframe = pd.read_excel(f'{path}/{self.filename}')
        return new_dataframe

    def to_csv(self, dataframe: pd.DataFrame, path=PATH):
        # removing old extension
        dot_index = self.filename.rfind('.')
        dataframe.to_csv(f'{path}/{self.filename[:-(dot_index - 1)]}.csv', sep=';', index=False)


    def dataframe_to_csv(self, dataframe: pd.DataFrame, path=PATH):
        dataframe.to_csv(f"{path}/{self.filename}", index=False, sep=';')



    ### Load DF for DB Operations ###

    def dataframe_products(self) -> pd.DataFrame:
        csv_files_path = fm.FileHandler().csv_file_list()
        df_list = [self.column_to_string(self.drop_nan(self.load_data_frame(filename=file_name),
                    columns=['barcode', 'name']),
                    column_name='barcode')
                   for file_name in csv_files_path]

        barcode_product_name_df_list = [self.extract_columns(dataframe=df,
                                    columns=['barcode', 'name']) for df in df_list]
        print(barcode_product_name_df_list[4])
        df_barcode_product_name = self.contact_dataframes(barcode_product_name_df_list, True, 'barcode')

        return df_barcode_product_name

    def dataframe_products_prices(self) -> pd.DataFrame:
        csv_file_path = fm.FileHandler().csv_file_list()
        df_list = []
        # creating df based on download files
        for file_name in csv_file_path:
            wholesaler = file_name[:file_name.rfind('.')]
            price_dollar = wholesalers[wholesaler]['price_dollar']
            supplier_id = wholesalers[wholesaler]['supplier_id']
            df = self.column_to_string(self.drop_nan(self.load_data_frame(filename=file_name),
                                        columns=['barcode', 'stock']), column_name='barcode')
            # Setting dollar price
            if not price_dollar:
                df['price_usd'] = round(df['price_usd'] / self.dollar, 2)

            # adding supplier id column
            df.insert(4, 'supplier_id', supplier_id)

            df_list.append(df)

        # Creating df list with not zero stock and only necessaries columns
        product_prices_df_list = [self.drop_zero(self.extract_columns(dataframe=df,
                            columns=['barcode', 'price_usd', 'due_date', 'stock', 'supplier_id']),
                                                 column='stock') for df in df_list]

        df_product_prices = self.contact_dataframes(product_prices_df_list, drop=False)

        product_id_barcode_df = self.dataframe_from_db(columns=['barcode', 'id'], db_table='products')

        merge_df = self.dataframe_merge(df_1=df_product_prices, df_2=product_id_barcode_df, column='barcode')

        # Delete barcode column
        merge_df['barcode'] = merge_df['id']
        # Reorder columns
        merge_df.rename(columns={'barcode': 'product_id', 'price_usd': 'price'}, inplace=True)
        # drop id column
        merge_df.drop(columns='id', inplace=True)

        return merge_df





    @staticmethod
    def dataframe_from_db(columns: list, db_table: str) -> pd.DataFrame:
        df_from_db = pd.read_sql(db_table, db.engine, coerce_float=False, columns=columns)
        return df_from_db




    ### DF OPERATIONS ###

    @staticmethod
    def dataframe_diff(df_1: pd.DataFrame, df_2: pd.DataFrame, column_compare: str):
        df_diff = df_2[~df_2[column_compare].isin(df_1[column_compare])]
        return df_diff


    @staticmethod
    def extract_columns(dataframe: pd.DataFrame, columns: list) -> pd.DataFrame:
        new_dataframe = dataframe[columns]
        return new_dataframe

    @staticmethod
    def contact_dataframes(dataframes: list, drop, subset='') -> pd.DataFrame:
        if drop:
            new_df = pd.concat(dataframes, ignore_index=True).drop_duplicates(subset)
        else:
            new_df = pd.concat(dataframes, ignore_index=True)

        return new_df

    @staticmethod
    def column_float_to_string(dataframe: pd.DataFrame, column_name: str) -> pd.DataFrame:
        str_column = dataframe[column_name].astype('int64').astype('str')
        dataframe[column_name] = str_column
        return dataframe
    @staticmethod
    def column_to_string(dataframe: pd.DataFrame, column_name: str) -> pd.DataFrame:
        str_column = dataframe[column_name].astype('str')
        dataframe[column_name] = str_column
        return dataframe

    @staticmethod
    def drop_nan(dataframe: pd.DataFrame, columns: list) -> pd.DataFrame:
        no_nan_df = dataframe.dropna(subset=columns)
        return no_nan_df
    @staticmethod
    def drop_zero(dataframe: pd.DataFrame, column: str) -> pd.DataFrame:
        no_zero_df = dataframe[dataframe[column] > 0 ]
        return no_zero_df


    @staticmethod
    def load_dataframe_from_db(columns: list, table_name: str) -> pd.DataFrame:
        df_from_db = pandas.read_sql(table_name, db.engine, coerce_float=False, columns=columns)
        return df_from_db

    @staticmethod
    def dataframe_diff(df_1: pd.DataFrame, df_2: pd.DataFrame, column: str):
        df_diff = df_2[~df_2[column].isin(df_1[column])]
        return df_diff

    @staticmethod
    def dataframe_merge(df_1: pd.DataFrame, df_2: pd.DataFrame, column: str) -> pd.DataFrame:
        merge_df = pd.merge(df_1, df_2, on=column)
        return merge_df