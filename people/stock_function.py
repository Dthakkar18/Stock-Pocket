from bs4 import BeautifulSoup
import requests
import yfinance as yf


def generalInfo(ticker):
	# using modular approach
	stock = yf.Ticker(ticker)
	info = stock.info
	names = ["Previous Close:", "Open:", "Days's Range:", "Volume:", "PE Ratio:", "Dividend Percentage:", "Dividend Amount", "Buy/Sell:"]
	values = []
	# getting all needed values
	previous_close = decimal_alignment(str(info["previousClose"]))
	open = decimal_alignment(str(info["open"]))
	day_low = decimal_alignment(str(info["dayLow"]))
	day_high = decimal_alignment(str(info["dayHigh"]))
	volume = str(info["volume"])
	trailing_pe = str(round(info["trailingPE"], 2))
	dividend_percetnage = str(round(float(info["dividendYield"] * 100), 2))
	dividend_amount = decimal_alignment(str(info["dividendRate"]))
	buy_or_sell = str(info["recommendationKey"])
	# adding to values list with corresponds respectivly to the names list
	values.append("$"+ previous_close)
	values.append("$" + open)
	values.append("$" + day_low + " - $" + day_high)
	values.append(volume)
	values.append(trailing_pe)
	values.append(dividend_percetnage + "%")
	values.append("$" + dividend_amount)
	values.append(buy_or_sell)
	
	namesAndValues = {"names": names, "values": values}
	return namesAndValues

# helper used in multiple menthods for proper price format
def decimal_alignment(amount: str) -> str:
	if amount.__contains__("."):
		amount = amount + "00"
		amount = f'{float(amount):.2f}'
	else:
		amount = amount + ".00"
	return amount 


def showRevenue(Name, Ticker):
	html_text = requests.get(f'https://www.macrotrends.net/stocks/charts/{Ticker.upper()}/{Name.lower()}/revenue').text
	soup = BeautifulSoup(html_text, 'lxml')
	table = soup.find('tbody')
	each = table.find_all('tr')
	revenues = []
	years = []
	for i in each:
		line = i.text.replace("\n", "")
		line = line.replace(",", "")
		years.append(line[:4])
		revenues.append(line[5:])

	yearsAndRevenues = {"years": years[::-1], "revenues": revenues[::-1]}
	return yearsAndRevenues

def showGrossProfit(Name, Ticker):
	html_text = requests.get(f'https://www.macrotrends.net/stocks/charts/{Ticker.upper()}/{Name.lower()}/gross-profit').text
	soup = BeautifulSoup(html_text, 'lxml')
	table = soup.find('tbody')
	each = table.find_all('tr')
	profits = []
	years = []
	for i in each:
		line = i.text.replace("\n", "")
		line = line.replace(",", "")
		years.append(line[:4])
		profits.append(line[5:])

	yearsAndProfits = {"years": years[::-1], "profits": profits[::-1]}
	return yearsAndProfits

def summary(Ticker): # sector, industry, employee, summary
	items_list = []
	stock = yf.Ticker(Ticker)
	info = stock.info
	items_list.append(info.get("sector"))
	items_list.append(info.get("industry"))
	items_list.append(str(info.get("fullTimeEmployees")))
	items_list.append(info.get("longBusinessSummary"))
	
	return items_list

def similar_tickers(Ticker):
	html_text = requests.get(f'https://finance.yahoo.com/quote/{Ticker.upper()}?p={Ticker.upper()}').text
	soup = BeautifulSoup(html_text, 'lxml')
	table = soup.find('table', class_='W(100%) Pos(r) Tbl(f) Bdcl(c) BdB Bdc($seperatorColor)')
	tbody = table.find('tbody')
	symbols = []
	for item in tbody:
		a = item.find('a', class_='Fw(b) Ell D(b) C($linkColor) Pos(r) Z(2)')
		symbols.append(a.text)
	return symbols

def similar_names(Ticker):
	html_text = requests.get(f'https://finance.yahoo.com/quote/{Ticker.upper()}?p={Ticker.upper()}').text
	soup = BeautifulSoup(html_text, 'lxml')
	table = soup.find('table', class_='W(100%) Pos(r) Tbl(f) Bdcl(c) BdB Bdc($seperatorColor)')
	tbody = table.find('tbody')
	symbols = []
	for item in tbody:
		p = item.find('p', class_='Fz(xs) Pt(2px) M(0) C($tertiaryColor) Pos(a) Fw(400)! Ell Maw(220px)')
		symbols.append(p.text)
	return symbols

