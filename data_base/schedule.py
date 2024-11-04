from .base import DataBase


class Schedule(DataBase):

    def create_user_table(self, user_tg_id: int):
        sql = f'''CREATE TABLE IF NOT EXISTS table_{user_tg_id}(
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER,
                month INTEGER,
                day INTEGER,
                time TEXT,
                desc TEXT)
                '''
        self.execute(sql, commit=True)

    def add_task(self, user_tg_id: int, year: int, month: int, day: int, time: str, desc: str):
        sql = f'''INSERT INTO table_{user_tg_id} (year, month, day, time, desc) VALUES (?, ?, ?, ?, ?)'''
        self.execute(sql, (year, month, day, time, desc), commit=True)

    def get_day(self, user_tg_id: int, year: int, month: int, day: int):
        sql = f'SELECT * FROM table_{user_tg_id} WHERE year=? AND month=? AND day=?'
        return self.execute(sql, (year, month, day), fetchall=True)

    def del_task(self, user_tg_id: int, task_id: int):
        sql = f'DELETE FROM table_{user_tg_id} WHERE task_id=?'
        self.execute(sql, (task_id,), commit=True)
