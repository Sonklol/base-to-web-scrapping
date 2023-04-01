from art import tprint

tprint('BASE  TO  WEB  SCRAPING')
menu = int(input('Web Scrapping (https://github.com/Sonklol)\n1. BASE1\n2. BASE2\n> '))

if menu == 1:
    from base import scrap
elif menu == 2:
    from base2 import scrap
scrap()
