import psycopg2


class DatabaseManager:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            return self.conn
        except:
            return

    def create_table(self, table_name, columns):
        with self.conn.cursor() as cur:
            column_str = ", ".join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_str})"
            cur.execute(query)
            self.conn.commit()

    def insert_data(self, table_name, data):
        with self.conn.cursor() as cur:
            column_names = ", ".join(data.keys())
            values = tuple(data.values())
            placeholders = ", ".join(["%s" for _ in data.values()])
            query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
            cur.execute(query, values)
            self.conn.commit()

    def update_data(self, table_name, update_data, condition):
        with self.conn.cursor() as cur:
            update_str = ", ".join([f"{col_name}=%s" for col_name in update_data.keys()])
            condition_str = " AND ".join([f"{col_name}=%s" for col_name in condition.keys()])
            values = tuple(list(update_data.values()) + list(condition.values()))
            query = f"UPDATE {table_name} SET {update_str} WHERE {condition_str}"
            cur.execute(query, values)
            self.conn.commit()

    def retrieve_data(self, table_name, columns=None, condition=None):
        with self.conn.cursor() as cur:
            column_str = "*" if columns is None else ", ".join(columns)
            condition_str = "" if condition is None else " WHERE " + " AND ".join(
                [f"{col_name}=%s" for col_name in condition.keys()])
            values = None if condition is None else tuple(condition.values())
            query = f"SELECT {column_str} FROM {table_name}{condition_str}"
            cur.execute(query, values)
            return cur.fetchall()
