import os

import pandas as pd

from core.wholesalers import wholesalers
from core.dataframe_manipulator.dataframe_manipulator import DataFrameHandler
from core.wholesalers import wholesalers

PATH = 'core/data'
class FileHandler:

    def __init__(self, mode='auto', path=''):
        self.mode = mode
        if self.mode == 'auto':
            self.list_files = os.listdir(PATH)
        else:
            self.list_files = os.listdir(path)
        self.valid_extensions = ('.csv', '.xlsx', '.txt')
        self.wholesalers = wholesalers


    ### Fix csv, xlsx, txt files ###
    @staticmethod
    def rewrite_header(file_name, header, has_header):
        new_path = f'{PATH}/{file_name}'
        with open(new_path, mode='r+', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            if has_header:
                lines[0] = f'{header}\n'
            else:
                lines.insert(0, f'{header}\n')
            file.seek(0)
            file.writelines(lines)

    @staticmethod
    def convert_to_csv(file_name, extension):
        if extension == '.csv' and file_name == 'dronena.csv':
            with open(f'{PATH}/{file_name}', mode='r') as file:
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

            # save new data
            with open(f'{PATH}/{file_name}', mode='w') as data:
                for lines in new_file:
                    for line in lines:
                        data.write(line)

        elif extension == '.xlsx':
            pd_handler = DataFrameHandler(filename=file_name)
            pd_handler.to_csv(pd_handler.read_excel())

    def convert_all_to_csv(self):
        self.iterate_over_path(self.convert_to_csv, csv='csv')
        self.iterate_over_path(None, remove='remove')
        self.rewrite_all_header()
        self.convert_barcodes_to_str()


    #fix barcodes int64 to str
    def convert_barcodes_to_str(self):
        self.iterate_over_path(DataFrameHandler, fix_barcode='fix_barcode')

    def rewrite_all_header(self):
        self.iterate_over_path(self.rewrite_header, header='header', has_header='has_header')

    def iterate_over_path(self, function, **kwargs):
        if kwargs.get('header'):
            iterate = os.listdir(PATH)
        else:
            iterate = self.list_files

        for file in iterate:
            # remove not csv files
            if kwargs.get('remove'):
                if file.endswith(('.xlsx', '.txt')):
                    os.remove(f'{PATH}/{file}')
                return
            if file.endswith(self.valid_extensions):
                dot_extension_index = file.rfind('.')
                if file[:dot_extension_index] in self.wholesalers.keys():
                    # convert in csv
                    if kwargs.get('csv'):
                        if not self.wholesalers[file[:dot_extension_index]][kwargs['csv']]:
                            function(extension=file[dot_extension_index:], file_name=file)
                    # rewrite all headers
                    if kwargs.get('header') and kwargs.get('has_header'):
                        function(file_name=file, header=self.wholesalers[file[:dot_extension_index]]['header'],
                                 has_header=self.wholesalers[file[:dot_extension_index]]['has_header'])

                    if kwargs.get('fix_barcode'):
                        if self.wholesalers[file[:dot_extension_index]]['fix_barcode']:
                            data_frame = function(filename=file).load_data_frame()
                            no_nan_df = function.drop_nan(data_frame, columns=['barcode'])
                            str_bar_code_df = function(filename='').column_float_to_string(no_nan_df, 'barcode')
                            function(filename=file).dataframe_to_csv(dataframe=str_bar_code_df)


    def csv_file_list(self) -> list:
        files = []
        for file in self.list_files:
            if file.endswith(self.valid_extensions):
                files.append(file)
        return files

















