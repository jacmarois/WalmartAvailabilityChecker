import requests
import sys
import os
import json
from bs4 import BeautifulSoup
from datetime import datetime

#This function prints the main menu message
def print_main_menu():
	os.system('cls')
	print('''
--------------- Menu ---------------
[1] Check from current list
[2] Add Walmart.com product URL
[3] Remove URL from list
[4] Help
[5] Exit
------------------------------------
Enter your choice [1-5]: 
	''')

#This function prints the help message
def print_help():
	os.system('cls')
	print('''
--------------- Help ---------------
This script takes a URL for a walmart.com product page and checks to see if the products are in stock.\n
Option 1 uses the current list of URLs (stored in prod_list.json) and checks their availability
Option 2 lets you add a url to the list stored 
Option 3 lets you remove a previously checked URL from the list to check again
Option 4 is what brought you here
Option 5 closes the script
------------------------------------
[99] Back
[5] Exit
------------------------------------
Enter your choice: 
	''')

#This function stops the script's execution with a message
def stop():
	print('\nStopping script...\n')
	sys.exit()

#This function gets the webpage data for the product and checks the availability
def get_item_avail(url):
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

		#Get name of product
		prod_name_temp = soup.find('h1', {'class':'prod-ProductTitle prod-productTitle-buyBox font-bold'}).get_text()

		#Sanitize prod_name
		rem_chars = "\':\"’’"
		prod_name = ''.join(c for c in prod_name_temp if c not in rem_chars)

		#Get time for timestamp
		time = '[' + datetime.now().strftime('%H:%M:%S') + ']: '

		#Check if the link is for the OutOfStock page or not
		if 'OutOfStock' in item_avail:
			#Added color codes for flair
			print(time + prod_name + ' is \033[91mOUT OF STOCK\033[0m')
		else:
			print(time + prod_name + ' is \033[92mIN STOCK\033[0m')

#This function checks the availability of all items in the input list
def check_items(prod_list):
	for url in prod_list:
		get_item_avail(url)

#This function does a halfway decent job of making sure the URL is valid
def validate_url(url):
	if 'https://' in url and 'walmart.com/ip/' in url:
		return True
	else:
		return False

#This function returns the list of URLs in prod_list.json as a list
def get_prod_list():
	prod_list = []

	if not os.path.isfile('./prod_list.json'):
		with open('prod_list.json','w') as outfile:
			outfile.write('[]')

	try:
		with open('prod_list.json') as prod_list_file:
			prod_list = json.load(prod_list_file)
	except:
		print('There was an issue reading prod_list.json')
		stop()

	return prod_list

#This function overwrites the prod_list.json with a new list
def set_prod_list(prod_list):
	try:
		with open('prod_list.json','w') as prod_list_file:
			json.dump(prod_list, prod_list_file, indent=2)
	except:
		print('There was an issue overwriting prod_list.json')
		stop()

#This function adds a product URL to the prod_list.json
def add_prod(url):
	#Make sure the URL looks right first
	if validate_url(url):
		#Then add it to the current list of URLs
		prod_list = get_prod_list()
		prod_list.append(url)
		set_prod_list(prod_list)
	else:
		print('That URL did not look like a walmart.com product page')

loop = True
while loop:
	print_main_menu()
	choice = int(input())

	#Check list
	if choice is 1:
		print('Checking...')
		prod_list = get_prod_list()
		os.system('cls')
		check_items(prod_list)
		input('Press any key to continue...')
	
	#Add URL to list
	elif choice is 2:
		wmpath = input('Enter the walmart.com product page URL: ')
		add_prod(wmpath)

		#Check availability immediately after adding the new URL to check
		print('Checking Availability...')
		prod_list = get_prod_list()
		check_items(prod_list)
		input('Press any key to continue...')
	
	#Remove URL from list
	elif choice is 3:
		#Print out the current list of products so the user can see
		os.system('cls')
		prod_list = get_prod_list()
		for i in range(len(prod_list)):
			print('[' + str(i+1) + '] ' + prod_list[i])
		print('Enter product to remove [1-' + str(len(prod_list)) + ']: ')
		#Added 1 to the message for appearance, but now have to subtract one to get the actual list index
		rem_prod = int(input())-1
		#Remove the element at the chosen index
		prod_list.pop(rem_prod)
		#Update prod_list.json
		set_prod_list(prod_list)
	
	#Help
	elif choice is 4:
		print_help()
		choice = int(input())
		if choice is 5:
			loop = False
	
	#Exit
	elif choice is 5:
		loop = False