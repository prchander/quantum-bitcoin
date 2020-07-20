import os
import subprocess
import json
import time

# Send a command to the linux terminal
def terminal(cmd):
	return os.popen(cmd).read()

# Send a command to the Bitcoin console
def bitcoin(cmd):
	print(u'\n \u27a4\tExecuting "' + cmd + '"')
	return terminal('src/bitcoin-cli -regtest -rpcuser=cybersec -rpcpassword=kZIdeN4HjZ3fp9Lge4iezt0eJrbjSi8kuSuOHeUkEUbQVdf09JZXAAGwF3R5R2qQkPgoLloW91yTFuufo7CYxM2VPT7A5lYeTrodcLWWzMMwIrOKu7ZNiwkrKOQ95KGW8kIuL1slRVFXoFpGsXXTIA55V3iUYLckn8rj8MZHBpmdGQjLxakotkj83ZlSRx1aOJ4BFxdvDNz0WHk1i2OPgXL4nsd56Ph991eKNbXVJHtzqCXUbtDELVf4shFJXame ' + cmd).strip()

# Returns True if bitcoin is running, otherwise False
def bitcoinUp():
	return winexists('Bitcoin Core - [regtest]') or winexists('Custom Bitcoin Console') 

def winexists(target):
    for line in subprocess.check_output(['wmctrl', '-l']).splitlines():
        window_name = line.split(None, 3)[-1].decode()
        if window_name == target:
            return True
    return False

# Main function
def initialize():
	os.system('clear')

	print('SIGNATURE VERIFICATION IS BEGINNING')

	if not bitcoinUp():
		print('Bitcoin is not running')
		return

	check = bitcoin('getaddressesbylabel signature_verification')
	address = ''
	if check == '':
		address = bitcoin('getnewaddress signature_verification')
	else:
		parsed = json.loads(check)
		print(f'Address found: {parsed}')
		address = next(iter(parsed))
	print(f'Public: {address}')

	private = bitcoin(f'dumpprivkey {address}')
	print(f'Private: {private}')

	while bitcoin('listunspent') == '[\n]':
		bitcoin(f'generatetoaddress 20 {address}')
		time.sleep(1)

	blockheight = bitcoin('getblockcount')
	blockhash = bitcoin(f'getblockhash {blockheight}')
	raw_block = bitcoin(f'getblock {blockhash}')
	print(f'Block = {raw_block}')

	block = json.loads(raw_block)

	txid = block['tx'][0]
	raw_tx = bitcoin(f'gettransaction {txid}')
	print(f'Transaction = {raw_tx}')

	tx_out = bitcoin(f'gettxout {txid} 0')
	print(f'Transaction out = {tx_out}')

	balance = bitcoin('getbalance')
	sent_money = bitcoin(f'sendtoaddress {address} {balance} "" "" true')
	print(f'Sent money ID = {sent_money}')

	mempool_entry = bitcoin(f'getmempoolentry {sent_money}')
	print(f'Mempool entry = {mempool_entry}')
	print()
	print('Final outcome:')
	print()

	print(' ' + '*' * 50)
	print(' ' + '*' * 50)
	if mempool_entry == '':
		print(' **' + 'TRANSACTION WAS UNSUCCESSFUL'.center(50 - 4) + '**')
	else:
		print(' **' + 'TRANSACTION WAS SUCCESSFUL'.center(50 - 4) + '**')
	print(' ' + '*' * 50)
	print(' ' + '*' * 50)
	print()
	print()


initialize()