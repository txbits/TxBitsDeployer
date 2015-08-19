#!/bin/env python3

# WARNING: The input json file is assumed to be trusted. If you allow an attacker to
# modify this json file, the attacker can execute arbitrary commands as the user
# that runs this file

import argparse
import json
import os
import os.path
import shutil
import random
import string
from passlib.hosts import linux_context

def not_exists(*filenames):
    if all(map(lambda filename: os.path.isfile(filename), filenames)):
        print("skipping", filenames, "(all exist)")
        return False
    return True


def make_dirs(filename):
    path = os.path.dirname(filename)
    if os.path.isdir(path):
        return False
    print('creating', path)
    os.makedirs(path, exist_ok=True)
    return True


def mv(from_, to):
    shutil.move(from_, to)


def cp(from_, to):
    shutil.copy(from_, to)


def read(filename):
    with open(filename, 'r') as f:
        return f.read()


def write(filename, text):
    with open(filename, 'w') as f:
        return f.write(text)


def rm(filename):
    os.remove(filename)


def main():
    parser = argparse.ArgumentParser(description='generates secrets for txbits')
    parser.add_argument('config_json_path', metavar='config.json', help='config file path')
    args = parser.parse_args()
    with open(args.config_json_path, 'r') as conf_file:
        conf = json.load(conf_file)
        os.makedirs(conf['path'], exist_ok=True)

        def pfx(path):
            return os.path.join(conf['path'], path)

        # DKIM
        filename = pfx('opendkim/default.private')
        filename2 = pfx('opendkim/default.txt')
        if not_exists(filename, filename2):
            make_dirs(filename)
            os.system('opendkim-genkey -b 2048 -d {0}'.format(conf['mail_for_fqdn']))
            mv('default.private', pfx('opendkim/default.private'))
            print("You probably want to add this entry to your DNS:")
            print(read('default.txt'))
            mv('default.txt', pfx('opendkim/default.txt'))

        # ssl certs
        def process_cert(conf_property, dst_key_path, dst_cert_path, domain):
            if not_exists(dst_key_path, dst_cert_path):
                make_dirs(dst_key_path)
                make_dirs(dst_cert_path)
                if conf[conf_property]['self_signed']:
                    os.system('openssl req -x509 -newkey rsa:2048 -keyout {0} -out {1} -days 365 -nodes -subj {2}'.format(dst_key_path, dst_cert_path, '/CN={0}/'.format(domain)))
                    print("TLS key generated.")
                else:
                    key_path = conf[conf_property]['key_path']
                    cp(key_path, dst_key_path)
                    cert_path = conf[conf_property]['cert_path']
                    cp(cert_path, dst_cert_path)

        #TODO: change this path to be less silly
        process_cert('mail_cert',
            pfx('tls/key.pem'),
            pfx('tls/cert.pem'),
            conf['mailserver_fqdn']
        )
        process_cert('frontend_cert',
            pfx(os.path.join('certs', conf['frontend_fqdn'], 'cert.key')),
            pfx(os.path.join('certs', conf['frontend_fqdn'], 'cert.pem')),
            conf['frontend_fqdn']
        )
        process_cert('monitor_cert',
            pfx(os.path.join('certs', conf['monitor_fqdn'], 'cert.key')),
            pfx(os.path.join('certs', conf['monitor_fqdn'], 'cert.pem')),
            conf['monitor_fqdn']
        )
        process_cert('database_cert',
            pfx(os.path.join('certs', 'postgres', 'server.key')),
            pfx(os.path.join('certs', 'postgres', 'server.crt')),
            conf['database_fqdn']
        )
        process_cert('lumberjack_cert',
            pfx(os.path.join('certs', 'lumberjack', 'lumberjack.key')),
            pfx(os.path.join('certs', 'lumberjack', 'lumberjack.crt')),
            conf['monitor_fqdn']
        )
        process_cert('lumberjack_server_cert',
            pfx(os.path.join('certs', 'lumberjack', 'lumberjack_server.key')),
            pfx(os.path.join('certs', 'lumberjack', 'lumberjack_server.crt')),
            conf['monitor_fqdn']
        )
        filename = pfx(os.path.join('certs', 'lumberjack', 'monitor_ca.crt'))
        if not_exists(filename):
            cp(pfx(os.path.join('certs', 'lumberjack', 'lumberjack_server.crt')), filename)

        # dhparam
        filename = pfx('certs/{0}/dhparam.pem'.format(conf['frontend_fqdn']))
        if not_exists(filename):
            os.system('openssl dhparam -out {0} 2048'.format(filename))

        # spiped
        def make_spiped_secret(name):
            filename = pfx('spiped/'+name)
            if not_exists(filename):
                make_dirs(filename)
                os.system('dd if=/dev/urandom of={0} bs=32 count=1'.format(filename))
        spiped_secrets = [
          'memcached',
          'bitcoind',
          'litecoind'
        ]
        for s in spiped_secrets:
          make_spiped_secret(s)

        # this is secure AFAK https://docs.python.org/2/library/random.html#random.SystemRandom
        r = random.SystemRandom()
        charset = string.ascii_letters + string.digits
        def random_pass():
            return ''.join([r.choice(string.ascii_letters)] + [r.choice(charset) for x in range(41)])
        charset_lowercase = string.ascii_lowercase + string.digits
        def random_pass_lowercase():
            return ''.join([r.choice(string.ascii_lowercase)] + [r.choice(charset_lowercase) for x in range(41)])
        # vars (passwords, etc)
        filename = pfx('vars.yml')
        if not_exists(filename):
            # generate password hash for user module
            # TODO: it would be great to rename mail_password to something like mail_password_hash
            if conf['vars']['txbits_mail_password'] == '[generate]':
                conf['vars']['txbits_mail_password'] = random_pass()
            conf['vars']['mail_password'] = linux_context.encrypt(conf['vars']['txbits_mail_password'])

            text = ''
            for k, v in conf['vars'].items():
                if v == '[generate]':
                    v = random_pass()
                elif v == '[generate_lowercase]':
                    v = random_pass_lowercase()
                # XXX: this can be improved
                text += k + ': "' + v + '"\n'
            write(filename, text)
            print("Wrote vars file.")

        # trust store for trusting the self signed cert of the mail server in staging
        filename = pfx('txbits_truststore')
        if not_exists(filename):
            make_dirs(filename)
            os.system('keytool -delete -keystore {0} -import -file {1} -storepass password -noprompt'.format(filename, pfx('tls/cert.pem')))

        # tarsnap
        if conf['backups']:
            def gen_tarsnap_key(name):
                master_filename = pfx('tarsnap/{0}/master.key'.format(name))
                filename = pfx('tarsnap/{0}/writeonly.key'.format(name))
                if not_exists(master_filename, filename):
                    make_dirs(master_filename)
                    os.system('echo -n {0} | tarsnap-keygen --keyfile {1} --user {2} --machine {3}'.format(
                            conf['tarsnap_password'],
                            master_filename,
                            conf['tarsnap_username'],
                            '{0}_{1}'.format(name, conf['path'])
                        )
                    )
                    print("Created tarsnap master key.")
                    make_dirs(filename)
                    os.system('tarsnap-keymgmt --outkeyfile {0} -w {1}'.format(
                            filename,
                            master_filename
                        )
                    )
                    print("Created tarsnap write only key.")
            gen_tarsnap_key('bitcoin')
            gen_tarsnap_key('litecoin')

if __name__ == '__main__':
    main()
