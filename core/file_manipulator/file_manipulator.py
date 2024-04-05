import os
from core.wholesalers import wholesalers
from core.dataframe_manipulator.dataframe_manipulator import DataFrameHandler

PATH = 'core/data'
class FileHandler:

    def __init__(self, file_name):
        self.file_name = file_name

    def rewrite_header(self, header, has_header):
        new_path = f'{PATH}/{self.file_name}'
        with open(new_path, mode='r+', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            if has_header:
                lines[0] = f'{header}\n'
            else:
                lines.insert(0, f'{header}\n')
            file.seek(0)
            file.writelines(lines)

    def convert_to_csv(self, extension):
        new_path = f'{PATH}/{self.file_name}'
        if extension == '.csv' and self.file_name == 'dronena.csv':
            with open(new_path, mode='r') as file:
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
            with open(new_path, mode='w') as data:
                for lines in new_file:
                    for line in lines:
                        data.write(line)

        elif extension == '.xlsx':
            pd_handler = DataFrameHandler(filename=self.file_name)
            pd_handler.to_csv(pd_handler.read_excel())


