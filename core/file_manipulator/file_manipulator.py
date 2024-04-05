import os
from core.wholesalers import wholesalers

PATH = 'core/data'
class FileHandler:

    def __init__(self, file_name):
        self.file_name = file_name

    def rewrite_header(self, header, has_header):
        new_path = f'{PATH}/{self.file_name}'
        with open(new_path, mode='r+') as file:
            if has_header:
                lines = file.readlines()
                lines[0] = f'{header}\n'
            else:
                lines = file.readlines
                lines.insert(0, f'{header}\n')
            file.seek(0)
            file.writelines(lines)
    def convert_to_csv(self):
        new_path = f'{PATH}/{self.file_name}'
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


