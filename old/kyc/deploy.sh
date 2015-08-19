#!/bin/bash

SERVER="$1"

if [ -e $SERVER ]
then
  echo "usage:" $0 "<target ip/host>"
else

# deploy play frontend
$(dirname $0)/../../kyc.sh dist
scp $(dirname $0)/../../kyc/target/universal/kyc-1.0-SNAPSHOT.zip ec2-user@$SERVER:/tmp/
ssh -t ec2-user@$SERVER 'kycUpdate /tmp/kyc-1.0-SNAPSHOT.zip && rm /tmp/kyc-1.0-SNAPSHOT.zip'

## start everything
ssh -t ec2-user@$SERVER 'sudo nohup /sbin/service kyc restart > /dev/null'

fi
