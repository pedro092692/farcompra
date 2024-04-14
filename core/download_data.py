from core.FTP.ftp import FTP
from flask import send_file

PATH = 'core/data'
class FtpDownload:
    def __init__(self, server, user, password, path, filename, alias):
        self.server = server
        self.user = user
        self.password = password
        self.path = path
        self.filename = filename
        self.alias = alias
        self.ftp_connect = FTP(url=self.server, user=self.user, password=self.password,
                               path=self.path,
                               file_name=self.filename,
                               alias=self.alias)

        # self.get_file = self.ftp_connect.download_file()

    def download_file(self):
        #download file
        self.ftp_connect.download_file()
        # open file
        return send_file(f'{PATH}/{self.alias}.csv', as_attachment=True)