#!/usr/bin/env sh
./valid_env.sh $0 $1
if [ $? -ne 0 ]; then
  exit 1
fi
cd playbook
  ansible-playbook -i ${1}_hosts -t db_wipe main.yml --extra-vars 'db_wipe=true'
cd -
