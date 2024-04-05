import pandas as pd

PATH = '../data'
class DataFrameHandler:

    def __init__(self, filename: str):
        self.filename = filename
        self.errors = {}

    def read_excel(self, path=PATH) -> pd.DataFrame:
        new_dataframe = pd.read_excel(f'{path}/{self.filename}')
        return new_dataframe

    def to_csv(self, dataframe: pd.DataFrame, path=PATH):
        # removing old extension
        dot_index = self.filename.rfind('.')
        dataframe.to_csv(f'{path}/{self.filename[:-(dot_index - 1)]}.csv', sep=';', index=False)


    def load_data_frame(self, path=PATH) -> pd.DataFrame:
        try:
            data_frame = pd.read_csv(f'{path}/{self.filename}', sep=';', on_bad_lines='skip', skiprows=None,
                                     encoding='utf-8', encoding_errors='ignore')
            return data_frame

        except FileNotFoundError as e:
            print('Sorry File Not Found Try again.')
            self.errors['Error': f'{e}']


    @staticmethod
    def extract_columns(dataframe: pd.DataFrame, columns: list) -> pd.DataFrame:
        new_dataframe = dataframe[columns]
        return new_dataframe

    @staticmethod
    def create_dataframe():
        data = {}
        new_dataframe = pd.DataFrame(data)
        return new_dataframe

    @staticmethod
    def contact_dataframes(dataframes: list, drop, subset='') -> pd.DataFrame:
        if drop:
            new_df = pd.concat(dataframes, ignore_index=True).drop(subset)
        else:
            new_df = pd.concat(dataframes, ignore_index=True)

        return new_df