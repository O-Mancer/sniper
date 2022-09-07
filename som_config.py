# SOM CONFIG FILE

# GENERAL SETTINGS
bscScanAPIKey = ''
wallet_address = ''
private_key = ''
manual_rpc = False
save_tokens_to_csv = True

# BUY SETTINGS - Basic settings
buy_mode = False
buy_amount = 0.01
maximum_buy_tax = 10
maximum_sell_tax = 10
minimum_market_cap = 50
minimum_liquidity = 500
analyze_mc_liq_ratio = True
txn_speed = 'standard'

# TOKEN AUDIT SETTINGS
enableMiniAudit = True
checkSourceCode = True
checkPancakeV1Router = True
checkValidPancakeV2 = True
checkMintFunction = True
checkHoneypot = True

# PAPER MODE SETTINGS
fake_mode = True
fake_balance = 10
fake_buy = 1

# BUY SETTINGS - Xs and Fee
takeprofit_x = 2
stoploss_x = 2
transaction_fee = 0.00088025

# MISC OPTIONS
telegram_enabled = False
telegram_bot_key = ''
telegram_bot_chat_id = ''
token_watcher_sleep = 5
max_scraper_wait = 5
updater_sleep_time = 5
overview_sleep_time = 60
maximum_database_index = 10
maximum_minutes_in_database = 30
rpc_lists = ['https://bsc-dataseed1.binance.org',
             'https://bsc-dataseed2.binance.org', 'https://bsc-dataseed3.binance.org',
             'https://bsc-dataseed4.binance.org']