def similar_prices(Ticker):
	html_text = requests.get(f'https://finance.yahoo.com/quote/{Ticker.upper()}?p={Ticker.upper()}').text
	soup = BeautifulSoup(html_text, 'lxml')
	table = soup.find('table', class_='W(100%) Pos(r) Tbl(f) Bdcl(c) BdB Bdc($seperatorColor)')
	tbody = table.find('tbody')
	symbols = []
	for item in tbody:
		fin = item.find('fin-streamer', class_='Fw(500)')
		symbols.append(fin.text)
	return symbols

# not using this function right now
def purchase(Ticker):
	html_text = requests.get(f'https://finance.yahoo.com/quote/{Ticker.upper()}?p={Ticker.upper()}').text
	soup = BeautifulSoup(html_text, 'lxml')
	div = soup.find('div', class_='Bdbw(2px) Bdbs(s) Bdbc($seperatorColor) H(1em) Pos(r) Mt(30px) Mx(10%)')
	print(div.text)
	if float(div.text) == 1 or float(div.text) <= 1.5:
		return [div.text, 'Strong Buy']
	elif float(div.text) > 1.5 or float(div.text) <= 2.5:
		return [div.text, "Buy"]
	elif float(div.text) > 2.5 or float(div.text) <= 3.5:
		return [div.text, "Hold"]
	elif float(div.text) > 3.5 or float(div.text) <= 4.5:
		return [div.text, "Underperforming"]
	else:
		return [div.text, "Sell"]

def current_change(Tickers, shares, amounts):
	formated_price_changes = []
	for i in range(len(Tickers)):
		stock = yf.Ticker(Tickers[i])
		info = stock.info
		current_price = info.get("regularMarketPrice")
		changed_price = str(current_price*shares[i] - amounts[i])
		changed_price = decimal_alignment(changed_price)
		if float(changed_price) < 0:
			formated_price_changes.append("- $" + changed_price[1:])
		else:
			formated_price_changes.append("+ $" + changed_price)

	return formated_price_changes

# helper method for current_change
def point(number):
		text = str(number)
		return text.index('.')

def dividendPercentage(Tickers, Companies, Amounts):
	correctFormatValues = [] # all dividends for this year
	for i in range(len(Tickers)):
		stock = yf.Ticker(Tickers[i])
		dividendRate = stock.info.get("dividendRate")
		if type(dividendRate) == None.__class__: # for stocks that don't have dividend rate
			dividendRate = 0.0
		amount = float(dividendRate) * Amounts[i] / 100 
		amount = round(amount, 2)
		index = point(amount) + 1 # to not include the "." in the substring length
		if len(str(amount)[index:]) != 2: # for the numbers that are not to the 0.00 format
			correctFormatValues.append("$" + str(amount) + "0")
		else: # for numbers that are already the right format
			correctFormatValues.append("$" + str(amount))
	return correctFormatValues

# returns dictionary of years and dividend amounts
def dividendGrowth(Ticker):
	stock = yf.Ticker(Ticker.upper())

	series = stock.dividends # returns pandas series
	quarterAmounts = series.values # returns list
	fullDates = series.keys() # returns list of full dates

	quarterYears = []
	annualYears = []
	for date in fullDates:
		theYear = str(date)[:4] # only gets the year from the time stamp
		quarterYears.append(theYear)
		if theYear not in annualYears:
			annualYears.append(theYear)

	annualAmounts = []
	bridge = 0 # index of last kind of that year
	for i in range(len(annualYears)):
		currYear = annualYears[i]

		# finding number of payouts for that year
		counter = 0
		for quarter in quarterYears: #only checks from cut off to 5 more
			if currYear == quarter:
				counter += 1

		amount = 0
		for num in quarterAmounts[bridge : bridge + counter]: # only goes over right section of list
			amount += float(num)

		annualAmounts.append(round(amount, 2))
		bridge += counter

	yearAndAmount = {"years": annualYears, "amounts": annualAmounts}
	return yearAndAmount

def stockPrice(Ticker, period):
	stock = yf.Ticker(Ticker.upper())
	hist = stock.history(period=str(period)) # {num}mo
	closePrices = hist['Close'] # dont know how to get date from df

def institutionalHolders(ticker):
	stock = yf.Ticker(ticker.upper())
	df = stock.institutional_holders # has holders, shares, value
	return df # access by df['Holder'], df['Shares'], df['Value']

def news(ticker):
	stock = yf.Ticker(ticker.upper())
	titles = []
	links = []
	for item in stock.news:
		titles.append(item.get('title'))
		links.append(item.get('link'))
	titleAndlink = {'titles': titles, 'links': links}
	return titleAndlink # list of dictionaries 

if __name__ == '__main__':
	print('hello, running function file')