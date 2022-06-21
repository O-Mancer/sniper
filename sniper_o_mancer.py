import datetime
import os
import signal
import sys
import threading
import time

import pandas as pd
import selenium
from colorama import init, Fore
from pyfiglet import figlet_format
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from contextlib import suppress
import psutil
from termcolor import cprint

startTime = time.time()

init(autoreset=True, strip=not sys.stdout.isatty())  # strip colors if stdout is redirected


# Get the uptime
def getuptime():
    """
    Returns the number of seconds since the program started.
    """
    # do return startTime if you just want the process start time
    n = int(time.time() - startTime)
    return str(datetime.timedelta(seconds=n))


class SniperOMancer:
    def __init__(self):
        # SETTINGS
        self.wallet_address = ''
        self.private_key = ''
        self.max_scraper_wait = 4
        self.scraper_sleep_time = 20
        self.updater_sleep_time = 5
        self.maximum_alerts = 4

        self.fake_mode = True
        self.fake_mode_sleep = 5
        self.fake_balance = 10
        self.fake_buy = 1
        self.takeprofit_x = 2
        self.stoploss_x = 2

        # INIT
        pd.set_option("display.precision", 16)
        pd.options.mode.chained_assignment = None  # default='warn'
        self.ser = Service(
            "./chromedriver")  # included in zip, if it isn't, you can download it from here: https://chromedriver.storage.googleapis.com/index.html?path=98.0.4758.102/
        self.op = Options()
        self.op.add_argument("--headless")  # allows you to scrape page without opening the browser window
        self.op.add_argument("--allow-running-insecure-content")  # allows you to scrape jewarch
        self.op.add_argument("--ignore-certificate-errors")  # allows you to scrape jewarch
        self.op.add_argument("--window-size=1920,1080")

        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        self.op.add_argument(f'user-agent={user_agent}')

        self.op.add_experimental_option('excludeSwitches', ['enable-logging'])  # remove annoying message
        self.newest_ca_driver = webdriver.Chrome(options=self.op)
        self.price_updater_driver = webdriver.Chrome(options=self.op)
        self.honeypot_updater_driver = webdriver.Chrome(options=self.op)
        self.kill_list = []
        self.inoperation = None
        self.jewarch_url = 'http://70.34.213.32'
        self.honeypot_url = 'https://honeypot.is/?address='
        self.database = pd.DataFrame(columns=['Name', 'Contract', 'Price', 'Rugcheck alerts', 'Honeypot', 'LP Lock', 'Ownership renounced', 'Excluded'])
        self.fake_buy_database = pd.DataFrame(columns=['Name', 'Contract', 'Entry', 'Current'])
        self.fake_buy_current_list = []
        self.exclude_list = []

    def scrape_newest_ca(self):
        while True:
            self.inoperation = True
            print(Fore.YELLOW + '\nScraping newest jewarch CA...')
            self.newest_ca_driver.get(self.jewarch_url)
            latest_ca = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "/html/body/div/div[2]/div/div[2]/div[1]/div[3]/div/div/div/table/tbody/tr[1]/td[4]/div/a[2]")))
            latest_ca_link = latest_ca.get_attribute('href')
            latest_ca = latest_ca.get_attribute('href').replace('https://poocoin.app/tokens/', '')

            if len(self.database['Contract']) > 0 and latest_ca in self.database["Contract"].values:
                print(Fore.CYAN + 'Contract already in database, continuing...')
                print(Fore.YELLOW + f'\nSleeping for {self.scraper_sleep_time} seconds...')
                time.sleep(self.scraper_sleep_time)
            else:
                print(Fore.YELLOW + 'New CA detected, getting info...')

                # Rugcheck
                try:
                    latest_ca_button = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "/html/body/div/div[2]/div/div[2]/div[1]/div[3]/div/div/div/table/tbody/tr[1]/td[3]/div/a")))
                    latest_ca_button.click()
                    rugcheck = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "/html/body/div[2]/div[1]/div/div/div/div/div[2]/button[4]/div/div/span")))

                    alert_number = int(rugcheck.text)
                    if alert_number > self.maximum_alerts:
                        self.exclude_list.append(latest_ca)

                except selenium.common.exceptions.TimeoutException:
                    alert_number = 'N/A'

                # LP Lock
                try:
                    lplock_or_not = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "/html/body/div[2]/div[1]/div/div/div/div/div[2]/button[3]/span")))
                    if lplock_or_not.text == '0':
                        latest_ca_lplock = False
                    elif lplock_or_not.text == '?':
                        latest_ca_lplock = 'N/A'
                    else:
                        latest_ca_lplock = True

                except selenium.common.exceptions.TimeoutException:
                    latest_ca_lplock = 'N/A'

                # Ownership
                try:
                    ownership_renounce_check = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "/html/body/div[2]/div[1]/div/div/div/div/div[3]/div[2]/ul/li[8]/span")))
                    if ownership_renounce_check.text == ' Renounced ':
                        latest_ca_ownership = True
                    else:
                        latest_ca_ownership = False

                except selenium.common.exceptions.TimeoutException:
                    latest_ca_ownership = 'N/A'

                # Honeypot
                try:
                    honeypot_url_ca = f'{self.honeypot_url}{latest_ca}'
                    self.newest_ca_driver.get(honeypot_url_ca)
                    honeypot_result = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "/html/body/div[2]/div[1]/div/div")))
                    if honeypot_result.text == 'Does not seem like a honeypot.':
                        latest_ca_honeypot = False
                    else:
                        latest_ca_honeypot = True

                        if latest_ca not in self.exclude_list:
                            self.exclude_list.append(latest_ca)
                except selenium.common.exceptions.TimeoutException:
                    latest_ca_honeypot = 'N/A'

                self.newest_ca_driver.get(latest_ca_link)

                latest_ca_name = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                    EC.visibility_of_element_located((
                        By.XPATH,
                        "/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/h1"))).text
                latest_ca_name = latest_ca_name.split(' (', 1)[0]

                # Price
                try:
                    latest_ca_price = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/span")))

                    try:
                        latest_ca_price = float(latest_ca_price.text.replace('$', ''))
                        latest_ca_price_forprint = f'{latest_ca_price:.20f}'
                        fake_buy_token = True
                    except ValueError:
                        print(Fore.YELLOW + f'{latest_ca_name} has an unstable price, skipping price')
                        latest_ca_price = 'N/A'
                        fake_buy_token = False

                except selenium.common.exceptions.TimeoutException:
                    latest_ca_price, latest_ca_price_forprint = 'N/A', 'N/A'
                    fake_buy_token = False
                else:
                    latest_ca_price_forprint = 'N/A'

                if latest_ca in self.exclude_list:
                    excluded = True
                    print(Fore.RED + f'Added {latest_ca_name} to exclusion list.')
                else:
                    excluded = False

                print(
                    Fore.GREEN + f'Name: {latest_ca_name} | CA: {latest_ca} | Price: {latest_ca_price_forprint} | Rugcheck alerts: {alert_number} | Honeypot: {latest_ca_honeypot} | LP Lock: {latest_ca_lplock} | Ownership renounced: {latest_ca_ownership}')

                self.database.loc[len(self.database.index)] = [latest_ca_name, latest_ca, latest_ca_price,
                                                               alert_number,
                                                               latest_ca_honeypot, latest_ca_lplock, latest_ca_ownership, excluded]
                print(Fore.YELLOW + f'\nAdded {latest_ca_name} to database...')

                if fake_buy_token:
                    t6 = threading.Thread(target=self.tx_handler,
                                          args=(latest_ca_name, latest_ca, latest_ca_price, None), daemon=True)
                    t6.start()

                self.inoperation = False
                print(Fore.YELLOW + f'\nSleeping for {self.scraper_sleep_time} seconds...')
                time.sleep(self.scraper_sleep_time)

    def updater(self, info):
        if info == 'price':
            while True:
                if len(self.database['Contract']) > 0:
                    for i in range(len(self.database['Contract'])):
                        current_contract = self.database['Contract'][i]
                        price_update_link = f'https://poocoin.app/tokens/{current_contract}'
                        ca_name = self.database['Name'][i]
                        if current_contract not in self.exclude_list:
                            # Price
                            try:
                                self.price_updater_driver.get(price_update_link)
                                ca_price = WebDriverWait(self.price_updater_driver, self.max_scraper_wait).until(
                                    EC.visibility_of_element_located((
                                        By.XPATH,
                                        "/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/span")))

                                try:
                                    ca_price = float(ca_price.text.replace('$', ''))
                                except ValueError:
                                    print(Fore.YELLOW + f'{ca_name} has an unstable price, skipping price')
                                    ca_price = 'N/A'

                                if self.database['Price'][i] == 'N/A':
                                    print(Fore.GREEN + f'Liquidity added to CA {ca_name}!')
                                    fake_buy_token = True
                                else:
                                    fake_buy_token = False
                                self.database['Price'][i] = ca_price

                                if fake_buy_token:
                                    t5 = threading.Thread(target=self.tx_handler,
                                                          args=(self.database['Name'][i], current_contract, ca_price, i,),
                                                          daemon=True)
                                    t5.start()
                            except selenium.common.exceptions.TimeoutException:
                                self.database['Price'][i] = 'N/A'
                            time.sleep(self.updater_sleep_time)

        elif info == 'honeypot':
            while True:
                if len(self.database['Contract']) > 1:
                    for i in range(len(self.database['Contract'])):
                        current_contract = self.database['Contract'][i]
                        ca_name = self.database['Name'][i]
                        # Honeypot
                        try:
                            honeypot_url_ca = f'{self.honeypot_url}{current_contract}'
                            self.honeypot_updater_driver.get(honeypot_url_ca)
                            honeypot_result = WebDriverWait(self.honeypot_updater_driver, self.max_scraper_wait).until(
                                EC.visibility_of_element_located((By.XPATH,
                                                                  "/html/body/div[2]/div[1]/div/div")))
                            if honeypot_result.text == 'Does not seem like a honeypot.':
                                if self.database['Honeypot'][i] is True and self.database['Honeypot'][i] == 'N/A':
                                    print(Fore.GREEN + f'CA {current_contract} just lost its honeypot!')
                                    self.database['Honeypot'][i] = False
                                    self.exclude_list.remove(current_contract)
                            else:
                                if self.database['Honeypot'][i] is False:
                                    self.database['Honeypot'][i] = True
                                    print(Fore.RED + f'CA {ca_name} just became a honeypot!')
                                    if current_contract not in self.exclude_list:
                                        self.exclude_list.append(current_contract)
                        except selenium.common.exceptions.TimeoutException:
                            self.database['Honeypot'][i] = 'N/A'
                    time.sleep(self.updater_sleep_time)

    def token_watcher(self, ca, ca_name):
        fake_token_holding = True
        fake_ca_database_index = self.database.index[self.database['Contract'] == ca].tolist()[0]
        fake_ca_fake_buy_index = self.fake_buy_database.index[self.fake_buy_database['Contract'] == ca].tolist()[0]
        while True:
            if self.fake_buy_database['Contract'][fake_ca_fake_buy_index] not in self.exclude_list:
                current_bought_price = self.database['Price'][fake_ca_database_index]
                remove_ca_name = self.fake_buy_database['Name'][fake_ca_fake_buy_index]
                if current_bought_price > self.fake_buy_database['Entry'][fake_ca_fake_buy_index] * self.takeprofit_x:
                    fake_token_holding = False
                    profit_from_buy = self.fake_buy
                    self.fake_balance = self.fake_balance + profit_from_buy
                    try:
                        self.fake_buy_current_list.remove(remove_ca_name)
                    except ValueError:
                        pass
                    print(Fore.GREEN + f'{ca_name} fake sold at a {self.takeprofit_x}x profit! Balance: {self.fake_balance} BNB')
                elif current_bought_price < self.fake_buy_database['Entry'][fake_ca_fake_buy_index] / self.stoploss_x:
                    fake_token_holding = False
                    profit_from_buy = self.fake_buy / self.stoploss_x
                    self.fake_balance = self.fake_balance - profit_from_buy
                    try:
                        self.fake_buy_current_list.remove(remove_ca_name)
                    except ValueError:
                        pass
                    print(Fore.RED + f'{ca_name} fake sold at a -{self.stoploss_x}x loss! Balance: {self.fake_balance} BNB')
                else:
                    time.sleep(self.fake_mode_sleep)
            else:
                print(Fore.RED + f'Money in {ca_name} lost!')
                break

    def tx_handler(self, ca_name, ca, entry_price, index_n):
        if self.fake_mode:
            if index_n is None:
                ca_index = self.database.index[self.database['Contract'] == ca].tolist()[0]
            else:
                ca_index = index_n
            rugcheck_v = self.database['Rugcheck alerts'][ca_index]
            honeypot_v = str(self.database['Honeypot'][ca_index])
            if rugcheck_v < self.maximum_alerts and honeypot_v == 'False':
                self.fake_buy_database.loc[len(self.fake_buy_database.index)] = [ca_name, ca, entry_price, None]
                self.fake_buy_current_list.append(ca_name)
                self.fake_balance = self.fake_balance - self.fake_buy
                print(Fore.BLUE + f'\nFake bought {ca_name}, watching token for sell point...')
                t4 = threading.Thread(target=self.token_watcher, args=(ca, ca_name,), daemon=True)
                t4.start()
            elif rugcheck_v > self.maximum_alerts:
                print(Fore.RED + f'\n{ca_name} has too many rugcheck alerts and token was not bought!')
            elif honeypot_v == 'True':
                print(Fore.RED + f'\n{ca_name} is a honeypot and token was not bought!')
            else:
                print(Fore.CYAN + 'Not enough info to decide to buy token')

    def run(self):
        print("\n\n")
        cprint(figlet_format(f'Sniper-O-Mancer', font='cosmic', width=150, justify="left"),
               'yellow')
        print(Fore.CYAN + '\n                                                       v0.0.2 Alpha')
        print(Fore.YELLOW + "                                                    Coded by yosharu.")
        print(
            Fore.RED + "                                    THIS SNIPER WAS MADE TO BE USED UNDER CLOSE SUPERVISION! \n                    ANYONE INVOLVED IN THE DEVELOPMENT OF SoM ARE NOT LIABLE FOR ANY LOSSES OCCURED UNDER USE!\n                                      BY USING THIS SNIPER, YOU AGREE TO THESE TERMS.")
        try:
            print(Fore.CYAN + 'Starting threads...')
            t1 = threading.Thread(target=self.scrape_newest_ca, daemon=True)

            # updater
            t2 = threading.Thread(target=self.updater, args=('price',), daemon=True)
            t3 = threading.Thread(target=self.updater, args=('honeypot',), daemon=True)

            t1.start()
            t2.start()
            t3.start()
            print(Fore.CYAN + 'Threads started')

            time.sleep(5)
            while True:
                if self.inoperation is False:
                    n_uptime = getuptime()
                    print(
                        f'\n{Fore.CYAN}-------------------------------------------------------------------\n{Fore.YELLOW}Overview:\nBalance: {Fore.WHITE}{self.fake_balance} BNB\n\n{Fore.YELLOW}Database:{Fore.WHITE}\n{self.database}\n\n{Fore.YELLOW}Currently fake holding:\n{Fore.WHITE}{self.fake_buy_current_list}\n\n{Fore.YELLOW}System:{Fore.WHITE}\nUptime: {n_uptime}\n{Fore.CYAN}-------------------------------------------------------------------')
                    time.sleep(60)
                else:
                    time.sleep(2)
        except KeyboardInterrupt:
            print(Fore.RED + '\nGoodbye.')

            # Simply .quit() didn't work on my system, so here i'm manually killing the Chrome windows with PIDs and task kill
            for process in psutil.process_iter():
                if process.name() == 'chrome.exe' and '--test-type=webdriver' in process.cmdline():
                    with suppress(psutil.NoSuchProcess):
                        self.kill_list.append(process.pid)
            for proc_id in self.kill_list:
                os.kill(int(proc_id), signal.SIGTERM)
            quit()


SniperOMancer().run()
