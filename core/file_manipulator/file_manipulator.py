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
            self.fix_dronena(file_name=file_name)

        elif extension == '.xlsx':
            pd_handler = DataFrameHandler(filename=file_name)
            pd_handler.to_csv(pd_handler.read_excel(path=self.path, filename=file_name), path=self.path, filename=file_name)

        elif extension == '.csv' and file_name == 'insuaminca':
            with open(f'{self.path}/{file_name}', mode='r') as infile, open(f'{self.path}'/{file_name}, mode='w') as outfile:
                content = infile.read().replace('\n', '')
                outfile.write(content)

        elif extension == '.csv' and file_name == 'drolanca.csv':
            self.fix_drolanca(file_name=file_name)
        elif extension == '.csv' and file_name == 'drovencentro.csv':
            self.fix_drovencentro(file_name=file_name)



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
            for line in file.readlines():
                line_divided = line.split(';')

                internal_code = line_divided[0]
                barcode = line_divided[1]
                name = line_divided[2].split('Vence:')[0].replace('-', '').rstrip()
                due_date = line_divided[2].split('Vence:')[1].lstrip()
                price = float(line_divided[8].replace(',', '.'))
                stock = int(line_divided[9])
                new_file.append(f'{internal_code};{barcode};{name};{due_date};{price};{stock}\n')

        with open(f'{self.path}/{file_name}', mode='w', encoding="latin-1") as data:
            for line in new_file:
                data.write(line)

    def fix_drovencentro(self, file_name):
        with open(f'{self.path}/{file_name}', mode='r', encoding='latin-1') as file:
            refactor_lines = []
            for line in file.readlines():
                cod = line[0:11]
                des = line[11:51]
                stock = int(line[54:60])
                price = int(line[60:70]) / 10
                discount = int(line[71:74]) / 100
                final_price = round(price * (1 - discount), 2)
                barcode = str(line[97:115])
                refactor_line = f'{cod};{des.strip()};{float(final_price)};{stock};{barcode.strip()}\n'
                refactor_lines.append(refactor_line)

        with open(f'{self.path}/{file_name}', mode='w', encoding='latin-1') as data:
            for line in refactor_lines:
                data.write(line)

    def fix_dronena(self, file_name):
        with open(f'{self.path}/{file_name}', mode='r') as file:
            new_line = []
            for line in file.readlines()[1:]:
                internal_code = line[0:5]
                name = line[7:48].rstrip()
                price = float(line[49:58])
                stock = int(line[64:73])
                discount = float(line[97:104])
                final_price = round(price * (1 - (discount / 100)), 2)
                barcode = line[130:144].rstrip()
                due_date = line[192:199]
                new_line.append(f'{internal_code};{name};{final_price};{stock};{barcode};{due_date}\n')

        with open(f'{self.path}/{file_name}', mode='w') as data:
            for line in new_line:
                data.write(line)

















