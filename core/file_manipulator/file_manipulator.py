import os

import pandas as pd

from core.wholesalers import wholesalers
from core.dataframe_manipulator.dataframe_manipulator import DataFrameHandler
from core.wholesalers import wholesalers

PATH = 'core/data'
MANUAL_PATH = 'core/data/manual_uploads'
class FileHandler:

    def __init__(self, mode='auto', path=''):
        self.mode = mode
        if self.mode == 'auto':
            self.list_files = os.listdir(PATH)
            self.path = PATH
        else:
            self.path = path
            self.list_files = os.listdir(MANUAL_PATH)

        self.valid_extensions = ('.csv', '.xlsx', '.txt', 'xls')
        self.wholesalers = wholesalers


    ### Fix csv, xlsx, txt files ###

    def rewrite_header(self, file_name, header, has_header):
        new_path = f'{self.path}/{file_name}'
        with open(new_path, mode='r+', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            if has_header:
                if file_name == 'drovencentro.csv':
                    lines[0] = f'{header}\n'
                    # lines[1:9] = '' for second xlsx file
                    lines[1] = ''
                else:
                    lines[0] = f'{header}\n'

            else:
                lines.insert(0, f'{header}\n')
            file.seek(0)
            file.writelines(lines)

    def convert_to_csv(self, file_name, extension):
        if extension == '.csv' and file_name == 'dronena.csv':
            with open(f'{self.path}/{file_name}', mode='r') as file:
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
            with open(f'{self.path}/{file_name}', mode='w') as data:
                for lines in new_file:
                    for line in lines:
                        data.write(line)

        elif extension == '.xlsx':
            pd_handler = DataFrameHandler(filename=file_name)
            pd_handler.to_csv(pd_handler.read_excel(path=self.path, filename=file_name), path=self.path, filename=file_name)

        elif extension == '.csv' and file_name == 'insuaminca':
            with open(f'{self.path}/{file_name}', mode='r') as infile, open(f'{self.path}'/{file_name}, mode='w') as outfile:
                content = infile.read().replace('\n', '')
                outfile.write(content)
        elif extension == '.csv' and file_name == 'drolanca.csv':
            self.fix_drolanca(file_name=file_name)


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
            iterate = os.listdir(self.path)
        else:
            iterate = self.list_files
        for file in iterate:
            # remove not csv files
            if kwargs.get('remove'):
                if file.endswith(('.xlsx', '.txt')):
                    os.remove(f'{self.path}/{file}')
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
                            data_frame = function(filename=file).load_data_frame(path=self.path)
                            no_nan_df = function.drop_nan(data_frame, columns=['barcode'])
                            str_bar_code_df = function(filename=file).column_float_to_string(no_nan_df, 'barcode')
                            function(filename=file).dataframe_to_csv(dataframe=str_bar_code_df, path=self.path,
                                                                     filename=file)

    def remove_all_files(self, path):
        path_files = os.listdir(path)
        for file in path_files:
            if file.endswith(self.valid_extensions):
                os.remove(f"{path}/{file}")

    def csv_file_list(self) -> list:
        files = []
        for file in self.list_files:
            if file.endswith('.csv'):
                files.append(file)
        return files

    def fix_drolanca(self, file_name):
        with open(f'{self.path}/{file_name}', mode='r', encoding="latin-1") as file:
            new_file = []
            i = 0
            for line in file.readlines():
                row = line.split(';')
                product_info = row[2].split(' Vence:')
                product_info[0] = product_info[0].replace(' -', '').rstrip()
                product_info[1] = product_info[1].lstrip()
                product_name = product_info[0]
                due_date = product_info[1]
                row[2] = product_name
                row[10] = due_date
                line = ';'.join(row)
                new_file.append(line)

        with open(f'{self.path}/{file_name}', mode='w', encoding="latin-1") as data:
            for lines in new_file:
                for line in lines:
                    data.write(line)

















