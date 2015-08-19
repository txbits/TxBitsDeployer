#!/bin/bash

SERVER="$1"

if [ -e $SERVER ]
then
  echo "usage:" $0 "<target ip/host>"
else

# kyc update shell script
scp $(dirname $0)/scripts/kycUpdate ec2-user@$SERVER:/tmp/kycUpdate
ssh -t ec2-user@$SERVER 'sudo cp /tmp/kycUpdate /usr/bin/kycUpdate && sudo chmod +x /usr/bin/kycUpdate'
ssh ec2-user@$SERVER 'rm /tmp/kycUpdate'

# kyc init script
scp $(dirname $0)/scripts/kyc ec2-user@$SERVER:/tmp/kyc
ssh -t ec2-user@$SERVER 'sudo cp /tmp/kyc /etc/init.d/kyc && sudo chmod +x /etc/init.d/kyc && sudo chkconfig --override /etc/init.d/kyc && sudo chkconfig kyc on'
ssh -t ec2-user@$SERVER 'rm /tmp/kyc'

# jdk version
ssh -t ec2-user@$SERVER 'sudo yum remove java-1.6.0-openjdk -y; sudo yum install java-1.7.0-openjdk -y'

# key id: 8AE1B1D4
scp $(dirname $0)/cert/fileserver.pub.pem ec2-user@$SERVER:/home/ec2-user/fileserver.pub.pem
ssh ec2-user@$SERVER 'gpg --import /home/ec2-user/fileserver.pub.pem'

fi
