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




