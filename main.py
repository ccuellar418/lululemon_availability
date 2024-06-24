import requests
import json
from bs4 import BeautifulSoup
import time
import pyautogui
import pywinauto
import os
import sys
import msvcrt
import keyboard
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
# from webdriver_manager.chrome import ChromeDriverManager

def driver_setup(url, email, first_name, last_name, phone_number, address, city, state, zip_code):
    driver = webdriver.Firefox()
    driver.get(url) 
    driver.maximize_window()
    time.sleep(5)
    keyboard.press_and_release('esc')
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 450)")
    # time.sleep(1)
    #move the mouse 1/3 up from the bottom of the screen and 3/4 to the right of the screen
    pyautogui.moveTo(1920*3/4, 1080*2/3)
    #click the mouse
    pyautogui.click()
    time.sleep(3)
    driver.get('https://shop.lululemon.com/shop/checkout')
    time.sleep(3)
    auto_fill_shipping(driver, email, first_name, last_name, phone_number, address, city, state, zip_code)
    continue_button = driver.find_element(By.ID, 'continue-to-payment-button')
    continue_button.click()
    time.sleep(30)


def auto_fill_shipping(driver, email, first_name, last_name, phone_number, address, city, state, zip_code):
    email_tag = driver.find_element(By.ID, 'contact-email')
    first_name_tag = driver.find_element(By.ID, 'shipping-first-name')
    last_name_tag = driver.find_element(By.ID, 'shipping-last-name')
    phone_number_tag = driver.find_element(By.ID, 'shipping-contact-phoneNumber')
    address_tag = driver.find_element(By.ID, 'shipping-street-address')
    city_tag = driver.find_element(By.ID, 'shipping-city')
    state_dropdown = driver.find_element(By.ID, 'shipping-state')
    zip_code_tag = driver.find_element(By.ID, 'shipping-zip-code')

    email_tag.send_keys(email)
    first_name_tag.send_keys(first_name)
    last_name_tag.send_keys(last_name)
    phone_number_tag.send_keys(phone_number)
    address_tag.send_keys(address)
    city_tag.send_keys(city)
    select_state = Select(state_dropdown)
    select_state.select_by_visible_text(state)
    zip_code_tag.send_keys(zip_code)





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

    if url == "s":
        url = 'https://shop.lululemon.com/p/women-sports-bras/Energy-Bra-Long-Line/_/prod9030660?color=65551&sz=4'
        auto_buy = True
        email = 'crlc418@gmail.com'
        first_name = 'Christian'
        last_name = 'Cuellar'
        phone_number = '1234567890'
        address = '1234 Main St'
        city = 'Los Angeles'
        state = 'California'
        zip_code = '90001'
    else:
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
        email = input("Please enter your email: ")
        first_name = input("Please enter your first name: ")
        last_name = input("Please enter your last name: ")
        phone_number = input("Please enter your phone number: ")
        address = input("Please enter your address: ")
        city = input("Please enter your city: ")
        state = input("Please enter your state: ")
        #make it so that no matter what the user inputs, it will have a capital for the first letter and lowercase for the rest in 'state' variable input
        state = state.capitalize()
        zip_code = input("Please enter your zip code: ")
    return url, auto_buy, email, first_name, last_name, phone_number, address, city, state, zip_code



def getStock(soup):
    meta_tag = soup.find('meta', {'property': 'og:product:availability'})
    availability = meta_tag['content']
    if availability == "in stock":
        return True
    elif availability == "out of stock":
        return False
    else:
        print(Exception("Unknown availability status: " + availability))


def retry(url, auto_buy, email, first_name, last_name, phone_number, address, city, state, zip_code):
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
                driver_setup(url, email, first_name, last_name, phone_number, address, city, state, zip_code)
                print("Auto buy action performed")
            break
        else:
            print("Product is out of stock. Checking again in 5 seconds...")
            time.sleep(5)
            retry(url, auto_buy, email, first_name, last_name, phone_number, address, city, state, zip_code)




def main():
    url, auto_buy, email, first_name, last_name, phone_number, address, city, state, zip_code = promptOps()
    url = 'https://shop.lululemon.com/p/women-sports-bras/Energy-Bra-Long-Line/_/prod9030660?color=65551&sz=4'
    retry(url, auto_buy, email, first_name, last_name, phone_number, address, city, state, zip_code)


if __name__ == "__main__":
    main()
