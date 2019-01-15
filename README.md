# Containerized Ethereum Network
Automated containerized Ethereum (geth) Network using shell scripting, with sample python script to execute a smart contract.

### Note that Blockchain & crypto currency are nascent technologies and can change at anytime.
### So this setup might stop working in future.
### There are many great guides and articles out there. This is a implementation which can be easily understood by any programer

This setup was tested on Windows & Ubuntu.

## Prerequisite

1. docker or docker-toolbox (windows) should be installed.
2. Install python 3.6
3. Install build tools for visual studio 2017 from one of the [link](https://www.visualstudio.com/downloads/#build-tools-for-visual-studio-2017).
It is 4+ gb download and takes 20-30min installation time.

   [click here to know the reason](https://wiki.python.org/moin/WindowsCompilers#Microsoft_Visual_C.2B-.2B-_14.0_standalone:_Build_Tools_for_Visual_Studio_2017_.28x86.2C_x64.2C_ARM.2C_ARM64.29)
4. Install [git](https://git-scm.com/download/win)
5. On Windows install [git bash](https://git-scm.com/download/win) or cygwin. Linux users can skip this step.
6. Clone my repository : ```git clone https://github.com/Mastro-Geppetto/containerizedEthereumNetwork.git```
7. Update python setuptools : ```pip install --upgrade setuptools```
8. Change directory to the cloned git repo directory.
9. Install python libs to interact with Ethereum Network : ```pip install -r requirements.txt```
10. Check docker is running : ```docker images```

## Build geth docker image
1. ```geth``` is Ethereum client written in Go.
2. We have a number of docker image options from custom docker image to official image.
3. Build Custom image with name *local/ethereumbase:latest*: ```docker build -t "local/ethereumbase:latest" -f ./Dockerfile .```
4. Instead to use official ```Dockerfile-official-alltools-image``` build with ```docker build -t "ocal/ethereumbase:latest" -f ./Dockerfile-official-alltools-image .```
5. Check Docker image ```docker images```

## Start network
- In bash shell change directory to cloned directory.
- ```./deploy```
- It will start
  - geth nodes : one bootnode, two miners and one eth node to interact : check Container IDs with ```docker ps```
  - create a bridge network "ether_priv_net" between containers : check IP with ```docker network ls```
  - disk volumes per nodes named as "bootnode_vol", "miner_1_vol" and so on : check with ```docker volume ls```
  - **Note: genesis.json is present in [common folder](https://github.com/Mastro-Geppetto/containerizedEthereumNetwork/tree/master/common)**
- This network has 9 prefilled accounts. Check [keystore](https://github.com/Mastro-Geppetto/containerizedEthereumNetwork/tree/master/common/keystore).
  - Out of that first four are used by bootnode, 2 miners & 1 eth node.
  - [Google Genesis ethereum](https://www.google.com/search?q=genesis+block+ethereum)
  - [What is Mining in ethereum ?](https://github.com/ethereum/wiki/wiki/Mining#introduction)
  
## Interact with network using command line in nodes
- **Miner node**
  - Initial DAG creation will take 5/10 mins. Miner nodes will create initial [DAG]( https://ethereum.stackexchange.com/questions/1993/what-actually-is-a-dag)
  - check miner logs. On bash run ```docker log miner_1```
  - **SAMPLE LOG**
  ```
  Generating DAG in progress               epoch=0 percentage=99 elapsed=19m41.071s
  Generating ethash verification cache     epoch=1 percentage=3  elapsed=3.284s
  ```
- **Eth client node**
  - Mean while check accounts and balance on eth node
  - attach to eth node's *geth* console : ```docker exec -it eth geth attach```
  - use geth console to check that block count is increasing each 10 sec as configured in [genesis](https://github.com/Mastro-Geppetto/containerizedEthereumNetwork/tree/master/common)
  - use the below commands one by one.
  ```
  eth.blockNumber
  # might output 16 
  eth.hashrate
  # 10
  eth.accounts
  #["0xa4b5db581bdee808c1896fac99ff22074885b079", "0x085db52a09584a953fab3046db4dd19474affc33", "0xe8c330a9112191ddcd65dd10f7ec60f32ab2067e", "0xf8ae31b2f7e68c36fff1370326aa6a7a9c586d69", "0x7eb19dbc863aa4f2e601b0e736a6000acc0e14b2", "0xc513ce206b0cd02b12b85796f87f6505cbf0e6f5"]
  eth.getBalance(eth.accounts[0])
  ```
  - In this non bootnode check that it shows 2 peers ```admin.peers```
  - Check your own address ```admin.nodeInfo.enode```
  - Check below for more examples.
  

## Stop network
- In bash shell from cloned directory give ```./shutdown```
- **Note** we created docker disk volumes, ```./shutdown``` will not clear these.
- Thus giving ```./deploy``` to a ```./shutdown``` network will start iit from last mined block.

## Cleanup network
- In bash shell from cloned directory give ```./shutdown``` then ```./cleanup```

## Console Example of Transcation : sending ether (crypto currency) to another address
- Login to client node ```docker exec -it eth geth attach```
- ```eth.coinbase``` will produce your coinbase / purse hash. Example ```"0xa4b5db581bdee808c1896fac99ff22074885b079"```
- ```eth.accounts``` will show list of all accounts on this network.
  - These are visible here because they were add in [genesis block](https://github.com/Mastro-Geppetto/containerizedEthereumNetwork/tree/master/common)
  - ```Output : ["0xa4b5db581bdee808c1896fac99ff22074885b079", "0x085db52a09584a953fab3046db4dd19474affc33", "0xe8c330a9112191ddcd65dd10f7ec60f32ab2067e", "0xf8ae31b2f7e68c36fff1370326aa6a7a9c586d69", "0x7eb19dbc863aa4f2e601b0e736a6000acc0e14b2", "0xc513ce206b0cd02b12b85796f87f6505cbf0e6f5"]```
- Send some ether to another account. It will output **transaction hash**.
```eth.sendTransaction({'from':eth.coinbase, 'to':'0xae17b64a594024b4df2158f804795cfba0d356f2', 'value':web3.toWei(3, 'ether')})
Output : "0xf2b0f7ef1ee3dd6c9ae5857ca481354efa46277a241e3d5369c070a6a577358e"
```
- using the **Output** hash get transaction receipt.
  - **Note** Transaction processing time == mining rate of block
  - **for a unprocessed transaction**
  ```
  eth.getTransactionReceipt("0xf2b0f7ef1ee3dd6c9ae5857ca481354efa46277a241e3d5369c070a6a577358e")

  Error: unknown transaction
      at web3.js:3143:20
      at web3.js:6347:15
      at web3.js:5081:36
      at <anonymous>:1:1
  ```
  - **processed transaction**
  ```
  eth.getTransactionReceipt("0xf2b0f7ef1ee3dd6c9ae5857ca481354efa46277a241e3d5369c070a6a577358e")
  {
    blockHash: "0xd58bfda2fb8800c0c7ad3ce32c2523b3526e5602f9a8c506f6df785955f0a41b",
    blockNumber: 24,
    contractAddress: null,
    cumulativeGasUsed: 21000,
    from: "0xa4b5db581bdee808c1896fac99ff22074885b079",
    gasUsed: 21000,
    logs: [],
    logsBloom: "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    status: "0x1",
    to: "0xae17b64a594024b4df2158f804795cfba0d356f2",
    transactionHash: "0xf2b0f7ef1ee3dd6c9ae5857ca481354efa46277a241e3d5369c070a6a577358e",
    transactionIndex: 0
  }
  ```
  

## Smart Contract
- Ethereum uses ["Solidity"](https://solidity.readthedocs.io/en/v0.5.1/) programing language & online Compiler named ["remix"](http://remix.ethereum.org/).
- Code is quite comprehensible.
- I have pre-compiled my smart contract code online & put in the python script.
- [This is another smart contract example.](http://remix.ethereum.org/#optimize=false&version=soljson-v0.4.20+commit.3155dd80.js)
- My solidity code with comments
  ```
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

      /* Constant function => no charges to user to execute */
      function getvalue() public constant returns (string) {
          return value;
      }

      ////////////////////////////////////////////////
      // BELOW EXPERIMENTAL CODE SHOULD BE SKIPPED
      // we can log events
      // event setvalue
      /*
      // array of viewers : To Be Done
      address [] viewers;

      function transferOwnership( address newOwner ) public {
        owner = newOwner;
      }*/
  }
  ```

## Python [client](https://github.com/Mastro-Geppetto/containerizedEthereumNetwork/tree/master/main.py) code
- From cloned directory start python script interactively ```python -i main.py```
- My python code ```JSONRPCBaseClient``` directly pushes compiled *bytecode* to deploy a smart contract.
  - ```JSONRPCBaseClient``` will connect to eth node on ```127.0.0.1:8545```
- In python console after first step select a password ``` password="UR_OWN_Password"
- *Create user* ```userId = createuser( password ) ```
- *Deploy contract* ```fixed_contract_hash = a=deploy_contract( userId, password )```
  - This operation will consume some gas ( actually smaller denomination of ether called wei ) because blockchain was modified.
    - "gas" is a proportion or a priority set by user. In this code I have defaulted the gas value to 1.
- *Set LandRecord* ```trans_receipt = setdata( userId, password, fixed_contract_hash )```
  - Each modify ie set operation will also consume gas.
  - In my actual project we saved a hash string which translated to a secured file server URL.
  - This URL was meaningless outside our server.
- *Get LandRecord* ```getdata( fixed_contract_hash )```
  - This doesn't modify blockchain so its free of any wei charge.
 
