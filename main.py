import requests
import json
from bs4 import BeautifulSoup
import time
import pyautogui
import pywinauto
import os
import sys
import msvcrt

def auto_submit():
    print("Would you like to enable auto buy? (y/n): ", end='', flush=True)
    user_input = msvcrt.getch().decode('utf-8')
    # print(f"\nYou submitted: {user_input}")
    return user_input


def get_specific_line(soup, line_number):#i dont think i will need this line of code
    # Get the raw HTML as a string
    raw_html = str(soup)#.prettify())
    lines = raw_html.split('\n')
    if line_number <= 0 or line_number > len(lines):
        return f"Error: line_number {line_number} is out of range. The HTML has {len(lines)} lines."
    return lines[line_number - 1]


def promptOps():
    print("Welcome to the Product Bot")
    print("Please input the product url you would like to watch over")
    url = input("Product URL:")
    print("Auto buy will automatically buy the product for you when it is in stock")
    #print("Would you like to enable auto buy? (y/n)")
    auto_buy = auto_submit()
    while auto_buy != "y" and auto_buy != "n":
        print("\nPlease only type 'y' or 'n'\n")
        auto_buy = auto_submit()
        
    if auto_buy == "y":
        print("Auto buy enabled\n")
        auto_buy = True
    else:
        print("Auto buy disabled\n")
        auto_buy = False
    return url, auto_buy


def getStock(soup):
    meta_tag = soup.find('meta', {'property': 'og:product:availability'})
    availability = meta_tag['content']
    if availability == "in stock":
        return True
    elif availability == "out of stock":
        return False
    else:
        print(Exception("Unknown availability status: " + availability))


def retry(url, auto_buy):
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    while True:
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()  # raises an exception if the request was not successful
        except requests.exceptions.RequestException as e:
            print(e)
            print('An error occurred while making the request')
        else:
            # request was successful
            soup = BeautifulSoup(r.content, 'lxml')


        stock = getStock(soup)
        if stock:
            print("Product is in stock!")
            if auto_buy:
                # Add code here to perform auto buy action
                print("Auto buy action performed")
            break
        else:
            print("Product is out of stock. Checking again in 5 seconds...")
            time.sleep(5)
            retry(url, auto_buy)




def main():
    url, auto_buy = promptOps()
    url = 'https://shop.lululemon.com/p/women-sports-bras/Energy-Bra-Long-Line/_/prod9030660?color=65551&sz=4'
    retry(url, auto_buy)


if __name__ == "__main__":
    main()
