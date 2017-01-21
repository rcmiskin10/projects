import numpy as np
import pandas as pd
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import sys

style.use('ggplot')

class Strategy(object):
	def __init__(self,stock):
		self.stock = stock
	def simple_moving_average(self, smashort, smalong):

		start = datetime.datetime(2001, 1, 1)
		
		end = datetime.datetime.now()
		
		df = web.DataReader(self.stock, "yahoo", start, end)

		#how to create array in np
		#array = np.array([1,2,2,3,1,2,3,2])

		#df = pd.DataFrame(array, columns=['price'])

		sma1 = pd.rolling_mean(df['Close'], smashort, min_periods=smashort)
		sma2 = pd.rolling_mean(df['Close'], smalong, min_periods=smalong)
		df['SMA1'] = sma1
		df['SMA2'] = sma2
		
		df['Decision'] = 'Sell'
		df.loc[df['SMA1'] > df['SMA2'],'Decision'] ='Buy'

		df['Date'] = df.index

		df = df[['Date', 'Close', 'SMA1', 'SMA2', 'Decision']]
		df = df.dropna()
		
		# shift decision column values up 1 so that we get a new column for previous decisions
		df['Previous Decision']= df['Decision'].shift(1)

		# column for decision change or crossover of moving averages.
		# if previous decision does not equal to current day decision then use current day decision as signal to buy or sell.

		df['Signal'] = 'None'
		df.loc[df['Decision'] != df['Previous Decision'],'Signal'] = df['Decision']

		buys = df[df.Signal == 'Buy']
		sells = df[df.Signal == 'Sell']
		frames = [buys, sells]

		transactions = pd.concat(frames)
		bs = transactions.sort_values(by='Date')[['Date','Close', 'Decision']]
		
		# turn buy sell df to numpy array
		bs = bs.values
		#remake_to_df = pd.DataFrame(bs, columns=['Date','Close','Decision'])
		if bs[0][2] == 'Sell':
			bs = bs[1:]
		if bs[0][2] == 'Buy':
			bs = bs
		# loop through np.array of bs, and if buy append to end of the list in array the 10k*the price, and same with sell
		# creates an np.array of all buys and sell signals
		orders = np.array([np.append(item,[item[1]*100]) if item[2] == 'Buy' else np.append(item,[item[1]*-100]) for item in bs ])
		
	
		initial = 100000
		for item in orders:
			initial = initial + item[3]
		init = 100000
		final_portfolio_value = initial
		gain = final_portfolio_value - init

		# convert to dataframe by using np.array of orders
		mo = pd.DataFrame(orders, columns=['Date','Close','Decision', 'Order'])

		print "Initial portfolio value: $100000"
		print mo
		print "Final portfolio value: $" + str(final_portfolio_value)
		print "Net Gain: $" + str(gain)

		##graph sma crossovers
		df['Close'].plot()
		df['SMA1'].plot()
		df['SMA2'].plot()
		# plot sma1's price, since we are looking at when sma1 is less than or greater than sma1
		plt.plot(buys.SMA1, 'g^', ms=10)
		plt.plot(sells.SMA1, 'rx', ms=10)

		plt.legend()
		plt.show()
		main()
	def exponential_moving_average(self, smashort, smalong):

		start = datetime.datetime(2001, 1, 1)
		
		end = datetime.datetime.now()
		
		df = web.DataReader(self.stock, "yahoo", start, end)

		#how to create array in np
		#array = np.array([1,2,2,3,1,2,3,2])

		#df = pd.DataFrame(array, columns=['price'])

		sma1 = df['Close'].rolling(smashort, smashort).mean()
		sma2 = df['Close'].rolling(smalong, smalong).mean()
		df['SMA1'] = sma1
		df['SMA2'] = sma2
		df['Date'] = df.index
		df = df[['Date','Close', 'SMA1', 'SMA2']]
		df = df.dropna()
		
		#weight = 2/days + 1
		#ema calculation: ((closing price - EMA(previous day))*mulitplier)+EMA(previous day)
		#EMA1
		
		df['EMA1'] = df['SMA1'].ewm(span=smashort, adjust=False).mean()
		df['EMA2'] = df['SMA2'].ewm(span=smalong, adjust=False).mean()

		df['Decision'] = 'Sell'
		df.loc[df['EMA1'] > df['EMA2'],'Decision'] ='Buy'

		df['Date'] = df.index

		df = df[['Date', 'Close', 'EMA1', 'EMA2', 'Decision']]
		
		
		# shift decision column values up 1 so that we get a new column for previous decisions
		df['Previous Decision']= df['Decision'].shift(1)

		# column for decision change or crossover of moving averages.
		# if previous decision does not equal to current day decision then use current day decision as signal to buy or sell.

		df['Signal'] = 'None'
		df.loc[df['Decision'] != df['Previous Decision'],'Signal'] = df['Decision']

		buys = df[df.Signal == 'Buy']
		sells = df[df.Signal == 'Sell']
		frames = [buys, sells]

		transactions = pd.concat(frames)
		bs = transactions.sort_values(by='Date')[['Date','Close', 'Decision']]
		
		# turn buy sell df to numpy array
		bs = bs.values
		#remake_to_df = pd.DataFrame(bs, columns=['Date','Close','Decision'])
		if bs[0][2] == 'Sell':
			bs = bs[1:]
		if bs[0][2] == 'Buy':
			bs = bs
		# loop through np.array of bs, and if buy append to end of the list in array the 10k*the price, and same with sell
		# creates an np.array of all buys and sell signals
		orders = np.array([np.append(item,[item[1]*100]) if item[2] == 'Buy' else np.append(item,[item[1]*-100]) for item in bs ])
		
	
		initial = 100000
		for item in orders:
			initial = initial + item[3]
		init = 100000
		final_portfolio_value = initial
		gain = final_portfolio_value - init

		# convert to dataframe by using np.array of orders
		mo = pd.DataFrame(orders, columns=['Date','Close','Decision', 'Order'])

		print "Initial portfolio value: $100000"
		print mo
		print "Final portfolio value: $" + str(final_portfolio_value)
		print "Net Gain: $" + str(gain)

		##graph sma crossovers
		df['Close'].plot()
		df['EMA1'].plot()
		df['EMA2'].plot()
		# plot sma1's price, since we are looking at when sma1 is less than or greater than sma1
		plt.plot(buys.EMA1, 'g^', ms=10)
		plt.plot(sells.EMA1, 'rx', ms=10)

		plt.legend()
		plt.show()
		main()
