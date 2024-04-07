import ftplib

PATH = 'core/data'


class FTP:

    def __init__(self, url: str, user: str, password: str, path: str, file_name, alias=''):
        self.url = url
        self.user = user
        self.password = password
        self.alias = alias
        self.path = path
        self.file_name = file_name
        self.error_log = {}
        self.server_connection = self.connect()

    def connect(self) -> ftplib.FTP:
        #connecto to ftp server
        try:
            ftp_conn = ftplib.FTP(self.url)
            ftp_conn.login(self.user, self.password)
            ftp_conn.encoding = 'utf-8'
            return ftp_conn

        except ftplib.all_errors as e:
            self.error_log[self.alias] = {"FTP connection error": f"{e}"}

        except UnicodeError as e:
            self.error_log[self.alias] = {"Unicode Error": f"{e}"}

    def download_file(self):
        #dowload files from ftp
        if self.server_connection:
            # change path directory
            try:
                self.server_connection.cwd(self.path)
            except ftplib.error_perm as e:
                self.add_error(error={'error': f'{e}'})
            else:
                # check if file size > 0 bites
                if self.check_file_size():
                    self.download()
                else:
                    self.add_error(error={'error': 'File size error must the greater than 0 bytes'})

                self.server_connection.quit()


    def download(self):
        with open(f"{PATH}/{self.alias}.csv", mode="wb") as file:
            self.server_connection.retrbinary(f'RETR {self.file_name}', file.write)


    def check_file_size(self):
        try:
            self.server_connection.sendcmd("TYPE I")
            return self.server_connection.size(self.file_name) > 0
        except ftplib.error_perm as e:
            self.add_error(error={'error:': f'{e}'})

    def add_error(self, error: dict):
        self.error_log[self.alias] = error


