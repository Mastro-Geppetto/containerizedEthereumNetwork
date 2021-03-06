#!/bin/bash -x

cd /root
# initalize
geth init "/root/genesis.json"

# Generate and store a wallet password
if [ ! -f ~/password ]; then
  echo `date +%s | sha256sum | base64 | head -c 32` > password
fi

mkdir -p ~/.ethereum/keystore
if [ ! -d ~/keystore ] || [ -z "$(ls -A ~/keystore)" ]; then
    mkdir -p ~/.ethereum/keystore/
    geth --password ~/password --datadir "/root/.ethereum" --keystore "/root/.ethereum/keystore" account new > ~/primaryaccount
else
    cp -rf ~/keystore/* ~/.ethereum/keystore/.
    #geth account import --password ~/password '/root/.ethereum/keystore/UTC--2018-02-27T03-44-29.286659913Z--7bacb4f41705da99157472d0f7db59b87e5f327e'
fi


# start miner
geth \
  --syncmode 'full' \
  --networkid "456719" \
  --identity "promit_priv_ethereum_net_miner_2" \
  --rpc \
  --rpcaddr 'localhost' \
  --rpcapi 'personal,db,eth,net,web3,txpool,miner' \
  --rpccorsdomain "*" \
  --gasprice '1' \
  --targetgaslimit 94000000 \
  --unlock '0x7bacb4f41705da99157472d0f7db59b87e5f327e' \
  --password ~/password \
  --mine --minerthreads 1 \
  --bootnodes="enode://288b97262895b1c7ec61cf314c2e2004407d0a5dc77566877aad1f2a36659c8b698f4b56fd06c4a0c0bf007b4cfb3e7122d907da3b005fa90e724441902eb19e@172.28.5.2:30303"
#  --verbosity 5 \
