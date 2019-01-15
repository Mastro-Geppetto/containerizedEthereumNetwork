import requests
import os, sys
import time,json
import logging
#from subprocess import getoutput
import web3
from web3.main import ( add_0x_prefix, remove_0x_prefix )
from web3.contract import ConciseContract
# from web3.utils.transactions import wait_for_transaction_receipt
#from eth_keyfile import decode_keyfile_json
# import pdb

#######################
'''
use http://remix.ethereum.org/#optimize=false&version=soljson-v0.4.20+commit.3155dd80.js
'''
#######################
'''
pragma solidity ^0.4.0;
contract auid{
    /* Define variable value of the type string */
    string value;
    /* Define variable owner of the type address */
    address owner;

    
    /* CTOR : This runs when the contract is executed */
    /* This function is executed at initialization and sets the owner of the contract */
    function auid() public { owner = msg.sender; }
    
    /* DTOR : Function to recover the funds on the contract */
    function kill() public { if (msg.sender == owner) selfdestruct(owner); }
    
   
    /* Main function */
    function setvalue(string _value) public {
        value = _value;
    }

    function getvalue() public constant returns (string) {
        return value;
    }
    
    ////////////////////////////////////////////////
    // BELOW EXPERIMENTAL CODE SHOULD BE SKIPPED
    // we can log events
    // event setvalue
    /*
    // array of viewers
    address [] viewers;
    
    function transferOwnership( address newOwner ) public {
      owner = newOwner;
    }*/
}
'''

"""
WEB3DEPLOY 
ie on geth console these commands will deploy a contract
var auidContract = web3.eth.contract([{"constant":false,"inputs":[{"name":"_value","type":"string"}],"name":"setvalue","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"kill","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getvalue","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]);
var auid = auidContract.new(
   {
     from: web3.eth.accounts[0], 
     data: '0x6060604052341561000f57600080fd5b33600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506103968061005f6000396000f300606060405260043610610057576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680631ee41bab1461005c57806341c0e1b5146100b957806369bd01c4146100ce575b600080fd5b341561006757600080fd5b6100b7600480803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509190505061015c565b005b34156100c457600080fd5b6100cc610176565b005b34156100d957600080fd5b6100e1610209565b6040518080602001828103825283818151815260200191508051906020019080838360005b83811015610121578082015181840152602081019050610106565b50505050905090810190601f16801561014e5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b80600090805190602001906101729291906102b1565b5050565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141561020757600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16ff5b565b610211610331565b60008054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156102a75780601f1061027c576101008083540402835291602001916102a7565b820191906000526020600020905b81548152906001019060200180831161028a57829003601f168201915b5050505050905090565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106102f257805160ff1916838001178555610320565b82800160010185558215610320579182015b8281111561031f578251825591602001919060010190610304565b5b50905061032d9190610345565b5090565b602060405190810160405280600081525090565b61036791905b8082111561036357600081600090555060010161034b565b5090565b905600a165627a7a72305820dddf6b25360475993517ed51ef8a33e6896ed36cce86c698d6edf832869119630029', 
     gas: '4700000'
   }, function (e, contract){
    console.log(e, contract);
    if (typeof contract.address !== 'undefined') {
         console.log('Contract mined! address: ' + contract.address + ' transactionHash: ' + contract.transactionHash);
    }
 })
"""

