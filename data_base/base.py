import psycopg2

import os


class DataBase:
    _instance = None
    _ip_address = os.getenv('IP_ADDRESS')
    _db_name = os.getenv('DB_NAME')
    _user_name = os.getenv('USER_NAME')
    _password = os.getenv('PASSWORD')

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def execute(self, sql: str, parameters: tuple = tuple(),
                fetchone=False, fetchall=False, commit=False):
        connection = psycopg2.connect(
            user=self._user_name,
            password=self._password,
            dbname=self._db_name,
            host=self._ip_address,
        )
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    @staticmethod
    def extract_kwargs(sql: str, parameters: dict, _and: bool = True) -> tuple:
        sql += (' AND ' if _and else ', ').join([f'{key} = ?' for key in parameters])
        return sql, tuple(parameters.values())

    def create_main_table(self):
        sql = f'''CREATE TABLE IF NOT EXISTS table_admins(
            entry_id        SERIAL PRIMARY KEY,
            user_tg_id      NUMERIC,
            scheduler_tg_id NUMERIC,
            scheduler_title CHARACTER VARYING(30),
            UNIQUE (user_tg_id, scheduler_tg_id)
            )'''
        self.execute(sql, commit=True)

    def create_user_table(self, user_tg_id):
        sql = f'''CREATE TABLE IF NOT EXISTS table_{user_tg_id}(
            task_id         SERIAL PRIMARY KEY,
            year            NUMERIC,
            month           NUMERIC,
            day             NUMERIC,
            time            CHARACTER VARYING(6),
            description     CHARACTER VARYING(500)
            )'''
        self.execute(sql, commit=True)

    def add_task(self, user_tg_id: int, year: int, month: int, day: int, time: str, desc: str):
        sql = f'INSERT INTO table_{user_tg_id} (year, month, day, time, description) VALUES (%s, %s, %s, %s, %s)'
        self.execute(sql, (year, month, day, time, desc), commit=True)

    def get_day(self, user_tg_id: int, year: int, month: int, day: int):
        sql = f'SELECT * FROM table_{user_tg_id} WHERE year=%s AND month=%s AND day=%s'
        return self.execute(sql, (year, month, day), fetchall=True)

    def get_month(self, user_tg_id: int, year: int, month: int):
        sql = f'SELECT day FROM table_{user_tg_id} WHERE year=%s AND month=%s'
        return self.execute(sql, (year, month), fetchall=True)

    def del_task(self, user_tg_id: int, task_id: int):
        sql = f'DELETE FROM table_{user_tg_id} WHERE task_id=%s'
        self.execute(sql, (task_id,), commit=True)

    def add_scheduler(self, user_tg_id: int, scheduler_tg_id: int, scheduler_title: str):
        sql = f'''INSERT INTO table_admins (user_tg_id, scheduler_tg_id, scheduler_title) VALUES 
            (%s, %s, %s) ON CONFLICT (user_tg_id, scheduler_tg_id) DO NOTHING'''
        return self.execute(sql, (user_tg_id, scheduler_tg_id, scheduler_title), commit=True)

    def load_schedulers(self, user_tg_id: int):
        sql = f'SELECT scheduler_tg_id, scheduler_title FROM table_admins WHERE user_tg_id=%s'
        return self.execute(sql, (user_tg_id,), fetchall=True)

    def del_scheduler(self, user_tg_id: int, scheduler_tg_id: int):
        sql = f'DELETE FROM table_admins WHERE user_tg_id=%s AND scheduler_tg_id=%s'
        self.execute(sql, (user_tg_id, scheduler_tg_id), commit=True)

    def count_tasks(self, user_tg_id: int, year: int, month: int):
        sql = f'SELECT * FROM table_{user_tg_id} WHERE year=%s AND month=%s'
        return self.execute(sql, (year, month), fetchall=True)
