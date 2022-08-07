#   /$$$$$$            /$$                                        /$$$$$$          /$$      /$$
#  /$$__  $$          |__/                                       /$$__  $$        | $$$    /$$$
# | $$  \__/ /$$$$$$$  /$$  /$$$$$$   /$$$$$$   /$$$$$$         | $$  \ $$        | $$$$  /$$$$  /$$$$$$  /$$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$
# |  $$$$$$ | $$__  $$| $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$$$$$| $$  | $$ /$$$$$$| $$ $$/$$ $$ |____  $$| $$__  $$ /$$_____/ /$$__  $$ /$$__  $$
#  \____  $$| $$  \ $$| $$| $$  \ $$| $$$$$$$$| $$  \__/|______/| $$  | $$|______/| $$  $$$| $$  /$$$$$$$| $$  \ $$| $$      | $$$$$$$$| $$  \__/
#  /$$  \ $$| $$  | $$| $$| $$  | $$| $$_____/| $$              | $$  | $$        | $$\  $ | $$ /$$__  $$| $$  | $$| $$      | $$_____/| $$
# |  $$$$$$/| $$  | $$| $$| $$$$$$$/|  $$$$$$$| $$              |  $$$$$$/        | $$ \/  | $$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$| $$
#  \______/ |__/  |__/|__/| $$____/  \_______/|__/               \______/         |__/     |__/ \_______/|__/  |__/ \_______/ \_______/|__/
#                         | $$
#                         | $$
#                         |__/
# ASCII AART HAHAHA
# BY °° YOSHARU °° 2022
# CHANGELOG:
# v0.1.2:
# - First changelog.
# - Added LP and MC/LP analysis.
# - Added RPC optimization.
# - Added buying/selling of tokens with real wallet.
# - Added honeypot and too high tax loss.
# - Added LP Lock updating.
# - Added MoonArch analysis for even more security.
# - Added a bunch of comments.
# - Added more error catching to minimize errors without sacrificing code quality.
# - Added ASCII lol.
# - Added rounded buy and sell taxes.
# - Fixed print.
# - Fixed initial honeypot and tax grab.
# - Made variables and internals more understandable for future development.
# - Changed maximum minutes in DB from 60 to 30.
# - Redefined codebase.
#
# TIP JAR:
# BSC & ETH: 0x930A400a816D702f4b81B143863859154d7ea209
#
import datetime
import os
import signal
import statistics
import sys
import threading
import time
import pandas as pd
import requests
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
from web3 import Web3

init(autoreset=True, strip=not sys.stdout.isatty())  # strip colors if stdout is redirected


