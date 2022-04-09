import cx_Oracle


class database:
    def __init__(self):
        lib_dir = "F:\instantclient_21_3"
        try:
            cx_Oracle.init_oracle_client(lib_dir)
        except Exception as err:
            print(err)

        self.user = "bd103"
        self.password = "bd103"
        self.hostname = "bd-dc.cs.tuiasi.ro:1539/orcl"
        self.success=0

    def connect(self):
        try:
            print("Connecting...")
            self.con = cx_Oracle.connect(self.user, self.password, self.hostname, encoding="UTF-8")
            print("Done")
            self.success=1
            self.cursor = self.con.cursor()
        except Exception as err:
            self.success=0
            print(err)

    def execute_query(self, query):
        answer = self.cursor.execute(query)
        return answer
