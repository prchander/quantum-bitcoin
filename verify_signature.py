import os
import subprocess
import json

# Send a command to the linux terminal
def terminal(cmd):
	return os.popen(cmd).read()

# Send a command to the Bitcoin console
def bitcoin(cmd):
	print(u'\n \u27a4\tExecuting "' + cmd + '"\n')
	return terminal('src/bitcoin-cli -regtest -rpcuser=cybersec -rpcpassword=kZIdeN4HjZ3fp9Lge4iezt0eJrbjSi8kuSuOHeUkEUbQVdf09JZXAAGwF3R5R2qQkPgoLloW91yTFuufo7CYxM2VPT7A5lYeTrodcLWWzMMwIrOKu7ZNiwkrKOQ95KGW8kIuL1slRVFXoFpGsXXTIA55V3iUYLckn8rj8MZHBpmdGQjLxakotkj83ZlSRx1aOJ4BFxdvDNz0WHk1i2OPgXL4nsd56Ph991eKNbXVJHtzqCXUbtDELVf4shFJXame ' + cmd).strip()

# Returns True if bitcoin is running, otherwise False
def bitcoinUp():
	return winexists('Bitcoin Core - [regtest]')

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
	if check == '':
		address = bitcoin('getnewaddress signature_verification')
	else:
		parsed = json.loads(check)
		print(f'Address found: {parsed}')
		address = next(iter(parsed))
	print(f'Public: {address}')

	private = bitcoin(f'dumpprivkey {address}')
	print(f'Private: {private}')

	print()
initialize()