class SniperOMancer:
    # Init
    def __init__(self):
        self.write(Fore.BLUE + 'Initializing...')
        self.version = 'v0.1.2 Alpha'

        # SETTINGS
        self.buy_mode = False
        self.wallet_address = ''
        self.private_key = ''
        self.buy_amount = 0

        self.maximum_buy_tax = 10
        self.maximum_sell_tax = 10
        self.minimum_market_cap = 500
        self.minimum_liquidity = 1000
        self.analyze_mc_liq_ratio = True
        self.lp_lock = False
        self.ownership_renounce = False
        self.verified_contract = False
        self.maximum_alerts = 5
        self.txn_speed = 'standard'

        self.fake_mode = False
        self.token_watcher_sleep = 5
        self.fake_balance = 10
        self.fake_buy = 1

        self.takeprofit_x = 2
        self.stoploss_x = 2
        self.transaction_fee = 0.00088025

        self.maximum_minutes_in_database = 30

        self.telegram_enabled = False
        self.telegram_bot_key = ''
        self.telegram_bot_chat_id = ''

        self.max_scraper_wait = 5
        self.scraper_sleep_time = 20
        self.updater_sleep_time = 5
        self.overview_sleep_time = 60
        self.maximum_database_index = 10

        # INIT
        self.RPC = self.find_closest_rpc()
        self.Web3 = Web3(Web3.HTTPProvider(self.RPC))
        # noinspection PyTypeChecker
        self.pcs_contract = self.Web3.eth.contract(address='0x10ED43C718714eb63d5aA57B78B54704E256024E',
                                                   abi='[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]')
        self.spend = self.Web3.toChecksumAddress("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c")  # wbnb contract address

        pd.set_option("display.precision", 16)
        pd.options.mode.chained_assignment = None  # default='warn'
        self.ser = Service(
            "./chromedriver")  # included in zip, if it isn't, you can download it from here: https://chromedriver.storage.googleapis.com/index.html?path=98.0.4758.102/
        self.op = Options()
        self.op.add_argument("--headless")  # allows you to scrape page without opening the browser window
        self.op.add_argument("--allow-running-insecure-content")  # allows you to scrape jewarch
        self.op.add_argument("--ignore-certificate-errors")  # allows you to scrape jewarch
        self.op.add_argument("--window-size=1920,1080")

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        self.op.add_argument(f'user-agent={user_agent}')

        self.op.add_experimental_option('excludeSwitches', ['enable-logging'])  # remove annoying message
        self.newest_ca_driver = webdriver.Chrome(options=self.op)
        self.price_updater_driver = webdriver.Chrome(options=self.op)
        self.honeypot_updater_driver = webdriver.Chrome(options=self.op)
        self.lplock_updater_driver = webdriver.Chrome(options=self.op)
        self.kill_list = []
        self.inoperation = None
        self.jewarch_url = 'http://70.34.213.32'
        self.moonarch_url = 'https://moonarch.app/token/'
        self.honeypot_url = 'https://honeypot.is/?address='
        self.rugdoc_url = 'https://honeypot.api.rugdoc.io/api/honeypotStatus.js?address='
        self.database = pd.DataFrame(
            columns=['Timestamp', 'Name', 'Contract', 'Price', 'Market Cap', 'Liquidity', 'Buy Tax', 'Sell Tax',
                     'Honeypot.is',
                     'RugDoc',
                     'Rugcheck Alerts', 'Scam',
                     'LP Lock',
                     'Ownership Renounced', 'Verified', 'Excluded', 'Xs', 'Finished'])
        self.internal_database = pd.DataFrame(columns=['Name', 'Contract', 'Entry', 'Current'])
        self.fake_buy_current_list = []
        self.exclude_list = []
        self.x_list = []
        self.reset_done = False
        self.startTime = time.time()

    # grab the wallet balance
    def get_balance(self):
        mybalance = self.Web3.eth.getBalance(self.wallet_address)
        return self.Web3.fromWei(mybalance, 'ether')

    # simple percentage func to help
    def percentage(self, percent, whole):
        return (percent * whole) / 100.0

    # Find lowest latency RPC for fastest bet
    def find_closest_rpc(self):
        self.write(Fore.YELLOW + 'Finding RPC with the lowest latency...')
        rpc_response_time_list = []
        rpc_lists = ['https://bsc.nodereal.io', 'https://binance.ankr.com/', 'https://rpc-bsc.bnb48.club/',
                     'https://bsc-dataseed1.binance.org', 'https://bsc-dataseed2.binance.org',
                     'https://bsc-dataseed3.binance.org', 'https://bsc-dataseed4.binance.org',
                     'https://bsc-dataseed1.defibit.io', 'https://bsc-dataseed2.defibit.io',
                     'https://bsc-dataseed3.defibit.io', 'https://bsc-dataseed4.defibit.io',
                     'https://bsc-dataseed1.ninicoin.io', 'https://bsc-dataseed2.ninicoin.io',
                     'https://bsc-dataseed3.ninicoin.io', 'https://bsc-dataseed4.ninicoin.io', 'https://bscrpc.com']
        for i in rpc_lists:
            rpc_response_time = requests.post(i).elapsed.total_seconds()
            rpc_response_time_list.append(rpc_response_time)
        best_rpc = min(rpc_response_time_list)
        best_rpc = rpc_response_time_list.index(best_rpc)
        best_rpc = rpc_lists[best_rpc]
        return best_rpc

    # Get the uptime
    def get_uptime(self):
        """
        Returns the number of seconds since the program started.
        """
        # do return startTime if you just want the process start time
        n = int(time.time() - self.startTime)
        return str(datetime.timedelta(seconds=n))

    # Print with datetime for debugging
    def write(self, x):
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("[{}] {}".format(str(ts), x))

    # Scraper which refreshes JewArch for new contracts to snipe.
    def scrape_newest_ca(self):
        while True:
            try:
                if self.reset_done:
                    time.sleep(1)
                else:
                    self.inoperation = True

                    # print(Fore.YELLOW + '\nScraping newest jewarch CA...')

                    def get_latest_ca_func():
                        try:
                            self.newest_ca_driver.get(self.jewarch_url)
                            return WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                                EC.visibility_of_element_located((
                                    By.XPATH,
                                    "/html/body/div/div[2]/div/div[2]/div[1]/div[3]/div/div/div/table/tbody/tr[1]/td[4]/div/a[2]")))
                        except selenium.common.exceptions.TimeoutException:
                            get_latest_ca_func()

                    try:
                        latest_ca = get_latest_ca_func()
                    except selenium.common.exceptions.TimeoutException:
                        self.write(Fore.RED + 'Jewarch is down, waiting 60s to retry.')
                        time.sleep(60)
                        latest_ca = get_latest_ca_func()

                    try:
                        latest_ca_link = latest_ca.get_attribute('href')
                        latest_ca = latest_ca.get_attribute('href').replace('https://poocoin.app/tokens/', '')
                    except AttributeError:
                        latest_ca_link = None
                        self.write(Fore.RED + 'JewArch grabbing failed after 3 attempts, exiting...')
                        # Simply .quit() didn't work on my system, so here i'm manually killing the Chrome windows with PIDs and task kill
                        for process in psutil.process_iter():
                            if process.name() == 'chrome.exe' and '--test-type=webdriver' in process.cmdline():
                                with suppress(psutil.NoSuchProcess):
                                    self.kill_list.append(process.pid)
                        for proc_id in self.kill_list:
                            os.kill(int(proc_id), signal.SIGTERM)
                        quit()

                    if len(self.database['Contract']) > 0 and latest_ca in self.database["Contract"].values:
                        # print(Fore.CYAN + 'Contract already in database, continuing...')
                        # print(Fore.YELLOW + f'\nSleeping for {self.scraper_sleep_time} seconds...')
                        time.sleep(self.scraper_sleep_time)
                    else:
                        # print(Fore.YELLOW + 'New CA detected, getting info...')

                        ########################
                        # Rugcheck via JewArch #
                        ########################
                        try:
                            latest_ca_button = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                                EC.visibility_of_element_located((By.XPATH,
                                                                  "/html/body/div/div[2]/div/div[2]/div[1]/div[3]/div/div/div/table/tbody/tr[1]/td[3]/div/a")))
                            try:
                                latest_ca_button.click()
                            except selenium.common.exceptions.ElementNotInteractableException:
                                latest_ca = get_latest_ca_func()
                                latest_ca_button = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                                    EC.visibility_of_element_located((By.XPATH,
                                                                      "/html/body/div/div[2]/div/div[2]/div[1]/div[3]/div/div/div/table/tbody/tr[1]/td[3]/div/a")))
                                latest_ca_button.click()
                            try:
                                rugcheck = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                                    EC.visibility_of_element_located((By.XPATH,
                                                                      "/html/body/div[2]/div[1]/div/div/div/div/div[2]/button[4]/div/div/span")))

                                latest_ca_alert_number = int(rugcheck.text)
                                if latest_ca_alert_number > self.maximum_alerts:
                                    self.exclude_list.append(latest_ca)
                                latest_ca_scam = False
                            except selenium.common.exceptions.TimeoutException:
                                rugcheck = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                                    EC.visibility_of_element_located((By.XPATH,
                                                                      "/html/body/div[2]/div[1]/div/div/div/div/div[2]/button[4]/div/span")))
                                if rugcheck.get_attribute(
                                        "title") == 'Moonarch rugcheck found suspicious code in the token contract':
                                    latest_ca_alert_number = 'N/A'
                                    latest_ca_scam = True
                                    if latest_ca not in self.exclude_list:
                                        self.exclude_list.append(latest_ca)
                                else:
                                    latest_ca_alert_number = 'N/A'
                                    latest_ca_scam = False

                        except selenium.common.exceptions.TimeoutException:
                            latest_ca_alert_number = 'N/A'
                            latest_ca_scam = 'N/A'

                        #########################
                        # Ownership via JewArch #
                        #########################
                        try:
                            ownership_renounce_check = WebDriverWait(self.newest_ca_driver,
                                                                     self.max_scraper_wait).until(
                                EC.visibility_of_element_located((By.XPATH,
                                                                  "/html/body/div[2]/div[1]/div/div/div/div/div[3]/div[2]/ul/li[8]/span")))
                            if ownership_renounce_check.text == ' Renounced ':
                                latest_ca_ownership = True
                            else:
                                latest_ca_ownership = False

                        except selenium.common.exceptions.TimeoutException:
                            latest_ca_ownership = 'N/A'

                        ####################################
                        # Honeypot and Tax via Honeypot.is #
                        ####################################
                        try:
                            honeypot_url_ca = f'{self.honeypot_url}{latest_ca}'
                            self.newest_ca_driver.get(honeypot_url_ca)

                            honeypot_ornot = WebDriverWait(self.newest_ca_driver,
                                                           self.max_scraper_wait).until(
                                EC.visibility_of_element_located((By.XPATH,
                                                                  "/html/body/div[2]/div[1]/div/div")))

                            if honeypot_ornot.text == 'Yup, honeypot. Run the fuck away.':
                                latest_ca_honeypot = True
                                if latest_ca not in self.exclude_list:
                                    self.exclude_list.append(latest_ca)
                            elif honeypot_ornot.text == 'Does not seem like a honeypot.':
                                latest_ca_honeypot = False
                            else:
                                latest_ca_honeypot = 'N/A'

                        except selenium.common.exceptions.TimeoutException:
                            latest_ca_honeypot = 'N/A'

                        try:
                            try:
                                tax = WebDriverWait(self.newest_ca_driver,
                                                    self.max_scraper_wait).until(
                                    EC.visibility_of_element_located((By.XPATH,
                                                                      "/html/body/div[2]/div[1]/div/p[6]")))
                                latest_ca_buy_tax = tax.text.split('%', 1)[0]
                                latest_ca_sell_tax = tax.text.split('%', 1)[1]

                                latest_ca_buy_tax = float(
                                    latest_ca_buy_tax.replace('Buy Tax: ', '').replace('%', '').replace('\n', ''))
                                latest_ca_sell_tax = float(
                                    latest_ca_sell_tax.replace('Sell Tax: ', '').replace('%', '').replace('\n', ''))
                            except (IndexError, selenium.common.exceptions.TimeoutException):
                                try:
                                    tax = WebDriverWait(self.newest_ca_driver,
                                                        self.max_scraper_wait).until(
                                        EC.visibility_of_element_located((By.XPATH,
                                                                          "/html/body/div[2]/div[1]/div/p[5]")))

                                    latest_ca_buy_tax = tax.text.split('%', 1)[0]
                                    latest_ca_sell_tax = tax.text.split('%', 1)[1]

                                    latest_ca_buy_tax = float(
                                        latest_ca_buy_tax.replace('Buy Tax: ', '').replace('%', '').replace('\n', ''))
                                    latest_ca_sell_tax = float(
                                        latest_ca_sell_tax.replace('Sell Tax: ', '').replace('%', '').replace('\n', ''))
                                except (IndexError, selenium.common.exceptions.TimeoutException):
                                    tax = WebDriverWait(self.newest_ca_driver,
                                                        self.max_scraper_wait).until(
                                        EC.visibility_of_element_located((By.XPATH,
                                                                          "/html/body/div[2]/div[1]/div/p[9]")))

                                    latest_ca_buy_tax = tax.text.split('%', 1)[0]
                                    latest_ca_sell_tax = tax.text.split('%', 1)[1]

                                    latest_ca_buy_tax = float(
                                        latest_ca_buy_tax.replace('Buy Tax: ', '').replace('%', '').replace('\n', ''))
                                    latest_ca_sell_tax = float(
                                        latest_ca_sell_tax.replace('Sell Tax: ', '').replace('%', '').replace('\n', ''))

                        except selenium.common.exceptions.TimeoutException:
                            latest_ca_buy_tax, latest_ca_sell_tax = 'N/A', 'N/A'

                        #############################################
                        # Price, Name, MC and Liquidity via PooCoin #
                        #############################################
                        self.newest_ca_driver.get(latest_ca_link)
                        try:
                            latest_ca_name = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                                EC.visibility_of_element_located((
                                    By.XPATH,
                                    "/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/h1"))).text
                            latest_ca_name = latest_ca_name.split(' (', 1)[0]
                        except selenium.common.exceptions.TimeoutException:
                            self.newest_ca_driver.get(latest_ca_link)
                            latest_ca_name = self.newest_ca_driver.title
                            latest_ca_name = latest_ca_name.split(' price', 1)[0]

                        try:
                            latest_ca_price = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                                EC.visibility_of_element_located((By.XPATH,
                                                                  "/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/span")))
                            try:
                                latest_ca_price = float(latest_ca_price.text.replace('$', ''))
                            except ValueError:
                                self.write(Fore.YELLOW + f'{latest_ca_name} has an unstable price, skipping price')
                                latest_ca_price = 'N/A'

                        except selenium.common.exceptions.TimeoutException:
                            latest_ca_price, latest_ca_price_forprint = 'N/A', 'N/A'

                        try:
                            latest_ca_mcap = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                                EC.visibility_of_element_located((By.XPATH,
                                                                  "/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]")))
                            try:
                                latest_ca_mcap = int(latest_ca_mcap.text.replace('$', '').replace(',', ''))
                            except ValueError:
                                self.write(Fore.YELLOW + f'{latest_ca_name} has an unstable market cap, skipping...')
                                latest_ca_mcap = 'N/A'

                        except selenium.common.exceptions.TimeoutException:
                            latest_ca_mcap = 'N/A'

                        if latest_ca_mcap != 'N/A' and latest_ca_mcap > 9999999:
                            latest_ca_mcap = 'N/A'

                        try:
                            latest_ca_liquidity = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                                EC.visibility_of_element_located((By.XPATH,
                                                                  "/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div/div/span")))
                            try:
                                latest_ca_liquidity = int(
                                    latest_ca_liquidity.text.replace('$', '').replace(',', '').replace('(', '').replace(
                                        ')', ''))
                            except ValueError:
                                self.write(Fore.YELLOW + f'{latest_ca_name} has an unstable LP, skipping...')
                                latest_ca_liquidity = 'N/A'

                        except selenium.common.exceptions.TimeoutException:
                            latest_ca_liquidity = 'N/A'

                        ##########
                        # RugDoc #
                        ##########
                        rugdoc_link = f'{self.rugdoc_url}{latest_ca}&chain=bsc'
                        try:
                            rugdoc_status = requests.post(rugdoc_link).json()
                        except requests.exceptions.ConnectionError:
                            try:
                                rugdoc_status = requests.post(rugdoc_link).json()
                            except requests.exceptions.ConnectionError:
                                try:
                                    rugdoc_status = requests.post(rugdoc_link).json()
                                except requests.exceptions.ConnectionError:
                                    self.write(Fore.RED + 'RugDoc API is not responding...')
                                    rugdoc_status = {'status': 'N/A'}
                        try:
                            rugdoc_status = rugdoc_status['status']
                        except KeyError:
                            try:
                                rugdoc_status = requests.post(rugdoc_link).json()
                                rugdoc_status = rugdoc_status['status']
                            except KeyError:
                                rugdoc_status = 'N/A'
                        if rugdoc_status == 'OK':
                            latest_ca_rugdoc = 'Clean'
                        else:
                            latest_ca_rugdoc = 'Dirty'
                            self.exclude_list.append(latest_ca)

                        ##################################################
                        # LP Lock and Contract Verification via Moonarch #
                        ##################################################
                        latest_ca_moonarch_link = f'{self.moonarch_url}{latest_ca}'
                        self.newest_ca_driver.get(latest_ca_moonarch_link)
                        latest_ca_verified = WebDriverWait(self.newest_ca_driver, self.max_scraper_wait).until(
                            EC.visibility_of_element_located((
                                By.XPATH,
                                "/html/body/div/div[3]/div[2]/div/div/div[3]/div[2]/div[1]"))).get_attribute("class")
                        if latest_ca_verified == 'not-verified':
                            latest_ca_verified = False
                        else:
                            latest_ca_verified = True

                        try:
                            lplock = WebDriverWait(self.newest_ca_driver,
                                                   self.max_scraper_wait).until(
                                EC.visibility_of_element_located((By.XPATH,
                                                                  "/html/body/div/div[3]/div[2]/div/div/div[3]/div[1]/div/div/h5"))).text
                            if lplock == 'Liquidity locks on PancakeSwap v2':
                                latest_ca_lplock = True
                            else:
                                latest_ca_lplock = False
                        except selenium.common.exceptions.TimeoutException:
                            latest_ca_lplock = False

                        if latest_ca in self.exclude_list:
                            excluded = True
                            self.write(Fore.RED + f'Added {latest_ca_name} to exclusion list.')
                        else:
                            excluded = False

                        if latest_ca_price != 'N/A':
                            latest_ca_price_forprint = f'{latest_ca_price:.20f}'
                        else:
                            latest_ca_price_forprint = 'N/A'

                        if latest_ca_buy_tax != 'N/A' and latest_ca_sell_tax != 'N/A':
                            latest_ca_buy_tax, latest_ca_sell_tax = round(latest_ca_buy_tax, 1), round(
                                latest_ca_sell_tax, 1)

                        timestamp = time.time()

                        if latest_ca_name != 'PooCoin BSC Charts':
                            self.database.loc[len(self.database.index)] = [timestamp, latest_ca_name, latest_ca,
                                                                           latest_ca_price,
                                                                           latest_ca_mcap, latest_ca_liquidity,
                                                                           latest_ca_buy_tax,
                                                                           latest_ca_sell_tax, latest_ca_honeypot,
                                                                           latest_ca_rugdoc,
                                                                           latest_ca_alert_number, latest_ca_scam,
                                                                           latest_ca_lplock,
                                                                           latest_ca_ownership, latest_ca_verified,
                                                                           excluded, None, False]

                            print(
                                Fore.CYAN + f'\n----------------------------------------------\n{Fore.BLUE}NEW TOKEN\n{Fore.GREEN}Name: {Fore.WHITE}{latest_ca_name} \n{Fore.GREEN}CA: {Fore.WHITE}{latest_ca} \n{Fore.GREEN}Price: {Fore.WHITE}{latest_ca_price_forprint} \n{Fore.GREEN}Market Cap: {Fore.WHITE}{latest_ca_mcap}\n{Fore.GREEN}LP: {Fore.WHITE}{latest_ca_liquidity} \n{Fore.GREEN}Buy Tax: {Fore.WHITE}{latest_ca_buy_tax} \n{Fore.GREEN}Sell Tax: {Fore.WHITE}{latest_ca_sell_tax} \n{Fore.GREEN}Rugcheck Alerts: {Fore.WHITE}{latest_ca_alert_number} \n{Fore.GREEN}Honeypot.is: {Fore.WHITE}{latest_ca_honeypot} \n{Fore.GREEN}RugDoc: {Fore.WHITE}{latest_ca_rugdoc} \n{Fore.GREEN}LP Lock: {Fore.WHITE}{latest_ca_lplock} \n{Fore.GREEN}Ownership renounced: {Fore.WHITE}{latest_ca_ownership}\n{Fore.GREEN}Verified: {Fore.WHITE}{latest_ca_verified}\n{Fore.CYAN}----------------------------------------------\n')
                            self.write(Fore.YELLOW + f'Added {latest_ca_name} to database...')

                            t6 = threading.Thread(target=self.tx_handler,
                                                  args=(latest_ca_name, latest_ca, latest_ca_price, None, True,),
                                                  daemon=True)
                            t6.start()
                            self.inoperation = False
                            # print(Fore.YELLOW + f'\nSleeping for {self.scraper_sleep_time} seconds...')
                            time.sleep(self.scraper_sleep_time)
            except ValueError as e:
                self.write(e)
                time.sleep(self.scraper_sleep_time)

    # Updates database
    def updater(self, info):
        while True:
            if len(self.database.index) > 0:
                if info == 'price':
                    #############################################
                    # Price, Name, MC and Liquidity via PooCoin #
                    #############################################
                    while True:
                        try:
                            for i in range(len(self.database['Contract'])):
                                if self.reset_done:
                                    break
                                else:
                                    current_contract = self.database['Contract'][i]
                                    price_update_link = f'https://poocoin.app/tokens/{current_contract}'
                                    ca_name = self.database['Name'][i]
                                    ca_timestamp = int(self.database['Timestamp'][i])
                                    seconds = self.maximum_minutes_in_database * 60
                                    if time.time() - ca_timestamp >= seconds:
                                        self.database['Finished'][i] = True
                                    if current_contract not in self.exclude_list and self.database['Finished'][
                                        i] == False:
                                        try:
                                            self.price_updater_driver.get(price_update_link)
                                            ca_price = WebDriverWait(self.price_updater_driver,
                                                                     self.max_scraper_wait).until(
                                                EC.visibility_of_element_located((
                                                    By.XPATH,
                                                    "/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/span")))

                                            try:
                                                ca_price = float(ca_price.text.replace('$', ''))
                                            except ValueError:
                                                ca_price = 'N/A'

                                            ca_mcap = WebDriverWait(self.price_updater_driver,
                                                                    self.max_scraper_wait).until(
                                                EC.visibility_of_element_located((By.XPATH,
                                                                                  "/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]")))
                                            try:
                                                ca_mcap = int(ca_mcap.text.replace('$', '').replace(',', ''))
                                            except ValueError:
                                                ca_mcap = 'N/A'

                                            if self.database['Price'][i] == 'N/A' and ca_price != 'N/A':
                                                self.write(Fore.GREEN + f'Liquidity added to CA {ca_name}!')
                                                fake_buy_token = True
                                            else:
                                                fake_buy_token = False

                                            if ca_mcap != 'N/A' and ca_mcap > 9999999:
                                                ca_mcap = 'N/A'
                                                fake_buy_token = False

                                            try:
                                                ca_liquidity = WebDriverWait(self.price_updater_driver,
                                                                             self.max_scraper_wait).until(
                                                    EC.visibility_of_element_located((By.XPATH,
                                                                                      "/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div/div/span")))
                                                try:
                                                    ca_liquidity = int(
                                                        ca_liquidity.text.replace('$', '').replace(',',
                                                                                                   '').replace(
                                                            '(', '').replace(')', ''))
                                                except ValueError:
                                                    self.write(
                                                        Fore.YELLOW + f'{ca_name} has an unstable LP, skipping...')
                                                    ca_liquidity = 'N/A'

                                            except selenium.common.exceptions.TimeoutException:
                                                ca_liquidity = 'N/A'

                                            self.database['Price'][i] = ca_price
                                            self.database['Market Cap'][i] = ca_mcap
                                            self.database['Liquidity'][i] = ca_liquidity

                                            if fake_buy_token:
                                                t5 = threading.Thread(target=self.tx_handler,
                                                                      args=(
                                                                          ca_name, current_contract,
                                                                          ca_price,
                                                                          i, False,),
                                                                      daemon=True)
                                                t5.start()
                                        except selenium.common.exceptions.TimeoutException:
                                            self.database['Price'][i] = 'N/A'
                                            self.database['Market Cap'][i] = 'N/A'
                                            self.database['Liquidity'][i] = 'N/A'
                                        time.sleep(self.updater_sleep_time)
                        except KeyError:
                            time.sleep(self.updater_sleep_time)

                elif info == 'honeypot':
                    ####################################
                    # Honeypot and Tax via Honeypot.is #
                    ####################################
                    while True:
                        try:
                            for i in range(len(self.database['Contract'])):
                                current_contract = self.database['Contract'][i]
                                ca_name = self.database['Name'][i]
                                ca_timestamp = int(self.database['Timestamp'][i])
                                seconds = self.maximum_minutes_in_database * 60
                                if time.time() - ca_timestamp >= seconds:
                                    self.database['Finished'][i] = True
                                if self.database['Finished'][i] == False:
                                    try:
                                        honeypot_url_ca = f'{self.honeypot_url}{current_contract}'
                                        self.honeypot_updater_driver.get(honeypot_url_ca)

                                        honeypot_ornot = WebDriverWait(self.honeypot_updater_driver,
                                                                       self.max_scraper_wait).until(
                                            EC.visibility_of_element_located((By.XPATH,
                                                                              "/html/body/div[2]/div[1]/div/div")))

                                        if honeypot_ornot.text == 'Yup, honeypot. Run the fuck away.' and \
                                                self.database['Honeypot.is'][i] == 'N/A':
                                            self.database['Honeypot.is'][i] = True
                                            self.database['Excluded'][i] = True
                                            self.write(Fore.RED + f'{ca_name} just became a honeypot!')
                                            if current_contract not in self.exclude_list:
                                                self.exclude_list.append(current_contract)
                                        elif honeypot_ornot.text == 'Does not seem like a honeypot.':
                                            if self.database['Honeypot.is'][i] == True:
                                                self.write(Fore.GREEN + f'{ca_name} just lost its honeypot!')
                                            if current_contract in self.exclude_list:
                                                self.exclude_list.remove(current_contract)
                                            self.database['Honeypot.is'][i] = False
                                            self.database['Excluded'][i] = False

                                    except selenium.common.exceptions.TimeoutException:
                                        self.database['Honeypot.is'][i] = 'N/A'

                                    try:
                                        try:
                                            tax = WebDriverWait(self.honeypot_updater_driver,
                                                                self.max_scraper_wait).until(
                                                EC.visibility_of_element_located((By.XPATH,
                                                                                  "/html/body/div[2]/div[1]/div/p[6]")))
                                            buy_tax = tax.text.split('%', 1)[0]
                                            sell_tax = tax.text.split('%', 1)[1]

                                            buy_tax = float(
                                                buy_tax.replace('Buy Tax: ', '').replace('%', '').replace('\n', ''))
                                            sell_tax = float(
                                                sell_tax.replace('Sell Tax: ', '').replace('%', '').replace('\n', ''))
                                        except (IndexError, selenium.common.exceptions.TimeoutException):
                                            try:
                                                tax = WebDriverWait(self.honeypot_updater_driver,
                                                                    self.max_scraper_wait).until(
                                                    EC.visibility_of_element_located((By.XPATH,
                                                                                      "/html/body/div[2]/div[1]/div/p[5]")))

                                                buy_tax = tax.text.split('%', 1)[0]
                                                sell_tax = tax.text.split('%', 1)[1]

                                                buy_tax = float(
                                                    buy_tax.replace('Buy Tax: ', '').replace('%', '').replace('\n', ''))
                                                sell_tax = float(
                                                    sell_tax.replace('Sell Tax: ', '').replace('%', '').replace('\n',
                                                                                                                ''))
                                            except (IndexError, selenium.common.exceptions.TimeoutException):
                                                tax = WebDriverWait(self.honeypot_updater_driver,
                                                                    self.max_scraper_wait).until(
                                                    EC.visibility_of_element_located((By.XPATH,
                                                                                      "/html/body/div[2]/div[1]/div/p[9]")))

                                                buy_tax = tax.text.split('%', 1)[0]
                                                sell_tax = tax.text.split('%', 1)[1]

                                                buy_tax = float(
                                                    buy_tax.replace('Buy Tax: ', '').replace('%', '').replace('\n', ''))
                                                sell_tax = float(
                                                    sell_tax.replace('Sell Tax: ', '').replace('%', '').replace('\n',
                                                                                                                ''))

                                        if buy_tax != 'N/A' and sell_tax != 'N/A':
                                            buy_tax, sell_tax = round(buy_tax, 1), round(sell_tax, 1)

                                        if buy_tax > 75 and sell_tax > 75:
                                            self.write(Fore.RED + f'{ca_name} just became a honeypot (tax)!')
                                            if current_contract not in self.exclude_list:
                                                self.exclude_list.append(current_contract)
                                            self.database['Excluded'][i] = True

                                        if self.database['Buy Tax'][i] != 'N/A' and self.database['Sell Tax'][
                                            i] != 'N/A':
                                            if self.database['Buy Tax'][i] != buy_tax:
                                                old_buy_tax = self.database['Buy Tax'][i]
                                                self.write(
                                                    Fore.RED + f'{ca_name} just changed their buy tax! Old tax: {old_buy_tax} | New tax: {buy_tax}')
                                            elif self.database['Sell Tax'][i] != sell_tax:
                                                old_sell_tax = self.database['Sell Tax'][i]
                                                self.write(
                                                    Fore.RED + f'{ca_name} just changed their sell tax! Old tax: {old_sell_tax} | New tax: {sell_tax}')
                                            elif self.database['Buy Tax'][i] != buy_tax and self.database['Sell Tax'][
                                                i] != sell_tax:
                                                old_buy_tax = self.database['Buy Tax'][i]
                                                old_sell_tax = self.database['Sell Tax'][i]
                                                self.write(
                                                    Fore.RED + f'{ca_name} just changed their taxes! Old tax: {old_buy_tax} / {old_sell_tax} | New tax: {buy_tax} / {sell_tax}')

                                        self.database['Buy Tax'][i] = buy_tax
                                        self.database['Sell Tax'][i] = sell_tax

                                        t5 = threading.Thread(target=self.tx_handler,
                                                              args=(
                                                                  ca_name, current_contract,
                                                                  self.database['Price'][i],
                                                                  i, False,),
                                                              daemon=True)
                                        t5.start()

                                    except selenium.common.exceptions.TimeoutException:
                                        self.database['Buy Tax'][i] = 'N/A'
                                        self.database['Sell Tax'][i] = 'N/A'

                            time.sleep(self.updater_sleep_time)
                        except KeyError:
                            time.sleep(self.updater_sleep_time)

                elif info == 'lplock':
                    ###########
                    # LP Lock #
                    ###########
                    while True:
                        try:
                            for i in range(len(self.database['Contract'])):
                                current_contract = self.database['Contract'][i]
                                ca_name = self.database['Name'][i]
                                if self.reset_done:
                                    break
                                else:
                                    lplock_url_ca = f'{self.moonarch_url}{current_contract}'
                                    self.lplock_updater_driver.get(lplock_url_ca)
                                    try:
                                        lplock = WebDriverWait(self.lplock_updater_driver,
                                                               self.max_scraper_wait).until(
                                            EC.visibility_of_element_located((By.XPATH,
                                                                              "/html/body/div/div[3]/div[2]/div/div/div[3]/div[1]/div/div/h5"))).text
                                        if lplock == 'Liquidity locks on PancakeSwap v2':
                                            if self.database['LP Lock'][i] == 'N/A' or self.database['LP Lock'][i] == False:
                                                self.write(Fore.GREEN + f'{ca_name} just locked their LP!')
                                            self.database['LP Lock'][i] = True
                                        else:
                                            self.database['LP Lock'][i] = False
                                    except selenium.common.exceptions.TimeoutException:
                                        self.database['LP Lock'][i] = False
                            time.sleep(self.updater_sleep_time)
                        except KeyError:
                            time.sleep(self.updater_sleep_time)

    # Monitors and sells bought tokens
    def token_watcher(self, ca, ca_name):
        while True:
            if self.reset_done:
                time.sleep(1)
            else:
                real_ca_database_index = self.database.index[self.database['Contract'] == ca].tolist()[0]
                internal_ca_index = \
                    self.internal_database.index[self.internal_database['Contract'] == ca].tolist()[0]
                if self.internal_database['Contract'][internal_ca_index] not in self.exclude_list and \
                        self.database['Price'][real_ca_database_index] != 'N/A' and self.database['Finished'][
                    real_ca_database_index] == False:

                    real_ca_database_index = self.database.index[self.database['Contract'] == ca].tolist()[0]
                    internal_ca_index = \
                        self.internal_database.index[self.internal_database['Contract'] == ca].tolist()[0]

                    current_bought_price = self.database['Price'][real_ca_database_index]
                    remove_ca_name = self.internal_database['Name'][internal_ca_index]

                    x_since_entry = self.database['Price'][real_ca_database_index] / self.internal_database['Entry'][
                        internal_ca_index]
                    self.database['Xs'][real_ca_database_index] = x_since_entry
                    try:
                        sell_tax = float(self.database['Sell Tax'][real_ca_database_index])
                    except ValueError:
                        sell_tax = 0
                    sell_tax_takeprofitx = self.percentage(sell_tax, self.takeprofit_x)
                    sell_tax_stoplossx = self.percentage(sell_tax, self.stoploss_x)
                    takeprofit = self.takeprofit_x + sell_tax_takeprofitx
                    stoploss = self.stoploss_x + sell_tax_stoplossx

                    if current_bought_price > float(
                            self.internal_database['Entry'][internal_ca_index]) * takeprofit:
                        profit_from_buy = self.fake_buy * self.takeprofit_x
                        profit_from_buy = profit_from_buy - self.percentage(sell_tax, profit_from_buy)
                        self.fake_balance = self.fake_balance + (profit_from_buy - self.transaction_fee)
                        try:
                            self.fake_buy_current_list.remove(remove_ca_name)
                        except ValueError:
                            pass

                        if self.fake_mode:
                            self.write(
                                Fore.GREEN + f'{ca_name} fake sold at a {self.takeprofit_x}x profit! Balance: {self.fake_balance} BNB')

                        if self.buy_mode:
                            real_balance = self.get_balance()
                            self.write(
                                Fore.GREEN + f'Selling {ca_name} at a {self.takeprofit_x}x profit! Balance: {real_balance} BNB')
                            self.place_order(ca, 'sell')

                        self.database['Finished'][real_ca_database_index] = True
                        self.x_list.append(self.database['Xs'][real_ca_database_index])
                        break
                    elif current_bought_price < float(
                            self.internal_database['Entry'][internal_ca_index]) / stoploss:
                        profit_from_buy = self.fake_buy / self.stoploss_x
                        self.fake_balance = self.fake_balance - (profit_from_buy + self.transaction_fee)
                        try:
                            self.fake_buy_current_list.remove(remove_ca_name)
                        except ValueError:
                            pass

                        if self.fake_mode:
                            self.write(
                                Fore.RED + f'{ca_name} fake sold at a {self.stoploss_x}x loss! Balance: {self.fake_balance} BNB')

                        if self.buy_mode:
                            self.write(Fore.RED + f'Selling {ca_name} at a {self.takeprofit_x}x profit!')
                            self.place_order(ca, 'sell')

                        self.database['Finished'][real_ca_database_index] = True
                        self.x_list.append(self.database['Xs'][real_ca_database_index])
                        break
                    else:
                        time.sleep(self.token_watcher_sleep)
                elif self.database['Finished'][real_ca_database_index] == True:
                    real_ca_database_index = self.database.index[self.database['Contract'] == ca].tolist()[0]
                    internal_ca_index = self.internal_database.index[self.internal_database['Contract'] == ca].tolist()[
                        0]
                    remove_ca_name = self.internal_database['Name'][internal_ca_index]
                    token_x = float(self.database['Xs'][real_ca_database_index])
                    profit = self.fake_buy * token_x
                    self.fake_balance = self.fake_balance + profit
                    if profit > self.fake_buy:
                        try:
                            self.fake_buy_current_list.remove(remove_ca_name)
                        except ValueError:
                            pass

                        if self.fake_mode:
                            self.write(
                                Fore.GREEN + f'{ca_name} fake sold at a {token_x}x profit because of inactivity!')

                        if self.buy_mode:
                            self.write(Fore.GREEN + f'{ca_name} sold at a {token_x}x profit because of inactivity!')
                            self.place_order(ca, 'sell')
                    elif profit < self.fake_buy:
                        if self.fake_mode:
                            self.write(Fore.RED + f'{ca_name} fake sold at a {token_x}x loss because of inactivity!')

                        if self.buy_mode:
                            self.write(Fore.RED + f'{ca_name} sold at a {token_x}x profit because of inactivity!')
                            self.place_order(ca, 'sell')
                    self.x_list.append(self.database['Xs'][real_ca_database_index])
                    break
                else:
                    internal_ca_index = \
                        self.internal_database.index[self.internal_database['Contract'] == ca].tolist()[0]
                    remove_ca_name = self.internal_database['Name'][internal_ca_index]
                    if self.fake_mode:
                        self.write(
                            Fore.RED + f'Money in {ca_name} fake lost! This is either due to the token becoming a honeypot or the taxes skyrocket. Money is assumed lost.')

                    if self.buy_mode:
                        self.write(
                            Fore.RED + f'Money in {ca_name} lost! This is either due to the token becoming a honeypot or the taxes skyrocket. Money is assumed lost.')

                    try:
                        self.fake_buy_current_list.remove(remove_ca_name)
                    except ValueError:
                        pass
                    self.x_list.append(self.database['Xs'][real_ca_database_index])
                    break

    # Token buying decision
    def tx_handler(self, ca_name, ca, entry_price, index_n, verbose):
        if (self.fake_mode and self.fake_balance >= self.fake_buy) or (
                self.buy_mode and self.real_balance >= self.buy_amount):
            try:
                if index_n is None:
                    ca_index = self.database.index[self.database['Contract'] == ca].tolist()[0]
                else:
                    ca_index = index_n
                ca_index_lost = False
            except IndexError:
                ca_index_lost = True
                ca_index = None
            if not ca_index_lost:
                try:
                    rugcheck_v = int(self.database['Rugcheck Alerts'][ca_index])
                except ValueError:
                    rugcheck_v = 999999999999999999999999999

                honeypot_v = str(self.database['Honeypot.is'][ca_index])
                price_v = str(self.database['Price'][ca_index])

                try:
                    mcap_v = float(self.database['Market Cap'][ca_index])
                except ValueError:
                    mcap_v = -1

                rugdoc_v = self.database['RugDoc'][ca_index]

                try:
                    lp_v = float(self.database['Liquidity'][ca_index])
                except ValueError:
                    lp_v = -1

                try:
                    buy_tax = float(self.database['Buy Tax'][ca_index])
                    sell_tax = float(self.database['Sell Tax'][ca_index])
                except ValueError:
                    buy_tax, sell_tax = 999999999999999999999999999, 99999999999999999999999999999999

                ownership_v = self.database['Ownership Renounced'][ca_index]
                if self.ownership_renounce is False:
                    ownership_v = True

                ca_x = self.database['Xs'][ca_index]

                if self.analyze_mc_liq_ratio and (mcap_v != -1 or lp_v != -1):
                    try:
                        if 0.6 < mcap_v / lp_v < 1.4:
                            ratio_sus = True
                        else:
                            ratio_sus = False
                    except ZeroDivisionError:
                        ratio_sus = False
                else:
                    ratio_sus = False

                lplock_v = self.database['LP Lock'][ca_index]
                if self.lp_lock == False:
                    lplock_v = True

                if buy_tax <= self.maximum_buy_tax and sell_tax <= self.maximum_sell_tax and rugcheck_v <= self.maximum_alerts and honeypot_v == 'False' and buy_tax != 'N/A' and sell_tax != 'N/A' and rugdoc_v == 'Clean' and mcap_v >= self.minimum_market_cap and lp_v >= self.minimum_liquidity and ratio_sus is False and lplock_v == True and ca_x == None and ownership_v == True:
                    try:
                        buy_tax = float(self.database['Buy Tax'][ca_index])
                    except ValueError:
                        buy_tax = 0

                    self.internal_database.loc[len(self.internal_database.index)] = [ca_name, ca, entry_price, None]
                    self.fake_buy_current_list.append(ca_name)
                    self.fake_balance = self.fake_balance - (self.fake_buy + self.transaction_fee)
                    actual_fake_buy = self.fake_buy - self.percentage(buy_tax, self.fake_buy)

                    if self.fake_mode:
                        self.write(
                            Fore.BLUE + f'Fake bought {ca_name} for {self.fake_buy} BNB (with tax: {actual_fake_buy} BNB), watching token for sell point...')

                    if self.buy_mode:
                        self.write(Fore.BLUE + f'Buying {ca_name} for {self.buy_amount} BNB @ {price_v}...')
                        self.place_order(ca, 'buy')

                    t4 = threading.Thread(target=self.token_watcher, args=(ca, ca_name,), daemon=True)
                    t4.start()

                    if self.telegram_enabled:
                        lp_lock = self.database['LP Lock'][ca_index]
                        ownership = self.database['Ownership Renounced'][ca_index]
                        poocoin_link = f'[💩](https://poocoin.app/tokens/{ca})'
                        dexscreener_link = f'[🤖](https://dexscreener.com/bsc/{ca})'
                        moonarch_link = f'[🌙](https://moonarch.app/token/{ca})'
                        tgmessage = f'*NEWLY LAUNCHED SHITCOIN DETECTED:* %0A *Name*: {ca_name} %0A *CA*: {ca} %0A *Price*: {price_v} %0A *Market Cap*: {mcap_v} %0A *LP*: {lp_v} %0A *Buy Tax*: {buy_tax} %0A *Sell Tax*: {sell_tax} %0A *Honeypot.is*: {honeypot_v} %0A *RugDoc*: {rugdoc_v} %0A *LP Lock*: {lp_lock} %0A *Ownership renounced*: {ownership} %0A {poocoin_link} %0A {dexscreener_link} %0A {moonarch_link} %0A%0A _If i posted the CA, this means it passed Honeypot.is, Rugcheck and RugDoc. It does NOT guarantee future results._ %0A_Not financial advice, DYOR!_'
                        requests.post(
                            f'https://api.telegram.org/bot{self.telegram_bot_key}/sendMessage?chat_id={self.telegram_bot_chat_id}&text={tgmessage}&parse_mode=Markdown')
                        self.write(Fore.CYAN + 'Telegram message sent')
                elif rugcheck_v > self.maximum_alerts and rugcheck_v != 999999999999999999999999999:
                    if verbose:
                        self.write(Fore.RED + f'{ca_name} has too many rugcheck alerts and was not bought!')
                elif honeypot_v == 'True':
                    if verbose:
                        self.write(Fore.RED + f'{ca_name} is a honeypot and was not bought!')
                elif rugdoc_v == 'Dirty':
                    if verbose:
                        self.write(Fore.RED + f'{ca_name} was dirty and was not bought!')
                elif buy_tax >= self.maximum_buy_tax and sell_tax >= self.maximum_sell_tax:
                    if verbose:
                        self.write(Fore.RED + f'{ca_name} had too high tax/tax not found and was not bought!')
                elif ratio_sus:
                    if verbose:
                        self.write(Fore.RED + f'{ca_name} had a sus MC/LP ratio and was not bought!')
                elif lplock_v == False and self.lp_lock:
                    if verbose:
                        self.write(Fore.RED + f'{ca_name} had no LP Lock and was not bought!')
                elif mcap_v <= self.minimum_market_cap:
                    if verbose:
                        self.write(
                            Fore.RED + f'{ca_name} had a market cap lower than ${self.minimum_market_cap} and was not bought!')
                elif lp_v <= self.minimum_liquidity:
                    if verbose:
                        self.write(
                            Fore.RED + f'{ca_name} had an LP lower than ${self.minimum_liquidity} and was not bought!')
                else:
                    if verbose:
                        self.write(Fore.RED + 'Not enough info to decide to buy token.')

    # Send orders to PancakeSwap
    def place_order(self, contract, action):
        try:
            txn = None
            contract = self.Web3.toChecksumAddress(contract)
            nonce = self.Web3.eth.get_transaction_count(self.wallet_address)
            if action == 'buy':
                txn = self.pcs_contract.functions.swapExactETHForTokens(
                    0,
                    [self.spend, contract],
                    self.wallet_address,
                    (int(time.time()) + 10000)
                ).buildTransaction({
                    'from': self.wallet_address,
                    'value': self.Web3.toWei(self.buy_amount, 'ether'),
                    'gasPrice': self.Web3.toWei(self.txn_speed, 'gwei'),
                    'nonce': nonce,
                })
            elif action == 'sell':
                txn = self.pcs_contract.functions.swapExactETHForTokens(
                    0,
                    [contract, self.spend],
                    self.wallet_address,
                    (int(time.time()) + 10000)
                ).buildTransaction({
                    'from': self.wallet_address,
                    'value': self.Web3.toWei(self.buy_amount, 'ether'),
                    'gasPrice': self.Web3.toWei(self.txn_speed, 'gwei'),
                    'nonce': nonce,
                })
            signed_txn = self.Web3.eth.account.signTransaction(txn, private_key=self.private_key)
            self.Web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            receipt = self.Web3.eth.waitForTransactionReceipt(signed_txn.hash)
            if receipt['status'] == 0:
                self.write(Fore.RED + 'Transaction failed!')
            else:
                self.write(Fore.GREEN + 'Transaction successful!')
        except ValueError:
            self.write(
                Fore.RED + 'Transaction initializing FAILED! This probably means the token has a too low liquidity and the price impact is too high for buying/selling.')

    # Main thread
    def run(self):
        ############################################################################################################
        # Hi! Thank you for reading this code. If you have any questions, please DM me on TG. https://t.me/yosharu #
        ############################################################################################################
        if self.buy_mode and self.fake_mode:
            self.write(
                Fore.RED + 'Both real and fake buying is enabled. Simultaneous betting is currently not supported and will cause problems. quitting...')
            quit()

        if self.buy_mode and (self.wallet_address != '' and self.private_key != ''):
            self.fake_balance = 100000000000000000000
            self.real_balance = self.get_balance()
            balance_overview = self.real_balance
        elif self.fake_mode:
            balance_overview = self.fake_balance
        elif self.wallet_address == '' or self.private_key == '':
            self.write(Fore.RED + 'You have buy mode enabled, but no wallet/private key could be found. Quitting...')
            quit()

        if self.txn_speed == 'standard':
            self.txn_speed = 5
        elif self.txn_speed == 'fast':
            self.txn_speed = 6
        elif self.txn_speed == 'instant':
            self.txn_speed = 7

        ## LOGO SEQUENCE AND DISCLAIMER
        print("\n\n")
        cprint(figlet_format(f'Sniper-O-Mancer', font='cosmic', width=150, justify="left"),
               'yellow')
        print(Fore.CYAN + f'\n                                                       {self.version}')
        print(Fore.YELLOW + "                                                     Coded by yosharu")
        print(
            Fore.RED + "                                    THIS SNIPER WAS MADE TO BE USED UNDER CLOSE SUPERVISION! \n                    ANYONE INVOLVED IN THE DEVELOPMENT OF SoM ARE NOT LIABLE FOR ANY LOSSES OCCURED UNDER USE!\n                                      BY USING THIS SNIPER, YOU AGREE TO THESE TERMS.\n")
        try:
            rpc_response_time = requests.post(self.RPC).elapsed.total_seconds()
            rpc_response_time = round(rpc_response_time, 3)
            self.write(Fore.YELLOW + f'RPC: {self.RPC} {Fore.WHITE}({rpc_response_time}ms)')
        except requests.exceptions.HTTPError:
            self.write(Fore.RED + f'RPC ({self.RPC}) 502 error, remove from list if it keeps happening...')
            quit()
        self.write(Fore.YELLOW + f'ADDRESS: {Fore.WHITE}{self.wallet_address}')
        self.write(Fore.YELLOW + f'WALLET BALANCE: {Fore.WHITE}{self.real_balance} BNB')

        ##MAIN THREAD
        try:
            # print(Fore.CYAN + '\nStarting threads...')
            t1 = threading.Thread(target=self.scrape_newest_ca, daemon=True)
            t2 = threading.Thread(target=self.updater, args=('price',), daemon=True)
            t3 = threading.Thread(target=self.updater, args=('honeypot',), daemon=True)
            t4 = threading.Thread(target=self.updater, args=('lplock',), daemon=True)
            t1.start()
            t2.start()
            t3.start()
            t4.start()
            self.write(Fore.CYAN + 'Threads started')
            time.sleep(5)
            while True:
                if self.inoperation is False:
                    n_uptime = self.get_uptime()
                    if self.buy_mode:
                        self.real_balance = self.get_balance()
                        balance_overview = round(self.real_balance, 6)
                    elif self.fake_mode:
                        balance_overview = round(self.fake_balance, 6)
                    else:
                        balance_overview = 'N/A'

                    try:
                        average_x = statistics.mean(self.x_list)
                    except statistics.StatisticsError:
                        average_x = 'N/A'

                    print(
                        f'\n{Fore.CYAN}-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n{Fore.YELLOW}Overview:\nBalance: {Fore.WHITE}{balance_overview} BNB\n{Fore.YELLOW}Average Xs:{Fore.WHITE} {average_x}\n\n{Fore.YELLOW}Database:{Fore.WHITE}\n{self.database}\n\n{Fore.YELLOW}Currently holding:\n{Fore.WHITE}{self.fake_buy_current_list}\n\n{Fore.YELLOW}System:{Fore.WHITE}\n{Fore.YELLOW}Uptime: {Fore.WHITE}{n_uptime}\n{Fore.YELLOW}Version: {Fore.WHITE}{self.version}\n{Fore.CYAN}-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
                    if len(self.database.index) >= self.maximum_database_index:
                        self.write(Fore.RED + 'Purging inactive tokens...')
                        self.reset_done = True
                        self.database = self.database[self.database['Xs'].notna()]
                        self.database = self.database[self.database['Finished'] == False]
                        self.database = self.database.reset_index().drop(columns=['index'])
                        time.sleep(5)
                        self.reset_done = False
                    time.sleep(self.overview_sleep_time)
                else:
                    time.sleep(2)
        except (KeyboardInterrupt, Exception) as e:
            if e == '':
                self.write(Fore.RED + f'FATAL ERROR: {Fore.WHITE} {e}')
            else:
                self.write(Fore.RED + 'Quit key detected! Closing...')
            self.write(Fore.RED + 'Exiting Chrome windows...')

            # Simply .quit() didn't work on my system, so here i'm manually killing the Chrome windows with PIDs and task kill
            for process in psutil.process_iter():
                if process.name() == 'chrome.exe' and '--test-type=webdriver' in process.cmdline():
                    with suppress(psutil.NoSuchProcess):
                        self.kill_list.append(process.pid)
            for proc_id in self.kill_list:
                os.kill(int(proc_id), signal.SIGTERM)
            self.write(Fore.RED + 'Goodbye.')
            quit()


SniperOMancer().run()
