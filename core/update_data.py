from .FTP.ftp import FTP
from .file_manipulator.file_manipulator import FileHandler
import os

PATH = 'core/data'

class UpdateData:
    def __init__(self, wholesalers: dict):
        self.wholesalers = wholesalers
        self.list_files = os.listdir(PATH)
        self.errors = []
        # self.download()

    def download(self):
        for wholesaler in self.wholesalers:
            # get data from ftps server
            url = self.wholesalers[wholesaler]['url']
            user = self.wholesalers[wholesaler]['user']
            password = self.wholesalers[wholesaler]['password']
            path = self.wholesalers[wholesaler]['path']
            file_name = self.wholesalers[wholesaler]['file_name']
            alias = wholesaler

            # download data
            new_connection = FTP(url=url, user=user, password=password, path=path, file_name=file_name, alias=alias)
            new_connection.download_file()

            # store errors
            if new_connection.error_log:
                self.errors.append(new_connection.error_log)

    def fix_file(self):
        for file in self.list_files:
            if file[:-4] in self.wholesalers.keys():
                # get data for file format
                csv = self.wholesalers[file[:-4]]['csv']
                has_header = self.wholesalers[file[:-4]]['has_header']
                header = self.wholesalers[file[:-4]]['header']

                if not csv:
                    new_csv_file = FileHandler(file_name=file)
                    new_csv_file.convert_to_csv()

                # rewrite header
                new_csv_file.rewrite_header(header, has_header=has_header)
