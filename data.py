from yahoo_fin import stock_info as si
import os
from tqdm import tqdm
import talib
import glob


if not os.path.exists('data'):
    os.mkdir('data')
else:
    files = glob.glob('data/*')
    if len(files) > 0:
        for f in tqdm(files, desc='Wiping out previously downloaded files'):
            os.remove(f)

nasdaq_ticker_list = si.tickers_nasdaq()
# print(nasdaq_ticker_list)

for symbol in tqdm(nasdaq_ticker_list, desc='Downloading stock historicals'):
    try:
        # retrieve stock info
        stock = si.get_data(symbol)
        stock = stock.drop(['adjclose', 'ticker'], axis=1)

        # Relative Strength Index (RSI)
        stock['rsi'] = talib.RSI(stock['close'], timeperiod=14)

        # Commodity Channel Index (CCI)
        stock['cci'] = talib.CCI(stock['high'], stock['low'], stock['close'], timeperiod=14)

        # Percentage Price Oscillator (PPO)
        stock['ppo'] = talib.PPO(stock['close'], fastperiod=12, slowperiod=26, matype=0)

        # Money Flow Index (MFI)
        stock['mfi'] = talib.MFI(stock['high'], stock['low'], stock['close'], stock['volume'], timeperiod=14)

        # Get rid of NaNs
        stock = stock.dropna(axis=0, how='any')

        # save CSV
        stock.to_csv(f'data/{symbol}.csv')
    except:
        print(f'\nThere was an error downloading {symbol}. Continuing to the next iteration.')
        continue
