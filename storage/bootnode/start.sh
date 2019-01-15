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
    #geth account import --password ~/password /root/.ethereum/keystore/UTC*
fi

# start bootnode
#bootnode --nodekeyhex="091bd6067cb4612df85d9c1ff85cc47f259ced4d4cd99816b14f35650f59c322"

geth \
  --networkid "456719" \
  --identity "promit_priv_ethereum_net_bootnode" \
  --rpc \
  --rpccorsdomain "*" \
  --maxpeers 6 \
  --gasprice '1' \
  --targetgaslimit 94000000 \
  --unlock '0xae17b64a594024b4df2158f804795cfba0d356f2' \
  --password "/root/password" \
  --nodekeyhex="091bd6067cb4612df85d9c1ff85cc47f259ced4d4cd99816b14f35650f59c322"
#  --verbosity 5 \