#object
sample_bytecode={
	"linkReferences": {},
	"object": "6060604052341561000f57600080fd5b33600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506103968061005f6000396000f300606060405260043610610057576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680631ee41bab1461005c57806341c0e1b5146100b957806369bd01c4146100ce575b600080fd5b341561006757600080fd5b6100b7600480803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509190505061015c565b005b34156100c457600080fd5b6100cc610176565b005b34156100d957600080fd5b6100e1610209565b6040518080602001828103825283818151815260200191508051906020019080838360005b83811015610121578082015181840152602081019050610106565b50505050905090810190601f16801561014e5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b80600090805190602001906101729291906102b1565b5050565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141561020757600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16ff5b565b610211610331565b60008054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156102a75780601f1061027c576101008083540402835291602001916102a7565b820191906000526020600020905b81548152906001019060200180831161028a57829003601f168201915b5050505050905090565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106102f257805160ff1916838001178555610320565b82800160010185558215610320579182015b8281111561031f578251825591602001919060010190610304565b5b50905061032d9190610345565b5090565b602060405190810160405280600081525090565b61036791905b8082111561036357600081600090555060010161034b565b5090565b905600a165627a7a72305820dddf6b25360475993517ed51ef8a33e6896ed36cce86c698d6edf832869119630029",
	"opcodes": "PUSH1 0x60 PUSH1 0x40 MSTORE CALLVALUE ISZERO PUSH2 0xF JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST CALLER PUSH1 0x1 PUSH1 0x0 PUSH2 0x100 EXP DUP2 SLOAD DUP2 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF MUL NOT AND SWAP1 DUP4 PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND MUL OR SWAP1 SSTORE POP PUSH2 0x396 DUP1 PUSH2 0x5F PUSH1 0x0 CODECOPY PUSH1 0x0 RETURN STOP PUSH1 0x60 PUSH1 0x40 MSTORE PUSH1 0x4 CALLDATASIZE LT PUSH2 0x57 JUMPI PUSH1 0x0 CALLDATALOAD PUSH29 0x100000000000000000000000000000000000000000000000000000000 SWAP1 DIV PUSH4 0xFFFFFFFF AND DUP1 PUSH4 0x1EE41BAB EQ PUSH2 0x5C JUMPI DUP1 PUSH4 0x41C0E1B5 EQ PUSH2 0xB9 JUMPI DUP1 PUSH4 0x69BD01C4 EQ PUSH2 0xCE JUMPI JUMPDEST PUSH1 0x0 DUP1 REVERT JUMPDEST CALLVALUE ISZERO PUSH2 0x67 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0xB7 PUSH1 0x4 DUP1 DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 DUP3 ADD DUP1 CALLDATALOAD SWAP1 PUSH1 0x20 ADD SWAP1 DUP1 DUP1 PUSH1 0x1F ADD PUSH1 0x20 DUP1 SWAP2 DIV MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP4 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP4 DUP4 DUP1 DUP3 DUP5 CALLDATACOPY DUP3 ADD SWAP2 POP POP POP POP POP POP SWAP2 SWAP1 POP POP PUSH2 0x15C JUMP JUMPDEST STOP JUMPDEST CALLVALUE ISZERO PUSH2 0xC4 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0xCC PUSH2 0x176 JUMP JUMPDEST STOP JUMPDEST CALLVALUE ISZERO PUSH2 0xD9 JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH2 0xE1 PUSH2 0x209 JUMP JUMPDEST PUSH1 0x40 MLOAD DUP1 DUP1 PUSH1 0x20 ADD DUP3 DUP2 SUB DUP3 MSTORE DUP4 DUP2 DUP2 MLOAD DUP2 MSTORE PUSH1 0x20 ADD SWAP2 POP DUP1 MLOAD SWAP1 PUSH1 0x20 ADD SWAP1 DUP1 DUP4 DUP4 PUSH1 0x0 JUMPDEST DUP4 DUP2 LT ISZERO PUSH2 0x121 JUMPI DUP1 DUP3 ADD MLOAD DUP2 DUP5 ADD MSTORE PUSH1 0x20 DUP2 ADD SWAP1 POP PUSH2 0x106 JUMP JUMPDEST POP POP POP POP SWAP1 POP SWAP1 DUP2 ADD SWAP1 PUSH1 0x1F AND DUP1 ISZERO PUSH2 0x14E JUMPI DUP1 DUP3 SUB DUP1 MLOAD PUSH1 0x1 DUP4 PUSH1 0x20 SUB PUSH2 0x100 EXP SUB NOT AND DUP2 MSTORE PUSH1 0x20 ADD SWAP2 POP JUMPDEST POP SWAP3 POP POP POP PUSH1 0x40 MLOAD DUP1 SWAP2 SUB SWAP1 RETURN JUMPDEST DUP1 PUSH1 0x0 SWAP1 DUP1 MLOAD SWAP1 PUSH1 0x20 ADD SWAP1 PUSH2 0x172 SWAP3 SWAP2 SWAP1 PUSH2 0x2B1 JUMP JUMPDEST POP POP JUMP JUMPDEST PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND CALLER PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND EQ ISZERO PUSH2 0x207 JUMPI PUSH1 0x1 PUSH1 0x0 SWAP1 SLOAD SWAP1 PUSH2 0x100 EXP SWAP1 DIV PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND PUSH20 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF AND SELFDESTRUCT JUMPDEST JUMP JUMPDEST PUSH2 0x211 PUSH2 0x331 JUMP JUMPDEST PUSH1 0x0 DUP1 SLOAD PUSH1 0x1 DUP2 PUSH1 0x1 AND ISZERO PUSH2 0x100 MUL SUB AND PUSH1 0x2 SWAP1 DIV DUP1 PUSH1 0x1F ADD PUSH1 0x20 DUP1 SWAP2 DIV MUL PUSH1 0x20 ADD PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 SWAP3 SWAP2 SWAP1 DUP2 DUP2 MSTORE PUSH1 0x20 ADD DUP3 DUP1 SLOAD PUSH1 0x1 DUP2 PUSH1 0x1 AND ISZERO PUSH2 0x100 MUL SUB AND PUSH1 0x2 SWAP1 DIV DUP1 ISZERO PUSH2 0x2A7 JUMPI DUP1 PUSH1 0x1F LT PUSH2 0x27C JUMPI PUSH2 0x100 DUP1 DUP4 SLOAD DIV MUL DUP4 MSTORE SWAP2 PUSH1 0x20 ADD SWAP2 PUSH2 0x2A7 JUMP JUMPDEST DUP3 ADD SWAP2 SWAP1 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 JUMPDEST DUP2 SLOAD DUP2 MSTORE SWAP1 PUSH1 0x1 ADD SWAP1 PUSH1 0x20 ADD DUP1 DUP4 GT PUSH2 0x28A JUMPI DUP3 SWAP1 SUB PUSH1 0x1F AND DUP3 ADD SWAP2 JUMPDEST POP POP POP POP POP SWAP1 POP SWAP1 JUMP JUMPDEST DUP3 DUP1 SLOAD PUSH1 0x1 DUP2 PUSH1 0x1 AND ISZERO PUSH2 0x100 MUL SUB AND PUSH1 0x2 SWAP1 DIV SWAP1 PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 KECCAK256 SWAP1 PUSH1 0x1F ADD PUSH1 0x20 SWAP1 DIV DUP2 ADD SWAP3 DUP3 PUSH1 0x1F LT PUSH2 0x2F2 JUMPI DUP1 MLOAD PUSH1 0xFF NOT AND DUP4 DUP1 ADD OR DUP6 SSTORE PUSH2 0x320 JUMP JUMPDEST DUP3 DUP1 ADD PUSH1 0x1 ADD DUP6 SSTORE DUP3 ISZERO PUSH2 0x320 JUMPI SWAP2 DUP3 ADD JUMPDEST DUP3 DUP2 GT ISZERO PUSH2 0x31F JUMPI DUP3 MLOAD DUP3 SSTORE SWAP2 PUSH1 0x20 ADD SWAP2 SWAP1 PUSH1 0x1 ADD SWAP1 PUSH2 0x304 JUMP JUMPDEST JUMPDEST POP SWAP1 POP PUSH2 0x32D SWAP2 SWAP1 PUSH2 0x345 JUMP JUMPDEST POP SWAP1 JUMP JUMPDEST PUSH1 0x20 PUSH1 0x40 MLOAD SWAP1 DUP2 ADD PUSH1 0x40 MSTORE DUP1 PUSH1 0x0 DUP2 MSTORE POP SWAP1 JUMP JUMPDEST PUSH2 0x367 SWAP2 SWAP1 JUMPDEST DUP1 DUP3 GT ISZERO PUSH2 0x363 JUMPI PUSH1 0x0 DUP2 PUSH1 0x0 SWAP1 SSTORE POP PUSH1 0x1 ADD PUSH2 0x34B JUMP JUMPDEST POP SWAP1 JUMP JUMPDEST SWAP1 JUMP STOP LOG1 PUSH6 0x627A7A723058 KECCAK256 0xdd 0xdf PUSH12 0x25360475993517ED51EF8A33 0xe6 DUP10 PUSH15 0xD36CCE86C698D6EDF8328691196300 0x29 ",
	"sourceMap": "24:1007:0:-;;;335:46;;;;;;;;368:10;360:5;;:18;;;;;;;;;;;;;;;;;;24:1007;;;;;;"
}
true=True
false=False
sample_abi=[
	{
		"constant": false,
		"inputs": [
			{
				"name": "_value",
				"type": "string"
			}
		],
		"name": "setvalue",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [],
		"name": "kill",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getvalue",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	}
]



###################  START OF MAIN PROGRAM #########################
# Initialize logger
logger = logging.getLogger(__name__)

class JSONRPCBaseClient():
    _nonce = 0
    def __init__(self,
                 ip='127.0.0.1',
                 port='8545',
                 genesisFile='genesis.json',
                 abi=sample_abi,
                 bytecode=sample_bytecode):
        # store smart contract abi and bytecode
        self.abi = abi
        self.bytecode = bytecode
        # IP address
        self.ip = ip
        self.port = port
        self.address = 'http://'+ip+':'+port
        # check if we are on docker-machine, get IP ADDRESS
        if os.environ.get('DOCKER_MACHINE_NAME'):
          logger.debug("We are inside a docker-machine on windows machine")
          IP=os.environ.get('DOCKER_HOST')
          if IP is None:
            logger.error("Couldn't get DOCKER_HOST IP address")
            sys.exit(1)
          self.ip=IP.split(':')[1].strip('/')
          self.address = 'http://'+self.ip+':'+self.port
        # create a web3 instance
        self.session = requests.Session()
        self.w3 = web3.Web3(web3.HTTPProvider(self.address))
        # get data from genesis
        self.genesisFilePath=os.path.join(os.getcwd(),'common',genesisFile)
        self.genesisFile = json.load(open(self.genesisFilePath))
        self.CHAINID = self.w3.net.version
        #self.NETWORKID = self.w3.admin.nodeInfo['protocols']['eth']['network']
        #self.CHAINID = self.w3.admin.nodeInfo['protocols']['eth']['config']['chainId']
        #self.PERIOD = self.w3.admin.nodeInfo['protocols']['eth']['config']['clique']['period']
        self.PERIOD  = self.genesisFile['config']['clique']['period']
        self.GASLIMIT= int(self.genesisFile['gasLimit'],0)
        self.contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode['object'])
    # private
    def get_nonce(self):
        self._nonce += 1
        return self._nonce
    # private
    def createJSONRPCRequestObject(self,_method, _params ):
      return {"jsonrpc":"2.0",
              "method":_method,
              "params":_params, # must be an array [value1, value2, ..., valueN]
              "id":self.get_nonce()}
    # private
    def postJSONRPCRequestObject(self,_HTTPEnpoint, _jsonRPCRequestObject):
        response = self.session.post(_HTTPEnpoint,
                                     json=_jsonRPCRequestObject,
                                     headers={'Content-type': 'application/json'})
        return response.json()
    # Public
    #def waitFor(self,method,*args, **kwargs,returnCheckMethod,duration):
    #  while(True):
    #    retVal = self.method(*args, **kwargs)
    #    if returnCheckMethod(retVal):
    #      return True
    #    time.sleep(duration/10)
    #
    # JSON-RPC Methods
    #
    def get_coinbase(self):
      return self.w3.eth.coinbase
    # Public
    def get_balance(self, address):
      return self.w3.eth.getBalance(address)
    # Public
    def get_accounts(self):
      return self.w3.eth.accounts
    # Public
    def create_newAccount( self, password ):
      return self.w3.personal.newAccount( password )
    # Public 
    def unlock_account( self, address, password ):
      return self.w3.personal.unlockAccount( address, password )
    # Public 
    #def get_privatekey(self, address, password ):
    #  """
    #  Hack : get key from hardcoded'eth' node
    #  """
    #  cmd1="docker exec eth ls -A /root/.ethereum/keystore/"
    #  cmd2="docker exec eth cat /root/.ethereum/keystore/{FILE_NAME}"
    #  # get list of keys in keystore
    #  out1=getoutput(cmd1)
    #  # address is in 0x.. format
    #  fileNamePattern = "--"+remove_0x_prefix(address)
    #  fileName=''
    #  for file in out1.split():
    #    if file.find(fileNamePattern.lower()) > 0:
    #      fileName = file
    #  if len(fileName) == 0:
    #    logger.error("Couldn't find any UTC keyfile inside \"eth\" node's /root/.ethereum/keystore/")
    #    return b'\0'.hex() # NULL
    #  # get file content
    #  keyfile_json=getoutput( cmd2.format(FILE_NAME=fileName) )
    #  # create JSON object
    #  keyfile = json.loads(keyfile_json)
    #  # We can double check by uploading the keyfile and password to
    #  # https://www.myetherwallet.com/#view-wallet-info
    #  try:
    #    privateKey = decode_keyfile_json(keyfile,password)
    #  except ValueError as err:
    #    logger.error("key file decoding failed : {0}".format(err))
    #    return b'\0'.hex() # NULL
    #  return add_0x_prefix(privateKey.hex())
    #
    ######  F U N D S  &   T R A N S A C T I O N S   #########
    # Public 
    def transfer_fund( self, fromAddress, toAddress, password, amount ):
      ''' amount is in ether'''
      if not self.unlock_account( fromAddress, password ):
        return b'\0'.hex() # NULL
      # check balance
      if self.w3.fromWei( self.get_balance( fromAddress ) ,'ether' ) < amount:
        return b'\0'.hex() # NULL
      trx = {'from':fromAddress,
             'to':toAddress,
             'value': self.w3.toWei(amount, 'ether')}
      return self.send_Transaction(trx,password)
    #
    ############### CONTRACT FUNCTIONS ##################
    # Public 
    # Public 
    def get_transactionReceipt(self, receipt):
      '''
      receipt is a 64 byte hex ex 0x74f5087b1e3840fc1b415991c84aad4fc377830291899ad61a64fdcf9cb9ce76
      '''
      value = None
      try:
        value = self.w3.eth.getTransactionReceipt( receipt )
      except ValueError as err:
        logger.debug("Invalid getTransactionReceipt : {0}".format(err))
        return b'\0'.hex() # NULL
      return value
    # Public
    def get_transactionCount(self, address):
      return self.w3.eth.getTransactionCount(address)    # 
    # Public
    def sign(self, transaction_dict,address,password):
      return self.w3.personal.sign(transaction_dict,address,password)
    # Public
    def send_rawTransaction(self, transaction_hex):
      return self.w3.eth.sendRawTransaction(transaction_hex)
    # Public 
    def send_Transaction(self,transaction_dict,password):
      return self.w3.personal.sendTransaction(transaction_dict,password)
