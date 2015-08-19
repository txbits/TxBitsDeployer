#!/usr/bin/env sh
./valid_env.sh $0 $1
if [ $? -ne 0 ]; then
  exit 1
fi
./txbits/txbits.sh universal:packageZipTarball
cd playbook
  ansible-playbook -i ${1}_hosts main.yml --skip-tags=slow -t rebuild_coins --extra-vars 'rebuild_coins=true'
cd -
