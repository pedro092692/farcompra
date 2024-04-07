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
            self.server_connection.cwd(self.path)
            # check if file size > 0 bites
            try:
                if self.check_file_size():
                    self.download()
                else:
                    self.add_error(error={"Error": "file size error"})

            except ftplib.error_perm as e:
                self.server_connection.sendcmd("TYPE I")
                if self.check_file_size():
                    self.download()
                else:
                    self.add_error(error={"Error": "file size error"})

            self.server_connection.quit()


    def download(self):
        with open(f"{PATH}/{self.alias}.csv", mode="wb") as file:
            self.server_connection.retrbinary(f'RETR {self.file_name}', file.write)

    def check_file_size(self):
        return self.server_connection.size(self.file_name) > 0

    def add_error(self, error: dict):
        self.error_log[self.alias] = error