###################################################################################################################
# global instance
client=JSONRPCBaseClient()

lastPreFundAccountIdx=0
preFundedAccounts = ["0xa4b5db581bdee808c1896fac99ff22074885b079", "0x085db52a09584a953fab3046db4dd19474affc33", "0xe8c330a9112191ddcd65dd10f7ec60f32ab2067e", "0xf8ae31b2f7e68c36fff1370326aa6a7a9c586d69", "0x7eb19dbc863aa4f2e601b0e736a6000acc0e14b2", "0xc513ce206b0cd02b12b85796f87f6505cbf0e6f5", "0xc196f592e2a9c4db2a90c413007052ed41222ad7"]
#

###################################################################################################################
def createuser( password ):
  client_address = client.create_newAccount( password )
  # 
  # 1. transfer 100 ether from default accounts
  #
  for base_account in preFundedAccounts:
    if client.w3.fromWei( client.get_balance( base_account ) ,'ether' ) > 600000:
      client.transfer_fund( base_account, client_address, "password", 300000 )
      break
  return client_address

def deploy_contract(  client_address, password ):
  #
  # 1. unlock the client account
  #
  client.unlock_account( client_address, password )
  #######################################
  # float a pre compiled smart contract #
  #######################################
  # 2. create a contract
  #contract = client.w3.eth.contract(abi=sample_abi,
  #                                  bytecode=sample_bytecode['object'])
  # 3. deploy transaction with contract
  # # gas value : rule of thumb / guess work
  # pdb.set_trace()
  """
  transaction_dict = {'from':myAddress,
                    'to':'', # empty address for deploying a new contract
                    'chainId':CHAINID,
                    'gasPrice':1, # careful with gas price, gas price below the --gasprice option of Geth CLI will cause problems. I am running my node with --gasprice '1'
                    'gas':2000000, # rule of thumb / guess work
                    'nonce':myNonce,
'data':bytecode} # no constrctor in my smart contract so bytecode is enough
  """
  tx_hash = client.contract.deploy( transaction={'from': client_address, 'gasPrice': 1, 'gas': 3000000})
  # 4. wait for transaction to get mined, this is contract address
  tx_receipt = None
  error = None
  passed=False
  while(passed == False):
    try:
      tx_receipt = client.w3.eth.getTransactionReceipt(tx_hash)
      passed=True
      break
    except ValueError as err:
      error = err
      if error.args[0]['code'] == -32000:
        time.sleep(client.PERIOD/10)
        continue
      else:
        tx_receipt = {'contractAddress': b'\0'.hex()}
        break
      #put timeout
  #tx_receipt = wait_for_transaction_receipt( client.w3,
  #                                           tx_hash )
  #### SKIPPING CHECKING tx_receipt for timeout ####
  return tx_receipt['contractAddress']

def setdata( client_address, password, contract_address, data ):
  """
  function setvalue(string _value) public {
      value = _value;
  }
  """
  #
  # 1. unlock the client account
  #
  client.unlock_account( client_address, password )
  #
  # 2. create contract interface : setter
  #
  contract_instance = client.w3.eth.contract( sample_abi,
                                              contract_address,
                                              ContractFactoryClass=ConciseContract)
  #
  # 3. set data and return new address
  #
  return contract_instance.setvalue(data, transact={'from': client_address})

def getdata( contract_address ):
  """
  function getvalue() public constant returns (string) {
      return value;
  }
  """
  #
  # create contract interface : getter
  #
  contract_instance = client.w3.eth.contract( sample_abi,
                                              contract_address,
                                              ContractFactoryClass=ConciseContract)
  # return value
  return contract_instance.getvalue()