# coreos-xhyve

```
brew install xhyve
brew install gpg
sudo nfsd enable
sudo nfsd start

/etc/exports:
/Users -alldirs -mapall=your_username -network=192.168.64.0 -mask=255.255.255.0

git clone git@github.com:coreos/coreos-xhyve.git
cd coreos-xhyve

sudo CLOUD_CONFIG="https://gist.githubusercontent.com/grepory/41ebc61e58111b000813/raw/de2dfdf5470a310158aeb21b84f3f7e194b7c131/cloud_config.yaml" ./coreos-xhyve-run
```

To use docker, get the IP for the xhyve VM.

```
unset DOCKER_TLS_VERIFY
unset DOCKER_CERT_PATH
export DOCKER_HOST=tcp://vmip:2376
```

That should do it.

You can stop here.

If you want to host more stuff locally:

```
mkdir ~/Sites
edit /etc/apache2/httpd.conf
Uncomment: 
#Include /private/etc/apache2/extra/httpd-userdir.conf

edit /etc/apache2/httpd-userdir.conf
Uncomment:
#Include /private/etc/apache2/users/*.conf

sudo apachectl start
sudo cat > /etc/apache2/users/your_username.conf
<Directory "/Users/your_username/Sites/">
    Options Indexes MultiViews
    AllowOverride None
    Require ip 127.0.0.1 192.168
</Directory>

sudo apachectl restart
```