def main():
	prompt = SMAPrompt()
	
	try:
		indicator = raw_input("What technical indicator do you want to backtest?\n\t1. Simple Moving Average Crossover\n\t2. Exponential Moving Average Crossover\n\t3. Exit\n>>> ")
	except:
		main()
	if indicator == '1' or indicator == 'sma' or indicator =='simple moving average':
		prompt = SMAPrompt()
		strat = Strategy(prompt.stock_symbol())
		short = prompt.shortsma()
		lon = prompt.longsma(short)
		strat.simple_moving_average(short, lon)
	if indicator == '2' or indicator == 'ema' or indicator =='exponential moving average':
		prompt = SMAPrompt()
		strat = Strategy(prompt.stock_symbol())
		short = prompt.shortsma()
		lon = prompt.longsma(short)
		strat.exponential_moving_average(short, lon)
	if indicator == '3' or indicator == 'exit' or indicator == 'Exit':
		sys.exit()
	else:
		main()

class SMAPrompt(object):

	def shortsma(self,*args, **kwargs):
		try:
			smashort = int(raw_input("How many days do you want the shorter moving average to be?\n>>> "))
			return smashort
		except:
			return self.shortsma(*args, **kwargs)
	
	def longsma(self, short, *args, **kwargs):
		try:			
			smalong = int(raw_input("How many days do you want the longer moving average to be?\n>>> "))
			if short < smalong:
				return smalong
			else:
				return self.longsma(short, *args, **kwargs)
		except:
			return self.longsma(*args, **kwargs)

	def stock_symbol(self, *args, **kwargs):
		try:
			stock = raw_input("What stock symbol do you want to back test?\n>>> ")
			web.DataReader(stock, "yahoo")
			return stock
		except:
			return self.stock_symbol(*args, **kwargs)

main()


