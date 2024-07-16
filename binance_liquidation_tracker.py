import websocket
import json
import pandas as pd
import pytz
from typing import List, Optional
from tabulate import tabulate  

class BinanceLiquidationFeed:
    SOCKET_URL = 'wss://fstream.binance.com/ws/!forceOrder@arr'
    
    def __init__(self, minimum_total_dollars: float = 0, tickers: Optional[List[str]] = None):
        self.minimum_total_dollars = minimum_total_dollars
        self.tickers = tickers
        self.tz = pytz.timezone('Asia/Seoul')
        
    def start(self):
        websocket.enableTrace(False)  # Disable for cleaner output
        self.ws = websocket.WebSocketApp(
            self.SOCKET_URL,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        self.ws.run_forever()
        
    def on_message(self, ws, message):
        data = json.loads(message)
        order_data = data['o']
        
        new_row = self.process_order(order_data)
        
        if self.passes_filters(new_row):
            self.print_liquidation(new_row)
        
    def process_order(self, order_data):
        trade_time = pd.to_datetime(order_data['T'], unit='ms', utc=True).tz_convert(self.tz)
        return {
            'Symbol': order_data['s'],
            'Side': order_data['S'],
            'Price': float(order_data['p']),
            'Quantity': float(order_data['q']),
            'Total($)': round(float(order_data['p']) * float(order_data['q']), 2),
            'Trade Time': trade_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
    def passes_filters(self, row):
        ticker_filter = self.tickers is None or row['Symbol'] in self.tickers
        value_filter = row['Total($)'] >= self.minimum_total_dollars
        return ticker_filter and value_filter
    
    def print_liquidation(self, row):
        table = [[k, v] for k, v in row.items()]
        print("\n=== Liquidation Event ===")
        print(tabulate(table, headers=['Field', 'Value'], tablefmt='pretty'))
        print("=========================\n")
    
    def on_error(self, ws, error):
        print(f'Error: {error}')
        
    def on_close(self, ws, close_status_code, close_msg):
        print(f'Connection closed: {close_status_code} - {close_msg}')
        
    def on_open(self, ws):
        print('Connection opened. Waiting for liquidation events...\n')

if __name__ == "__main__":
    feed = BinanceLiquidationFeed(
        minimum_total_dollars=100,
        tickers=['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT']
    )
    feed.start()