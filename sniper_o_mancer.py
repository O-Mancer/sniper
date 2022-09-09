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
#
# TIP JAR:
# BSC & ETH: 0x930A400a816D702f4b81B143863859154d7ea209
#
import datetime
import json
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
from som_config import *

init(autoreset=True, strip=not sys.stdout.isatty())  # strip colors if stdout is redirected


class SniperOMancer:
    # Init
    def __init__(self):
        self.write(Fore.BLUE + 'Initializing...')
        self.version = 'v0.2 Alpha'

        # INIT
        self.numTokensBought = 0
        if manual_rpc is False:
            self.RPC, self.response_time = self.find_closest_rpc()
        else:
            self.RPC = manual_rpc
            self.response_time = round(requests.get(self.RPC).elapsed.total_seconds(), 3)
        self.Web3 = Web3(Web3.HTTPProvider(self.RPC))

        listeningABI = json.loads(
            '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
        pancakeSwapFactoryAddress = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'  # read from JSON later
        # noinspection PyTypeChecker
        self.listening_contract = self.Web3.eth.contract(address=pancakeSwapFactoryAddress, abi=listeningABI)
        # noinspection PyTypeChecker
        self.pcs_contract = self.Web3.eth.contract(address='0x10ED43C718714eb63d5aA57B78B54704E256024E',
                                                   abi='[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]')
        self.spend = self.Web3.toChecksumAddress("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c")  # wbnb contract address
        self.tokenNameABI = json.loads(
            '[ { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "owner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "spender", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "value", "type": "uint256" } ], "name": "Approval", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "from", "type": "address" }, { "indexed": true, "internalType": "address", "name": "to", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "value", "type": "uint256" } ], "name": "Transfer", "type": "event" }, { "constant": true, "inputs": [ { "internalType": "address", "name": "_owner", "type": "address" }, { "internalType": "address", "name": "spender", "type": "address" } ], "name": "allowance", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "address", "name": "spender", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "approve", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [ { "internalType": "address", "name": "account", "type": "address" } ], "name": "balanceOf", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "decimals", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "getOwner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "name", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "symbol", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "totalSupply", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "address", "name": "recipient", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "transfer", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "address", "name": "sender", "type": "address" }, { "internalType": "address", "name": "recipient", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "transferFrom", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" } ]')

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
        self.honeypot_updater_driver = webdriver.Chrome(options=self.op)
        self.price_updater_driver = webdriver.Chrome(options=self.op)
        self.kill_list = []
        self.inoperation = None
        self.honeypot_url = 'https://honeypot.is/?address='
        self.rugdoc_url = 'https://honeypot.api.rugdoc.io/api/honeypotStatus.js?address='
        self.poocoin_url = 'https://poocoin.app/tokens/'
        self.database = pd.DataFrame(
            columns=['Timestamp', 'Name', 'Contract', 'Price', 'Market Cap', 'Liquidity', 'Buy Tax', 'Sell Tax',
                     'MiniAudit', 'Honeypot.is', 'RugDoc', 'Excluded', 'Xs', 'Finished'])
        self.internal_database = pd.DataFrame(columns=['Name', 'Contract', 'Entry', 'Current'])
        self.fake_buy_current_list = []
        self.exclude_list = []
        self.x_list = []
        self.reset_done = False
        self.startTime = time.time()

    # grab the wallet balance
    def get_balance(self):
        mybalance = self.Web3.eth.getBalance(wallet_address)
        return self.Web3.fromWei(mybalance, 'ether')

    # simple percentage func to help
    def percentage(self, percent, whole):
        return (percent * whole) / 100.0

    # Find the lowest latency RPC for the fastest transactions possible.
    def find_closest_rpc(self):
        self.write(Fore.YELLOW + 'Optimizing RPC...')
        rpc_response_time_list = []
        for i in rpc_lists:
            rpc_response_time = requests.post(i).elapsed.total_seconds()
            rpc_response_time_list.append(rpc_response_time)
        best_rpc = min(rpc_response_time_list)
        best_rpc = rpc_response_time_list.index(best_rpc)
        response_time = round(rpc_response_time_list[best_rpc], 3)
        best_rpc = rpc_lists[best_rpc]
        if manual_rpc is False:
            # Read in the file
            with open('som_config.py', 'r') as file:
                filedata = file.read()
            # Replace the target string
            filedata = filedata.replace('manual_rpc = False', f"manual_rpc = '{best_rpc}'")
            # Write the file out again
            with open('som_config.py', 'w') as file:
                file.write(filedata)
            self.write(Fore.YELLOW + 'Saved the RPC to the config!')
        return best_rpc, response_time

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

    # Scraper which refreshes the PCS Factory contract for new contracts to snipe.
    def scrape_newest_ca(self):
        while True:
            try:
                if self.reset_done:
                    time.sleep(1)
                else:
                    self.inoperation = True
                    # print(Fore.YELLOW + '\nScraping newest jewarch CA...')
                    latest_ca = None
                    contract = self.listening_contract
                    try:
                        event_filter = contract.events.PairCreated.createFilter(fromBlock='latest').get_new_entries()
                    except requests.exceptions.HTTPError:
                        event_filter = None

                    if event_filter is not None:
                        for PairCreated in event_filter:
                            jsonEventContents = json.loads(Web3.toJSON(PairCreated))
                            if ((jsonEventContents['args'][
                                     'token0'] == "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c") or (
                                    jsonEventContents['args'][
                                        'token1'] == "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c")):
                                if (jsonEventContents['args'][
                                        'token0'] == "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"):
                                    latest_ca = jsonEventContents['args']['token1']
                                else:
                                    latest_ca = jsonEventContents['args']['token0']
                            # print(latest_ca)
                            # print(Fore.YELLOW + 'New CA detected, getting info...')
                            #########################################
                            # Grab price, liq and mcap from poocoin #
                            #########################################

                            self.newest_ca_driver.get(f'{self.poocoin_url}{latest_ca}')
                            try:
                                latest_ca_name = WebDriverWait(self.newest_ca_driver, max_scraper_wait).until(
                                    EC.visibility_of_element_located((
                                        By.XPATH,
                                        "/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/h1"))).text
                                latest_ca_name = latest_ca_name.split(' (', 1)[0]
                            except selenium.common.exceptions.TimeoutException:
                                self.newest_ca_driver.get(f'{self.poocoin_url}{latest_ca}')
                                latest_ca_name = self.newest_ca_driver.title
                                latest_ca_name = latest_ca_name.split(' price', 1)[0]

                            try:
                                latest_ca_price = WebDriverWait(self.newest_ca_driver, max_scraper_wait).until(
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
                                latest_ca_mcap = WebDriverWait(self.newest_ca_driver, max_scraper_wait).until(
                                    EC.visibility_of_element_located((By.XPATH,
                                                                      "/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]")))
                                try:
                                    latest_ca_mcap = int(latest_ca_mcap.text.replace('$', '').replace(',', ''))
                                except ValueError:
                                    self.write(
                                        Fore.YELLOW + f'{latest_ca_name} has an unstable market cap, skipping...')
                                    latest_ca_mcap = 'N/A'

                            except selenium.common.exceptions.TimeoutException:
                                latest_ca_mcap = 'N/A'

                            if latest_ca_mcap != 'N/A' and latest_ca_mcap > 9999999:
                                latest_ca_mcap = 'N/A'

                            try:
                                latest_ca_liquidity = WebDriverWait(self.newest_ca_driver, max_scraper_wait).until(
                                    EC.visibility_of_element_located((By.XPATH,
                                                                      "/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div/div/span")))
                                try:
                                    latest_ca_liquidity = int(
                                        latest_ca_liquidity.text.replace('$', '').replace(',', '').replace('(',
                                                                                                           '').replace(
                                            ')', ''))
                                except ValueError:
                                    self.write(Fore.YELLOW + f'{latest_ca_name} has an unstable LP, skipping...')
                                    latest_ca_liquidity = 'N/A'

                            except selenium.common.exceptions.TimeoutException:
                                latest_ca_liquidity = 'N/A'

                            #############
                            # MiniAudit #
                            #############
                            if enableMiniAudit is True:
                                latest_ca_miniaudit = self.miniAudit(latest_ca)
                            else:
                                latest_ca_miniaudit = None

                            ####################################
                            # Honeypot and Tax via Honeypot.is #
                            ####################################
                            try:
                                honeypot_url_ca = f'{self.honeypot_url}{latest_ca}'
                                self.newest_ca_driver.get(honeypot_url_ca)

                                honeypot_ornot = WebDriverWait(self.newest_ca_driver,
                                                               max_scraper_wait).until(
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
                                                        max_scraper_wait).until(
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
                                                            max_scraper_wait).until(
                                            EC.visibility_of_element_located((By.XPATH,
                                                                              "/html/body/div[2]/div[1]/div/p[5]")))

                                        latest_ca_buy_tax = tax.text.split('%', 1)[0]
                                        latest_ca_sell_tax = tax.text.split('%', 1)[1]

                                        latest_ca_buy_tax = float(
                                            latest_ca_buy_tax.replace('Buy Tax: ', '').replace('%', '').replace('\n',
                                                                                                                ''))
                                        latest_ca_sell_tax = float(
                                            latest_ca_sell_tax.replace('Sell Tax: ', '').replace('%', '').replace('\n',
                                                                                                                  ''))
                                    except (IndexError, selenium.common.exceptions.TimeoutException):
                                        tax = WebDriverWait(self.newest_ca_driver,
                                                            max_scraper_wait).until(
                                            EC.visibility_of_element_located((By.XPATH,
                                                                              "/html/body/div[2]/div[1]/div/p[9]")))

                                        latest_ca_buy_tax = tax.text.split('%', 1)[0]
                                        latest_ca_sell_tax = tax.text.split('%', 1)[1]

                                        latest_ca_buy_tax = float(
                                            latest_ca_buy_tax.replace('Buy Tax: ', '').replace('%', '').replace('\n',
                                                                                                                ''))
                                        latest_ca_sell_tax = float(
                                            latest_ca_sell_tax.replace('Sell Tax: ', '').replace('%', '').replace('\n',
                                                                                                                  ''))

                            except selenium.common.exceptions.TimeoutException:
                                latest_ca_buy_tax, latest_ca_sell_tax = 'N/A', 'N/A'

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

                            if latest_ca in self.exclude_list:
                                excluded = True
                                # self.write(Fore.RED + f'Added {latest_ca_name} to exclusion list.')
                            else:
                                excluded = False

                            if latest_ca_buy_tax != 'N/A' and latest_ca_sell_tax != 'N/A':
                                latest_ca_buy_tax, latest_ca_sell_tax = round(latest_ca_buy_tax, 1), round(
                                    latest_ca_sell_tax, 1)

                            if latest_ca_price != 'N/A':
                                latest_ca_price_forprint = f'{latest_ca_price:.20f}'
                            else:
                                latest_ca_price_forprint = 'N/A'

                            timestamp = time.time()

                            if latest_ca_name != 'PooCoin BSC Charts' and excluded is False:
                                self.database.loc[len(self.database.index)] = [timestamp, latest_ca_name, latest_ca,
                                                                               latest_ca_price,
                                                                               latest_ca_mcap, latest_ca_liquidity,
                                                                               latest_ca_buy_tax,
                                                                               latest_ca_sell_tax, latest_ca_miniaudit,
                                                                               latest_ca_honeypot,
                                                                               latest_ca_rugdoc,
                                                                               excluded, None, False]

                                print(
                                    Fore.CYAN + f'\n----------------------------------------------\n{Fore.BLUE}NEW TOKEN\n{Fore.GREEN}Name: {Fore.WHITE}{latest_ca_name} \n{Fore.GREEN}CA: {Fore.WHITE}{latest_ca} \n{Fore.GREEN}Price: {Fore.WHITE}{latest_ca_price_forprint} \n{Fore.GREEN}Market Cap: {Fore.WHITE}{latest_ca_mcap}\n{Fore.GREEN}LP: {Fore.WHITE}{latest_ca_liquidity} \n{Fore.GREEN}Buy Tax: {Fore.WHITE}{latest_ca_buy_tax} \n{Fore.GREEN}Sell Tax: {Fore.WHITE}{latest_ca_sell_tax} \n{Fore.GREEN}MiniAudit: {Fore.WHITE}{latest_ca_miniaudit} \n{Fore.GREEN}Honeypot.is: {Fore.WHITE}{latest_ca_honeypot} \n{Fore.GREEN}RugDoc: {Fore.WHITE}{latest_ca_rugdoc}\n{Fore.CYAN}----------------------------------------------\n')
                                self.write(Fore.YELLOW + f'Added {latest_ca_name} to database...')

                                t6 = threading.Thread(target=self.tx_handler,
                                                      args=(latest_ca_name, latest_ca, latest_ca_price, None, True,),
                                                      daemon=True)
                                t6.start()
                                self.inoperation = False
                                # print(Fore.YELLOW + f'\nSleeping for {scraper_sleep_time} seconds...')
            except ValueError as e:
                self.write(e)
                pass

    # Mini audit // credit jontstaz
    def miniAudit(self, tokenAddress):
        try:
            pancakeSwapRouterAddress = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
            if (
                    enableMiniAudit == True):  # enable mini audit feature: quickly scans token for potential features that make it a scam / honeypot / rugpull etc
                # self.write(Fore.YELLOW + "[MiniAudit] Starting Mini Audit...")
                contractCodeGetRequestURL = "https://api.bscscan.com/api?module=contract&action=getsourcecode&address=" + str(tokenAddress) + "&apikey=" + str(bscScanAPIKey)
                contractCodeRequest = requests.get(url=contractCodeGetRequestURL)
                tokenContractCode = contractCodeRequest.json()

                if (str(tokenContractCode['result'][0][
                            'ABI']) == "Contract source code not verified") and checkSourceCode is True:  # check if source code is verified
                    # self.write(Fore.RED + "[MiniAudit] Contract source code isn't verified.")
                    return 'Bad'

                elif ("0x05fF2B0DB69458A0750badebc4f9e13aDd608C7F" in str(tokenContractCode['result'][0][
                                                                              'SourceCode'])) and checkPancakeV1Router is True:  # check if pancakeswap v1 router is used
                    # self.write(Fore.RED + "[MiniAudit] Contract uses PancakeSwap v1 router.")
                    return 'Bad'


                elif (str(pancakeSwapRouterAddress) not in str(tokenContractCode['result'][0][
                                                                   'SourceCode'])) and checkValidPancakeV2 is True:  # check if pancakeswap v2 router is used
                    # self.write(Fore.RED + "[MiniAudit] Contract doesn't use valid PancakeSwap v2 router.")
                    return 'Bad'

                elif "mint" in str(tokenContractCode['result'][0][
                                       'SourceCode']) and checkMintFunction is True:  # check if any mint function enabled
                    # self.write(Fore.RED + "[MiniAudit] Contract has mint function enabled.")
                    return 'Bad'


                elif (
                        "function transferFrom(address sender, address recipient, uint256 amount) public override returns (bool)" in str(
                    tokenContractCode['result'][0][
                        'SourceCode']) or "function _approve(address owner, address spender, uint256 amount) internal" in str(
                    tokenContractCode['result'][0]['SourceCode']) or "newun" in str(tokenContractCode['result'][0][
                                                                                        'SourceCode'])) and checkHoneypot is True:  # check if token is honeypot
                    # self.write(Fore.RED + "[MiniAudit] Contract is a honeypot.")
                    return 'Bad'

                else:
                    # self.write(Fore.GREEN + "[MiniAudit] Token has passed mini audit.")  # now you can buy
                    return 'Good'
        except TypeError:
            return 'N/A'

    # Updates database
    def updater(self, info):
        while True:
            if len(self.database.index) > 0:
                if info == 'price':
                    #######################################
                    # Price, Mcap and liq from blockchain #
                    #######################################
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
                                    seconds = maximum_minutes_in_database * 60
                                    if time.time() - ca_timestamp >= seconds:
                                        self.database['Finished'][i] = True
                                    if current_contract not in self.exclude_list and self.database['Finished'][
                                        i] == False:
                                        try:
                                            self.price_updater_driver.get(price_update_link)
                                            ca_price = WebDriverWait(self.price_updater_driver,
                                                                     max_scraper_wait).until(
                                                EC.visibility_of_element_located((
                                                    By.XPATH,
                                                    "/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/span")))

                                            try:
                                                ca_price = float(ca_price.text.replace('$', ''))
                                            except ValueError:
                                                ca_price = 'N/A'

                                            ca_mcap = WebDriverWait(self.price_updater_driver,
                                                                    max_scraper_wait).until(
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
                                                                             max_scraper_wait).until(
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
                                        time.sleep(updater_sleep_time)
                        except KeyError:
                            time.sleep(updater_sleep_time)

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
                                seconds = maximum_minutes_in_database * 60
                                if time.time() - ca_timestamp >= seconds:
                                    self.database['Finished'][i] = True
                                if self.database['Finished'][i] == False:
                                    try:
                                        honeypot_url_ca = f'{self.honeypot_url}{current_contract}'
                                        self.honeypot_updater_driver.get(honeypot_url_ca)

                                        honeypot_ornot = WebDriverWait(self.honeypot_updater_driver,
                                                                       max_scraper_wait).until(
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
                                                                max_scraper_wait).until(
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
                                                                    max_scraper_wait).until(
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
                                                                    max_scraper_wait).until(
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

                            self.database.to_csv('sniper_o_mancer.csv', encoding='utf-8')
                            time.sleep(updater_sleep_time)
                        except KeyError:
                            time.sleep(updater_sleep_time)

    # Monitors and sells bought tokens
    def token_watcher(self, ca, ca_name):
        global fake_balance
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
                    sell_tax_takeprofitx = self.percentage(sell_tax, takeprofit_x)
                    sell_tax_stoplossx = self.percentage(sell_tax, stoploss_x)
                    takeprofit = takeprofit_x + sell_tax_takeprofitx
                    stoploss = stoploss_x + sell_tax_stoplossx

                    if current_bought_price > float(
                            self.internal_database['Entry'][internal_ca_index]) * takeprofit:
                        profit_from_buy = fake_buy * takeprofit_x
                        profit_from_buy = profit_from_buy - self.percentage(sell_tax, profit_from_buy)
                        fake_balance = fake_balance + (profit_from_buy - transaction_fee)
                        try:
                            self.fake_buy_current_list.remove(remove_ca_name)
                        except ValueError:
                            pass

                        if fake_mode:
                            self.write(
                                Fore.GREEN + f'{ca_name} fake sold at a {takeprofit_x}x profit! Balance: {fake_balance} BNB')

                        if buy_mode:
                            real_balance = self.get_balance()
                            self.write(
                                Fore.GREEN + f'Selling {ca_name} at a {takeprofit_x}x profit! Balance: {real_balance} BNB')
                            self.place_order(ca, 'sell')

                        self.database['Finished'][real_ca_database_index] = True
                        self.x_list.append(self.database['Xs'][real_ca_database_index])
                        break
                    elif current_bought_price < float(
                            self.internal_database['Entry'][internal_ca_index]) / stoploss:
                        profit_from_buy = fake_buy / stoploss_x
                        fake_balance = fake_balance - (profit_from_buy + transaction_fee)
                        try:
                            self.fake_buy_current_list.remove(remove_ca_name)
                        except ValueError:
                            pass

                        if fake_mode:
                            self.write(
                                Fore.RED + f'{ca_name} fake sold at a {stoploss_x}x loss! Balance: {fake_balance} BNB')

                        if buy_mode:
                            self.write(Fore.RED + f'Selling {ca_name} at a {takeprofit_x}x profit!')
                            self.place_order(ca, 'sell')

                        self.database['Finished'][real_ca_database_index] = True
                        self.x_list.append(self.database['Xs'][real_ca_database_index])
                        break
                    else:
                        time.sleep(token_watcher_sleep)
                elif self.database['Finished'][real_ca_database_index] == True:
                    real_ca_database_index = self.database.index[self.database['Contract'] == ca].tolist()[0]
                    internal_ca_index = self.internal_database.index[self.internal_database['Contract'] == ca].tolist()[
                        0]
                    remove_ca_name = self.internal_database['Name'][internal_ca_index]
                    token_x = float(self.database['Xs'][real_ca_database_index])
                    profit = fake_buy * token_x
                    fake_balance = fake_balance + profit
                    if profit > fake_buy:
                        try:
                            self.fake_buy_current_list.remove(remove_ca_name)
                        except ValueError:
                            pass

                        if fake_mode:
                            self.write(
                                Fore.GREEN + f'{ca_name} fake sold at a {token_x}x profit because of inactivity!')

                        if buy_mode:
                            self.write(Fore.GREEN + f'{ca_name} sold at a {token_x}x profit because of inactivity!')
                            self.place_order(ca, 'sell')
                    elif profit < fake_buy:
                        if fake_mode:
                            self.write(Fore.RED + f'{ca_name} fake sold at a {token_x}x loss because of inactivity!')

                        if buy_mode:
                            self.write(Fore.RED + f'{ca_name} sold at a {token_x}x profit because of inactivity!')
                            self.place_order(ca, 'sell')
                    self.x_list.append(self.database['Xs'][real_ca_database_index])
                    break
                else:
                    internal_ca_index = \
                        self.internal_database.index[self.internal_database['Contract'] == ca].tolist()[0]
                    remove_ca_name = self.internal_database['Name'][internal_ca_index]
                    if fake_mode:
                        self.write(
                            Fore.RED + f'Money in {ca_name} fake lost! This is either due to the token becoming a honeypot or the taxes skyrocket. Money is assumed lost.')

                    if buy_mode:
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
        global fake_balance
        if (fake_mode and fake_balance >= fake_buy) or (
                buy_mode and self.real_balance >= buy_amount):
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

                ca_x = self.database['Xs'][ca_index]

                if analyze_mc_liq_ratio and (mcap_v != -1 or lp_v != -1):
                    try:
                        if 0.6 < mcap_v / lp_v < 1.4:
                            ratio_sus = True
                        else:
                            ratio_sus = False
                    except ZeroDivisionError:
                        ratio_sus = False
                else:
                    ratio_sus = False

                if enableMiniAudit is True:
                    miniaudit_v = self.database['MiniAudit'][ca_index]
                else:
                    miniaudit_v = 'Good'

                if miniaudit_v == 'Good' and buy_tax <= maximum_buy_tax and sell_tax <= maximum_sell_tax and honeypot_v == 'False' and buy_tax != 'N/A' and sell_tax != 'N/A' and rugdoc_v == 'Clean' and mcap_v >= minimum_market_cap and lp_v >= minimum_liquidity and ratio_sus is False and ca_x == None:
                    try:
                        buy_tax = float(self.database['Buy Tax'][ca_index])
                    except ValueError:
                        buy_tax = 0

                    self.internal_database.loc[len(self.internal_database.index)] = [ca_name, ca, entry_price, None]
                    self.fake_buy_current_list.append(ca_name)
                    fake_balance = fake_balance - (fake_buy + transaction_fee)
                    actual_fake_buy = fake_buy - self.percentage(buy_tax, fake_buy)

                    if fake_mode:
                        self.write(
                            Fore.BLUE + f'Fake bought {ca_name} for {fake_buy} BNB (with tax: {actual_fake_buy} BNB), watching token for sell point...')

                    if buy_mode:
                        self.write(Fore.BLUE + f'Buying {ca_name} for {buy_amount} BNB @ {price_v}...')
                        self.place_order(ca, 'buy')

                    t4 = threading.Thread(target=self.token_watcher, args=(ca, ca_name,), daemon=True)
                    t4.start()

                    if telegram_enabled:
                        poocoin_link = f'[💩](https://poocoin.app/tokens/{ca})'
                        dexscreener_link = f'[🤖](https://dexscreener.com/bsc/{ca})'
                        moonarch_link = f'[🌙](https://moonarch.app/token/{ca})'
                        tgmessage = f'*NEWLY LAUNCHED SHITCOIN DETECTED:* %0A *Name*: {ca_name} %0A *CA*: {ca} %0A *Price*: {price_v} %0A *Market Cap*: {mcap_v} %0A *LP*: {lp_v} %0A *Buy Tax*: {buy_tax} %0A *Sell Tax*: {sell_tax} %0A *MiniAudit*: {miniaudit_v} %0A *Honeypot.is*: {honeypot_v} %0A *RugDoc*: {rugdoc_v} %0A {poocoin_link} %0A {dexscreener_link} %0A {moonarch_link} %0A%0A _If i posted the CA, this means it passed Honeypot.is, Rugcheck and RugDoc. It does NOT guarantee future results._ %0A_Not financial advice, DYOR!_'
                        requests.post(
                            f'https://api.telegram.org/bot{telegram_bot_key}/sendMessage?chat_id={telegram_bot_chat_id}&text={tgmessage}&parse_mode=Markdown')
                        self.write(Fore.CYAN + 'Telegram message sent')
                elif honeypot_v == 'True':
                    if verbose:
                        self.write(Fore.RED + f'{ca_name} is a honeypot and was not bought!')
                elif rugdoc_v == 'Dirty':
                    if verbose:
                        self.write(Fore.RED + f'{ca_name} was dirty and was not bought!')
                elif buy_tax >= maximum_buy_tax and sell_tax >= maximum_sell_tax:
                    if verbose:
                        self.write(Fore.RED + f'{ca_name} had too high tax/tax not found and was not bought!')
                elif ratio_sus:
                    if verbose:
                        self.write(Fore.RED + f'{ca_name} had a sus MC/LP ratio and was not bought!')
                elif mcap_v <= minimum_market_cap:
                    if verbose:
                        self.write(
                            Fore.RED + f'{ca_name} had a market cap lower than ${minimum_market_cap} and was not bought!')
                elif lp_v <= minimum_liquidity:
                    if verbose:
                        self.write(
                            Fore.RED + f'{ca_name} had an LP lower than ${minimum_liquidity} and was not bought!')
                else:
                    if verbose:
                        self.write(Fore.RED + 'Not enough info to decide to buy token.')

    # Send orders to PancakeSwap
    def place_order(self, contract, action):
        try:
            txn = None
            contract = self.Web3.toChecksumAddress(contract)
            nonce = self.Web3.eth.get_transaction_count(wallet_address)
            if action == 'buy':
                txn = self.pcs_contract.functions.swapExactETHForTokens(
                    0,
                    [self.spend, contract],
                    wallet_address,
                    (int(time.time()) + 10000)
                ).buildTransaction({
                    'from': wallet_address,
                    'value': self.Web3.toWei(buy_amount, 'ether'),
                    'gasPrice': self.Web3.toWei(txn_speed, 'gwei'),
                    'nonce': nonce,
                })
            elif action == 'sell':
                txn = self.pcs_contract.functions.swapExactETHForTokens(
                    0,
                    [contract, self.spend],
                    wallet_address,
                    (int(time.time()) + 10000)
                ).buildTransaction({
                    'from': wallet_address,
                    'value': self.Web3.toWei(buy_amount, 'ether'),
                    'gasPrice': self.Web3.toWei(txn_speed, 'gwei'),
                    'nonce': nonce,
                })
            signed_txn = self.Web3.eth.account.signTransaction(txn, private_key=private_key)
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
        global fake_balance
        global txn_speed
        #########################################################################################################################
        # Hi! Thank you for reading this code. If you have any questions, please feel free to DM me on TG. https://t.me/yosharu #
        #########################################################################################################################
        if buy_mode and fake_mode:
            self.write(
                Fore.RED + 'Both real and fake buying is enabled. Simultaneous betting is currently not supported and will cause problems. quitting...')
            quit()

        if buy_mode and wallet_address != '' and private_key != '':
            fake_balance = 100000000000000000000
            self.real_balance = self.get_balance()
            balance_overview = self.real_balance
        elif fake_mode:
            balance_overview = fake_balance
        elif wallet_address == '' or private_key == '':
            self.write(Fore.RED + 'You have buy mode enabled, but no wallet/private key could be found. Quitting...')
            quit()
        else:
            self.real_balance = 'N/A'

        if txn_speed == 'standard':
            txn_speed = 5
        elif txn_speed == 'fast':
            txn_speed = 6
        elif txn_speed == 'instant':
            txn_speed = 7

        ## LOGO SEQUENCE AND DISCLAIMER
        print("\n\n")
        cprint(figlet_format(f'Sniper-O-Mancer', font='cosmic', width=150, justify="left"),
               'yellow')
        print(Fore.CYAN + f'\n                                                       {self.version}')
        print(Fore.YELLOW + "                                                     Coded by yosharu")
        print(
            Fore.RED + "                                    THIS SNIPER WAS MADE TO BE USED UNDER CLOSE SUPERVISION! \n                    ANYONE INVOLVED IN THE DEVELOPMENT OF SoM ARE NOT LIABLE FOR ANY LOSSES OCCURED UNDER USE!\n                                      BY USING THIS SNIPER, YOU AGREE TO THESE TERMS.\n")
        try:
            self.write(Fore.YELLOW + f'RPC: {self.RPC} {Fore.WHITE}({self.response_time}ms)')
        except requests.exceptions.HTTPError:
            self.write(Fore.RED + f'RPC ({self.RPC}) 502 error, remove from list if it keeps happening...')
            quit()
        if buy_mode:
            self.write(Fore.YELLOW + f'ADDRESS: {Fore.WHITE}{wallet_address}')
            self.write(Fore.YELLOW + f'WALLET BALANCE: {Fore.WHITE}{self.real_balance} BNB')

        ##MAIN THREAD
        try:
            # print(Fore.CYAN + '\nStarting threads...')
            t1 = threading.Thread(target=self.scrape_newest_ca, daemon=True)
            t2 = threading.Thread(target=self.updater, args=('price',), daemon=True)
            t3 = threading.Thread(target=self.updater, args=('honeypot',), daemon=True)
            t1.start()
            t2.start()
            t3.start()
            self.write(Fore.CYAN + 'Threads successfully started!')
            self.write(Fore.CYAN + 'Only new tokens that fit your config will appear in this window.')
            time.sleep(5)
            while True:
                n_uptime = self.get_uptime()
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if buy_mode:
                    self.real_balance = self.get_balance()
                    balance_overview = round(self.real_balance, 6)
                elif fake_mode:
                    balance_overview = round(fake_balance, 6)
                else:
                    balance_overview = 'N/A'

                try:
                    average_x = statistics.mean(self.x_list)
                except statistics.StatisticsError:
                    average_x = 'N/A'

                if len(self.database.index) > 0:
                    print(
                        f'\n{Fore.CYAN}-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n{Fore.YELLOW}Overview:\nBalance: {Fore.WHITE}{balance_overview} BNB\n{Fore.YELLOW}Average Xs:{Fore.WHITE} {average_x}\n\n{Fore.YELLOW}Database:{Fore.WHITE}\n{self.database}\n\n{Fore.YELLOW}Currently holding:\n{Fore.WHITE}{self.fake_buy_current_list}\n\n{Fore.YELLOW}System:{Fore.WHITE}\n{Fore.YELLOW}Time: {Fore.WHITE}{current_time}\n{Fore.YELLOW}Uptime: {Fore.WHITE}{n_uptime}\n{Fore.YELLOW}Version: {Fore.WHITE}{self.version}\n{Fore.CYAN}-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
                if len(self.database.index) >= maximum_database_index:
                    try:
                        self.write(Fore.RED + 'Purging inactive tokens...')
                        self.reset_done = True
                        self.database = self.database[self.database['Xs'].notna()]
                        self.database = self.database[self.database['Finished'] == False]
                        self.database = self.database.reset_index().drop(columns=['index'])
                        time.sleep(5)
                        self.reset_done = False
                    except Exception as e:
                        print(e)
                time.sleep(overview_sleep_time)
        except (KeyboardInterrupt, Exception) as e:
            if e == '':
                self.write(Fore.RED + f'FATAL ERROR: {Fore.WHITE} {e}')
            else:
                self.write(Fore.RED + 'Closing...')
            self.write(Fore.RED + '[1] Chrome hosts...')

            # Simply .quit() didn't work on my system, so here I'm manually killing the Chrome windows with PIDs and task kill
            for process in psutil.process_iter():
                if process.name() == 'chrome.exe' and '--test-type=webdriver' in process.cmdline():
                    with suppress(psutil.NoSuchProcess):
                        self.kill_list.append(process.pid)
            for proc_id in self.kill_list:
                os.kill(int(proc_id), signal.SIGTERM)
            self.write(Fore.RED + '[2] Threads...')
            self.write(Fore.RED + 'Goodbye.')
            quit()


SniperOMancer().run()
