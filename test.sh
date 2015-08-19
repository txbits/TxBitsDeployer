#!/bin/sh
./valid_env.sh $0 $1
if [ $? -ne 0 ]; then
  exit 1
fi

echo ok
