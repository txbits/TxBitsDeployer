# TxBitsDeployer

An Ansible config to help you deploy TxBits in production.

## Usage

1. git clone https://github.com/txbits/TxBitsDeployer.git
1. `bootstrap.sh`
1. Continue in one of the two sections below

### In development / staging

1. Set up a virtual machine with 512 MB of ram and 1 core. We recommend VirtualBox for this. *
1. Install Debian 7.x on it, add your ssh key and clone it into 7 machines
1. Check the ips of the machines and put them into `playbook/group_vars/staging_testnet`
1. On your host set up your hosts file like this:
    ```
    192.168.56.107       longcat.staging-testnet-txbits.com
    192.168.56.104     grumpycat.staging-testnet-txbits.com
    192.168.56.106       limecat.staging-testnet-txbits.com
    192.168.56.102   businesscat.staging-testnet-txbits.com
    192.168.56.105        bitcat.staging-testnet-txbits.com
    192.168.56.103       litecat.staging-testnet-txbits.com
    192.168.56.108          mail.staging-testnet-txbits.com

    192.168.56.107               staging-testnet-txbits.com
    192.168.56.104       monitor.staging-testnet-txbits.com
    ```
1. `./initial_deploy.sh staging_testnet`

* You may be able to do this faster with Vagrant, but we haven't tried doing it yet.

### In production

1. Set up the 7 machines as described above, but this time with a VPS provider. The bitcoin virtual machine might need more storage than the 20GB you get with Digital Ocean for $5/month. Check the current size of the blockchain. Make sure all the machines can talk to each other over a LAN (even though all communication between them is encrypted)
1. Copy `playbook/staging_testnet_hosts` to `playbook/production_hosts` and replace any references to `staging_testnet` with `production`
1. Copy `playbook/group_vars/staging_testnet` to `playbook/group_vars/production` if it doesn't already exist
1. Update the private ips in `playbook/group_vars/production`
1. Create a secrets file in `playbook/secrets` called `production.json` based on `staging_testnet.json`
1. Install the only dependency for gen.py: `pip3 install passlib`
1. Run `python3 ./gen.py production.json`
1. `./initial_deploy.sh production`


### Setting up the database

After deploying, you'll need to set up the database in order for the frontend to start up. It should be as simple as:

1. `./dbmigrate.sh <environment>`
1. `./dbpopulate.sh <environment>`

After deploying the database you'll need to restart the frontend.
