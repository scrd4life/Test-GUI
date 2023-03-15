import json

import psycopg2
import io
import csv


class DatabaseManager:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.conn = {}
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
            return "Error"

    def create_table(self, table_name, columns, primary_key):
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cur:
            column_str = ", ".join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_str}, PRIMARY KEY ({primary_key}))"
            cur.execute(query)
            self.conn.commit()

    def insert_stock_price(self, table_name, data):
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cur:
            column_names = ["time", "open", "high", "low", "close", "volume"]
            placeholders = ",".join(["%s" for _ in column_names])
            query = f"INSERT INTO {table_name} ({','.join(column_names)}) VALUES ({placeholders}) ON CONFLICT (time) DO NOTHING"
            values = [(row['time'], row['open'], row['high'], row['low'], row['close'], row['volume']) for row in data]
            cur.executemany(query, values)
            self.conn.commit()

    def update_data(self, table_name, update_data, condition):
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cur:
            update_str = ", ".join([f"{col_name}=%s" for col_name in update_data.keys()])
            condition_str = " AND ".join([f"{col_name}=%s" for col_name in condition.keys()])
            values = tuple(list(update_data.values()) + list(condition.values()))
            query = f"UPDATE {table_name} SET {update_str} WHERE {condition_str}"
            cur.execute(query, values)
            self.conn.commit()

    def retrieve_data(self, table_name, columns=None, condition=None):
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cur:
            column_str = "*" if columns is None else ", ".join(columns)
            condition_str = "" if condition is None else " WHERE " + " AND ".join(
                [f"{col_name}=%s" for col_name in condition.keys()])
            values = None if condition is None else tuple(condition.values())
            query = f"SELECT {column_str} FROM {table_name}{condition_str}"
            cur.execute(query, values)
            return cur.fetchall()

    def get_tables(self):
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cur:
            query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND " \
                    "table_type='BASE TABLE'"
            cur.execute(query)
            return [table[0] for table in cur.fetchall()]

    def get_last_date(self, table_name):
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cur:
            query = f"SELECT MAX(time) FROM {table_name}"
            cur.execute(query)
            return cur.fetchone()[0]

    def store_news(self, data, symbol):
        with self.conn.cursor() as cur:
            items = json.loads(data)["feed"]
            for item in items:
                overall_sentiment_score = item["overall_sentiment_score"]
                time_published = item['time_published']
                for ticker_sentiment in item["ticker_sentiment"]:
                    if ticker_sentiment["ticker"]:
                        ticker = ticker_sentiment["ticker"]
                        relevance_score = ticker_sentiment["relevance_score"]
                        ticker_sentiment_score = ticker_sentiment["ticker_sentiment_score"]
                        cur.execute(f"INSERT INTO {symbol}_news (overall_sentiment_score, relevance_score, "
                                    f"ticker_sentiment_score, time_published) VALUES (%s, %s, %s, %s)",
                                    (overall_sentiment_score, relevance_score, ticker_sentiment_score,
                                     time_published))

            self.conn.commit()
            cur.close()
            self.conn.close()
