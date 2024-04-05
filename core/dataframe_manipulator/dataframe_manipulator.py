import pandas as pd

PATH = 'core/data'
class DataFrameHandler:

    def __init__(self, filename: str):
        self.filename = filename

    def read_excel(self, path=PATH) -> pd.DataFrame:
        new_dataframe = pd.read_excel(f'{path}/{self.filename}')
        return new_dataframe

    def to_csv(self, dataframe: pd.DataFrame, path=PATH):
        # removing old extension
        dot_index = self.filename.rfind('.')
        dataframe.to_csv(f'{path}/{self.filename[:-(dot_index - 1)]}.csv', sep=';', index=False)


