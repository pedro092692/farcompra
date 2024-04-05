from .FTP.ftp import FTP
from .file_manipulator.file_manipulator import FileHandler
import os

PATH = 'core/data'

class UpdateData:
    def __init__(self, wholesalers: dict):
        self.wholesalers = wholesalers
        self.list_files = os.listdir(PATH)
        self.valid_extensions = ('.csv', '.xlsx', '.txt')
        self.errors = []
        self.download()

    def download(self):
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
                new_connection.download_file()
                # store errors
                if new_connection.error_log:
                    self.errors.append(new_connection.error_log)

    def convert_file_in_csv(self):
        # converting all file in valid csv
        for file in self.list_files:
            if file.endswith(self.valid_extensions):
                # search .extension index
                extension_dot_index = file.rfind('.')
                if file[:extension_dot_index] in self.wholesalers.keys():
                    # get data for file format
                    csv = self.wholesalers[file[:extension_dot_index]]['csv']
                    # create New filehandler object
                    new_csv_file = FileHandler(file_name=file)
                    if not csv:
                        new_csv_file.convert_to_csv(extension=file[extension_dot_index:])

        self.remove_not_csv_files()
        self.rewrite_headers()

    def rewrite_headers(self):
        for file in os.listdir(PATH):
            if file.endswith(self.valid_extensions):
                # search .extension index
                extension_dot_index = file.rfind('.')
                if file[:extension_dot_index] in self.wholesalers.keys():
                    has_header = self.wholesalers[file[:extension_dot_index]]['has_header']
                    header = self.wholesalers[file[:extension_dot_index]]['header']
                    # create new file handler object
                    csv_file = FileHandler(file_name=file)
                    csv_file.rewrite_header(header=header, has_header=has_header)
    def remove_not_csv_files(self):
        for file in self.list_files:
            if file.endswith(('.xlsx', '.txt')):
                os.remove(f'{PATH}/{file}')



