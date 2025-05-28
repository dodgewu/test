import sqlite3
from tabulate import tabulate


class MySqlite():
    def __init__(self, db, **kwargs):
        self.db = db
        # 動態設定 keywords arguments
        for key, value in kwargs.items():
            setattr(self, key, value)

    def build_conn(self):
        """建立連線"""
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

    def create_table(self):
        # 使用instance 的constructor 來建造table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT ,
                age INTEGER
            )
            ''')
        self.conn.commit()

    def insert_data(self, sql_command=None):
        self.cursor.execute('''
        INSERT INTO users (name,age)
        VALUES (?,?)
        ''', ('shien', None))
        self.conn.commit()

    def select_data(self, sql_command=None):
        """顯示選擇資料並顯示在Terminal 中
            syntax SELECT * FROM users WHERE...
        """
        self.cursor.execute('SELECT * FROM users')
        # 先執行，再抓欄位名才有資料
        col_name = [desc[0] for desc in self.cursor.description]
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=col_name, tablefmt="grid"))

    def delete_table(self, sql_command=None):
        """清空db中的資料
            syntax: delete from users
        """
        self.cursor.execute("delete from users")
        self.conn.commit()

    def drop_table(self, sql_command=None):
        self.cursor.execute("DROP TABLE IF EXISTS users")
        self.conn.commit()


if __name__ == '__main__':
    my_sql = MySqlite(db='test.db')
    my_sql.build_conn()
    # my_sql.create_table()
    # my_sql.delete_table()
    # my_sql.select_data()
    # my_sql.insert_data()
    my_sql.drop_table()
    my_sql.select_data()
