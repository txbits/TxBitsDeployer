cd /opt/bitcoin/bitcoin
git reset --hard
git clean -f
./autogen.sh
./configure --with-incompatible-bdb --disable-hardening
make
