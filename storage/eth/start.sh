#!/bin/bash -x

cd /root
# initalize
geth init "/root/genesis.json"

# Generate and store a wallet password
if [ ! -f ~/password ]; then
  echo `date +%s | sha256sum | base64 | head -c 32` > password
fi

mkdir -p ~/.ethereum/keystore
if [ ! -d ~/keystore/ ] || [ -z "$(ls -A ~/keystore)" ] ; then
    mkdir -p ~/.ethereum/keystore/
    geth --password ~/password --datadir "/root/.ethereum" --keystore "/root/.ethereum/keystore" account new > ~/primaryaccount
else
    cp -rf ~/keystore/* ~/.ethereum/keystore/.
    #geth account import --password ~/password /root/.ethereum/keystore/UTC*
fi


# start eth
####### THESE ACCOUNTS ARE PREFUNDED AND WILL BE UNLOCKED BY ETH  #############
#UTC--2018-02-27T03-44-35.768299726Z--a4b5db581bdee808c1896fac99ff22074885b079
#UTC--2018-02-27T03-44-40.234052495Z--085db52a09584a953fab3046db4dd19474affc33
#UTC--2018-02-27T03-45-38.534454485Z--e8c330a9112191ddcd65dd10f7ec60f32ab2067e
#UTC--2018-02-27T03-45-44.404308096Z--f8ae31b2f7e68c36fff1370326aa6a7a9c586d69
#UTC--2018-02-27T03-45-45.859389630Z--7eb19dbc863aa4f2e601b0e736a6000acc0e14b2
#UTC--2018-02-27T03-45-59.000703068Z--c513ce206b0cd02b12b85796f87f6505cbf0e6f5
###############################################################################
geth \
  --maxpeers 6 \
  --networkid "456719" \
  --identity "promit_priv_ethereum_net_eth" \
  --rpc \
  --rpccorsdomain "*" \
  --rpcaddr "0.0.0.0" \
  --rpcapi "db,eth,net,web3,personal,admin" \
  --rpcport=8545 \
  --gasprice '1' \
  --targetgaslimit 94000000 \
  --unlock '0xa4b5db581bdee808c1896fac99ff22074885b079' \
  --password ~/password \
  --bootnodes="enode://288b97262895b1c7ec61cf314c2e2004407d0a5dc77566877aad1f2a36659c8b698f4b56fd06c4a0c0bf007b4cfb3e7122d907da3b005fa90e724441902eb19e@172.28.5.2:30303"
  #--verbosity 5 \
