import sqlite3
from tabulate import tabulate


class MySqlite():
    """使用步驟:
    1. 建立實例，e.g. my_sql = MySqlite(db='CD8021.db')
    2. 建立連線，e.g. my_sql.build_conn()
    3. 建立table，e.g. my_sql.create_table()
    4. 進行sql 處理，e.g. my_sql.insert_data(sql_command="INSERT INTO users (name, age) VALUES ('shien', 18)")
    5. 關閉連線，e.g. my_sql.close_conn()
    """
    def __init__(self, db, **kwargs):
        self.db = db
        # 動態設定 keywords arguments
        for key, value in kwargs.items():
            setattr(self, key, value)

    def build_conn(self):
        """建立與db的連線"""
        try:
            # 選擇建立連線的db
            self.conn = sqlite3.connect(self.db)
            # 設定 instance 連線
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(
                f"There is an error occure while building to sqlite3.db({self.db}):\n{e}")

    def close_conn(self):
        """關閉連線"""
        self.conn.close()
        self.cursor.close()

    def create_table(self,sql_command=None):
        """在連線的db中建立table
            SYNTAX:
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT ,
                age INTEGER
            )
        """
        # 使用instance 的constructor 來建造table
        self.cursor.execute(sql_command)
        self.conn.commit()

    def insert_data(self, sql_command=None):
        """插入資料到db.table中
            syntax: INSERT INTO users (name,age) VALUES ('shien', 18)
        """
        self.cursor.execute(sql_command)
        self.conn.commit()

    def select_data(self, sql_command=None):
        """顯示選擇資料並顯示在Terminal 中
            syntax SELECT * FROM users WHERE...
        """
        self.cursor.execute(sql_command)
        # 先執行，再抓欄位名才有資料
        col_name = [desc[0] for desc in self.cursor.description]
        rows = self.cursor.fetchall()
        # 使用tabulate來美化顯示，maxcolwidths=寬度*col_name的個數  # 設定每一欄的最大寬度為30
        print(tabulate(rows, headers=col_name, tablefmt="grid",maxcolwidths=[40]*len(col_name)))

    def delete_table(self, sql_command=None):
        """清空db中的資料
            syntax: delete from users
        """
        self.cursor.execute(sql_command)
        self.conn.commit()

    def drop_table(self, sql_command=None):
        """ 刪除db中的table
            syntax: DROP TABLE IF EXISTS users
        """
        self.cursor.execute(sql_command)
        self.conn.commit()


if __name__ == '__main__':
    my_sql = MySqlite(db='CD8021.db')
    my_sql.build_conn()
    my_sql.create_table("""CREATE TABLE IF NOT EXISTS model (
                id INTEGER PRIMARY KEY aUTOINCREMENT,
                Docsis_version REAL,
                Firmware_version TEXT,
                sysDescr TEXT,
                docsDevSwVersion TEXT
                
            )""")
    my_sql.insert_data("""insert into model(Docsis_version,sysDescr,docsDevSwversion,Firmware_version) 
                       values(3.0,'normal','DOCSIS 3.1 Cable Modem <<HW_REV: V1.0; VENDOR: Compal Broadband Networks; BOOTR: 2.8.47alpha0; SW_REV: Cert_24.2.0.4; MODEL: MNB1525 CD8021>>'
                       ,'Cert_24.2.0.4')""")
    my_sql.insert_data("""insert into model(Docsis_version,sysDescr,docsDevSwversion,Firmware_version) 
                       values(3.0,'mac-14','MAC-14 test image for CW151'
                       ,'Cert_24.2.0.3 MAC14_ver')""")
    my_sql.insert_data("""insert into model(Docsis_version,sysDescr,docsDevSwversion,Firmware_version) 
                       values(3.1,'normal','DOCSIS 3.1 Cable Modem <<HW_REV: V1.0; VENDOR: Compal Broadband Networks; BOOTR: 2.8.47alpha0; SW_REV: Cert_24.2.0.4; MODEL: MNB1525 CD8021>>'
                       ,'Cert_24.2.0.4')""")
    my_sql.insert_data("""insert into model(Docsis_version,sysDescr,docsDevSwversion,Firmware_version) 
                       values(3.1,'normal','MAC-14 test image for CW151'
                       ,'Cert_24.2.0.3 MAC14_ver')""")
    my_sql.select_data("SELECT * FROM model")
