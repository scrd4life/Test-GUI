import json
import io
import csv
import requests
import time
from datetime import datetime, timedelta


class Stockdata:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def check_table(self, symbol):
        tables = self.db_manager.get_tables()
        return symbol in tables

    def get_last_date(self, symbol):
        last_date = self.db_manager.get_last_date(symbol)
        if last_date is not None:
            return last_date.date()

    def download_stock_prices(self, symbol):
        last_date = self.get_last_date(symbol)
        print(last_date)
        if last_date is None:
            start_date = datetime.now().date() - timedelta(days=2 * 365)
        else:
            start_date = last_date + timedelta(days=1)
        end_date = datetime.now().date()
        print(start_date)
        url = "https://www.alphavantage.co/query?"
        function = "TIME_SERIES_INTRADAY_EXTENDED"
        api_key = "VCVT4TNZBRSU8V86"
        time_diff = (end_date - start_date).days
        slices = []
        for i in range(1, (time_diff // 30) + 2):
            if i == 1:
                start_day = 1
            else:
                start_day = (i - 1) * 30 + 1
            end_day = i * 30
            if end_day > time_diff:
                end_day = time_diff
            if end_day >= start_day:
                month = str((i - 1) % 12 + 1)
                year = str(1 + (i - 1) // 12)
                slices.append(f"year{year}month{month}")
                print(slices)
        slices = []
        timer_start = time.monotonic()
        for i, slice in enumerate(slices):
            with requests.Session() as s:
                time_elapsed = time.monotonic() - timer_start
                time_remaining = max(0, i * 13 - time_elapsed)
                if time_remaining > 0:
                    print(f"Waiting for {time_remaining:.2f} seconds to avoid exceeding API rate limit...")
                    time.sleep(time_remaining)
                query = f"function={function}&symbol={symbol}&interval=1min&apikey={api_key}&slice={slice}"
                response = s.get(url + query)
                decoded_content = response.content.decode('utf-8')
                csvdata = csv.DictReader(io.StringIO(decoded_content))
                next(csvdata)
                all_data = []
                for row in csvdata:
                    rowtime = datetime.strptime(row['time'], '%Y-%m-%d %H:%M:%S')
                    open_price = float(row['open'])
                    high_price = float(row['high'])
                    low_price = float(row['low'])
                    close_price = float(row['close'])
                    volume = int(row['volume'])
                    row_dict = {'time': str(rowtime), 'open': open_price,
                                'high': high_price, 'low': low_price, 'close': close_price,
                                'volume': volume}
                    all_data.append(row_dict)
                if response.status_code == 200:
                    print(f"Downloaded data for slice {slice}")
                    self.db_manager.insert_stock_price(table_name=symbol, data=all_data)
                else:
                    print(f"Error downloading data for slice {slice}")
        function = "NEWS_SENTIMENT"
        time_from = "20210303T0000"

    def create_table(self, symbol):
        columns = {
            "time": "timestamp",
            "open": "float",
            "high": "float",
            "low": "float",
            "close": "float",
            "volume": "int"
        }
        self.db_manager.create_table(symbol, columns, "time")

    def download_data(self, symbol):
        if not self.check_table(symbol):
            self.create_table(symbol)
        self.download_stock_prices(symbol)
        self.download_news(symbol)

    def download_news(self, symbol):
        if not self.check_table(symbol+"_news"):
            self.create_table(symbol+"_news")
        url = "https://www.alphavantage.co/query"
        function = "NEWS_SENTIMENT"
        api_key = "VCVT4TNZBRSU8V86"
        query = f"function={function}&symbol={symbol}&apikey={api_key}"
        response = requests.get(url, params=query)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error downloading news sentiment data for {symbol}: {response.status_code}")
            return None

