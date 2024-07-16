# Binance-Liquidation-Tracker


# Binance Futures Liquidation Feed

This Python script connects to the Binance Futures WebSocket API to stream real-time liquidation events. It filters and displays liquidation orders based on user-defined criteria.

## Features

- Real-time streaming of Binance Futures liquidation events
- Customizable filters for minimum liquidation value and specific trading pairs
- Clean, human-readable output format
- Timezone conversion to Asia/Seoul time but change this to whatever you need

## Requirements

- Python 3.7+
- websocket-client
- pandas
- pytz
- tabulate

## Installation

1. Clone this repository or download the script.

2. Install the required Python packages:

   ```
   pip install websocket-client pandas pytz tabulate
   ```

## Usage

1. Open the script in a text editor.

2. Modify the following parameters in the `__main__` section as needed:

   ```python
   feed = BinanceLiquidationFeed(
       minimum_total_dollars=100,
       tickers=['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT']
   )
   ```

   - `minimum_total_dollars`: The minimum USD value of liquidations to display
   - `tickers`: A list of specific trading pairs to monitor (or `None` to monitor all)

3. Run the script:

   ```
   python binance_liquidation_feed.py
   ```

4. The script will connect to the Binance WebSocket and start displaying liquidation events that meet your criteria.

## Output Format

Each liquidation event is displayed in a table format:

```
=== Liquidation Event ===
+------------+----------------------+
| Field      | Value                |
+============+======================+
| Symbol     | BTCUSDT              |
+------------+----------------------+
| Side       | SELL                 |
+------------+----------------------+
| Price      | 63108.65             |
+------------+----------------------+
| Quantity   | 0.002                |
+------------+----------------------+
| Total($)   | 126.22               |
+------------+----------------------+
| Trade Time | 2024-07-16 16:39:23  |
+------------+----------------------+
=========================
```

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/binance-liquidation-feed/issues) if you want to contribute.

```
