from flask import send_file
from core.wholesalers import wholesalers
from core.FTP.ftp import FTP
from core.file_manipulator.file_manipulator import FileHandler
PATH = 'core/data'
class Supplier:

    def __init__(self, name=''):
        if name:
            self.name = name
            self.server_url = wholesalers[self.name]['url']
            self.user_name = wholesalers[self.name]['user']
            self.password = wholesalers[self.name]['password']
            self.path = wholesalers[self.name]['path']
            self.file_name = wholesalers[self.name]['file_name']

    def download_file(self):
        file_handler = FileHandler()
        ftp_con = FTP(url=self.server_url, user=self.user_name, password=self.password,
                      path=self.path, file_name=self.file_name, alias=self.name)
        ftp_con.download_file()
        #send to user
        with open(f'{PATH}/{self.name}.csv', mode='rb') as local_file:
            file_data = local_file.read()
        # delete file
        file_handler.remove_all_files(path=PATH)
        return file_data

    @staticmethod
    def supplier_list():
        suppliers = {'ftp':[], 'no_ftp': []}
        for key in wholesalers:
            if wholesalers[key]['url']:
                suppliers['ftp'].append(key)
            else:
                suppliers['no_ftp'].append(key)
        return suppliers


