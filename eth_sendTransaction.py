from web3.auto import w3
from web3 import Web3
web3 = Web3(Web3.HTTPProvider("HTTP://localhost:30304"))
account_1 = "0x04d856a4f43EB1C9c9F18f1364E047aA6E035B71" 
acoount_2 = "0xe000c32900c3e36552bf961a9c42ceb38bedd84b"
private_key = private_hx

nonce = web3.eth.getTransactionCount(account_1)

txt = {'from': nonce,
        'to': account_2,
        'value': web3.toWei(1,'ether'),
        'gas': 2000000
        'gasPrice': web3.toWei('50','gwei') 
      }
signed_tx = web3.eth.account.signTransaction(tx,private_key)         # Error  ValueError: The private key must be exactly 32 bytes long, instead of 64 bytes.
tx_hash = web3.eth.sendTransaction(signed_tx.rawTransaction)
print(web3.toHex(tx_hash))
