import requests
from bs4 import BeautifulSoup
from datetime import datetime

#User inputs URL for product to check availability
url = input("Enter the product's URL:\n")

#Make sure the user kept the 'https' and that the URL is for walmart.com
checker = ['walmart', 'https']
for check in checker:
	if check not in url:
		print("Sorry, but the URL must include the 'https' and be from walmart.com")
		quit()

#Get the source HTML from the URL
#note: the user agent IS REQUIRED for this to work due to the way walmart.com works
page = requests.get(url, headers={"User-Agent":"Defined"})

#make sure the page was gotten without issue
if page.status_code == 200:
	#parse the page
	soup = BeautifulSoup(page.content, 'html.parser')
	#the link tag with the availability itemprop will contain an href that links to either
	#an in stock or out of stock schema.org page
	item_avail = soup.find('link', {'itemprop':'availability','href':True})['href']

	#Get time for timestamp
	time = '[' + datetime.now().strftime('%H:%M:%S') + ']: '

	#Check if the link is for the OutOfStock page or not
	if 'OutOfStock' in item_avail:
		#Added color codes for flair
		print(time + 'Item is \033[91mOUT OF STOCK\033[0m')
	else:
		print(time + 'Item is \033[92mIN STOCK\033[0m')