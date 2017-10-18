from slacker import Slacker
import pandas as pd
import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError
from datetime import datetime, timedelta
import pause


slackBot = Slacker('api key here')


def postMessage(message, slackBot=slackBot):
    slackBot.chat.post_message('@username', message, username='StockBot', as_user=False,
                            icon_url='http://i2.kym-cdn.com/entries/icons/facebook/000/000/107/awesome-face.jpg')


df = pd.read_csv('sp500.csv')

while 1:
	if datetime.now().weekday() in [5,6]:
		time.sleep(86400)
		continue
	pause.until(datetime(datetime.now().year,datetime.now().month,datetime.now().day) + timedelta(days=17./24))
	print 'test'
	dateList = web.DataReader('SPY', 'google', datetime.now() - timedelta(days=7), datetime.now()).index
	di = {'ticker': [], 'change':[]}
	for ticker in df.Ticker:
		ticker = ticker.replace('.', '-')
		try:
			tmp = web.DataReader(ticker, 'google', dateList[-2], dateList[-1])
			if len(tmp) < 2:
				continue
			di['change'].append(100 * (tmp['Close'].iloc[-1] / tmp['Close'].iloc[-2] - 1))
			di['ticker'].append(ticker)
		except RemoteDataError:
			print 'Error retrieving data for',ticker

	losers = pd.DataFrame(di).sort_values('change').head(10)
	message = """
	Bottom performing stocks today:\n
	%s: %s%% \n
	%s: %s%% \n
	%s: %s%% \n
	%s: %s%% \n
	%s: %s%% \n
	%s: %s%% \n
	%s: %s%% \n
	%s: %s%% \n
	%s: %s%% \n
	%s: %s%%
	""" % (
		losers.ticker.iloc[0], round(losers.change.iloc[0],3),
		losers.ticker.iloc[1], round(losers.change.iloc[1],3),
		losers.ticker.iloc[2], round(losers.change.iloc[2],3),
		losers.ticker.iloc[3], round(losers.change.iloc[3],3),
		losers.ticker.iloc[4], round(losers.change.iloc[4],3),
		losers.ticker.iloc[5], round(losers.change.iloc[5],3),
		losers.ticker.iloc[6], round(losers.change.iloc[6],3),
		losers.ticker.iloc[7], round(losers.change.iloc[7],3),
		losers.ticker.iloc[8], round(losers.change.iloc[8],3),
		losers.ticker.iloc[9], round(losers.change.iloc[9],3) 
		)

	postMessage(message)