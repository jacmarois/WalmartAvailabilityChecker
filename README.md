# WalmartAvailabilityChecker
A friend was sick of going to the walmart.com page to see if the PS5 was in stock, so I made this to run instead.

## How to use
This script is command line only, and made to run specifically on **Windows**. When you run the script, it will show a menu.

### Option 1
Option 1 will check for a file in the same directory as the script called prod_list.json. If this file doesn't already exist, it will be created, if it does, it will be read to get a list of URLs for walmart.com product pages and will check the availability of those products.

### Option 2
Option 2 allows you to add a URL to the prod_list.json file. There are some rudimentary checks to make sure the URL provided is for a walmart.com product page (don't forget the 'https://'!). Once the URL is added, the script will check the availability of all URLs in prod_list.json.

### Option 3
Option 3 allows you to remove URLs from the prod_list.json file.

### Option 4
Option 4 is a help function incase you forget any of this.

### Option 5
Option 5 stops the main loop.

## Issues
I'm sure there are plenty, but the most common one I've experienced is a TypeError that I believe to be a request limiter on Walmart's end. If you wait about 30 seconds to a minute and run the script again it works fine...

###### Yes, I know I misspelled useful in the commit...
