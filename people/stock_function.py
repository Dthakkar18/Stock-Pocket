from bs4 import BeautifulSoup
import requests
import yfinance as yf


def generalInfo(ticker):
	html_text = requests.get(f'https://finance.yahoo.com/quote/{ticker.upper()}/').text
	soup = BeautifulSoup(html_text, 'lxml')
	the_tr = soup.find_all('tr')
	the_items = []
	the_date = []
	finished = []
	the_items.append(the_tr[0].text) #previous close
	the_items.append(the_tr[1].text) #open
	the_items.append(the_tr[4].text) #day range
	the_items.append(the_tr[6].text) #volume
	the_items.append(the_tr[8].text) #market cap
	the_items.append(the_tr[10].text) #pe ratio
	the_items.append(the_tr[13].text) #dividend val
	the_date.append(the_tr[12].text) #earnings
	the_date.append(the_tr[14].text) #ex dividend date
	for item in the_items:
		new_item = seperator(item)
		finished.append(new_item)
	for date in the_date:
		new_date = seperator(date)
		colon = new_date.index(":")
		start_index = colon - 4
		the_date = new_date[:start_index] + ': ' + new_date[start_index:colon] + new_date[colon+2:]
		finished.append(the_date)
	return finished

#helper for generalInfo
def seperator(word):
		counter = 0  #gets index for where the number is in text --> (open120)
		for char in word:
			if char.isdigit() == False:
				counter += 1 #counting letters before number 
				pass
			else:
				break
		if counter != len(word):
			return (word[0:(counter)] + ': ' + word[counter:]) #seperates --> (open: 120)
		else:
			badChars = ['N', 'A', '(', ')', '/']
			for i in badChars:
				word = word.replace(i, '')
			return (word + ": N/A")	


def showRevenue(Name, Ticker):
	html_text = requests.get(f'https://www.macrotrends.net/stocks/charts/{Ticker.upper()}/{Name.lower()}/revenue').text
	soup = BeautifulSoup(html_text, 'lxml')
	table = soup.find('tbody')
	each = table.find_all('tr')
	revenues = []
	for i in each:
		revenues.append(i.text.replace("\n", " "))
	return revenues

def showGrossProfit(Name, Ticker):
	html_text = requests.get(f'https://www.macrotrends.net/stocks/charts/{Ticker.upper()}/{Name.lower()}/gross-profit').text
	soup = BeautifulSoup(html_text, 'lxml')
	table = soup.find('tbody')
	each = table.find_all('tr')
	profits = []
	for i in each:
		profits.append(i.text.replace("\n", " "))
	return profits

def summary(Ticker):
	html_text = requests.get(f'https://finance.yahoo.com/quote/{Ticker.upper()}?p={Ticker.upper()}').text
	soup = BeautifulSoup(html_text, 'lxml')
	items_list = []
	summary = soup.find('p', class_='businessSummary Mt(10px) Ov(h) Tov(e)')
	div_section = soup.find('div', class_="Mb(25px)")
	span_sectors = div_section.find_all('span', class_="Fw(600)")
	for item in span_sectors:
		items_list.append(item.text)
	items_list.append(summary.text)
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
	currentP = []
	up_down = []
	for ticker in Tickers:
		html_text = requests.get(f'https://finance.yahoo.com/quote/{ticker.upper()}?p={ticker.upper()}').text
		soup = BeautifulSoup(html_text, 'lxml')
		price = soup.find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)')
		currentP.append(float(price.text))
	#adds string version of num to up_down
	for i in range(len(currentP)):
		num = round((currentP[i])*shares[i] - amounts[i], 2)
		index = point(num) + 1 # to not include the "." in the substring length
		if len(str(num)[index:]) != 2: # for the numbers that are not to the 0.00 format
			if num > 0: #if it should have "+"
				up_down.append("+ $" + str(num) + "0") 
			else: #if it should have "-"
				up_down.append("- $" + str(num)[1:] + "0") # gets rid of the neg in the front of the number
		else: # for numbers that are in the right format
			if num > 0:
				up_down.append("+ $" + str(num))
			else:
				up_down.append("- $" + str(num)[1:]) # gets rid of the neg in the front of the number
			
	return up_down

# helper method for current_change
def point(number):
		text = str(number)
		return text.index('.')	

def dividendPercentage(Tickers, Companies, Amounts):
	correctFormatValues = [] # all dividends for this year
	for i in range(len(Tickers)):
		html_text = requests.get(f'https://www.macrotrends.net/stocks/charts/{Tickers[i].upper()}/{Companies[i].lower()}/dividend-yield-history').text
		soup = BeautifulSoup(html_text, 'lxml')
		div = soup.select_one('div[style="background-color:#fff; margin: 0px 0px 20px 0px; padding:20px 30px; border:1px solid #dfdfdf;"]')
		percentage = div.text[-7:-3]
		amount = float(percentage) * Amounts[i] / 100 
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


if __name__ == '__main__':
	print('hello, running function file')