# nxpydocs
Automated NXOS Business Ready Documents from th guestshell Python

## Setting up guestshell and Python3.8
### Enable guestshell
```console
switch# guestshell enable
```
Wait until the guestshell becomes active

### Resize guestshell diskspace
```console
guestshell resize rootfs 2000
guesthshell reboot
```

### Update DNS
```console
[cisco@guestshell ~]sudo vi /etc/resolv.conf
nameserver <dns server IP address>
domain <domain that matches NX-OS configured domain>
```

### Update yum
```console
[cisco@guestshell ~]yum update -y
```
### Install Python3.8
```console
[cisco@guestshell ~]sudo yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel
[cisco@guestshell ~]sudo yum -y install wget
[cisco@guestshell ~]cd /opt
[cisco@guestshell ~]sudo wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz
[cisco@guestshell ~]tar xzf Python-3.8.12.tgz
[cisco@guestshell ~]cd Python-3.8.12
[cisco@guestshell ~]sudo ./configure --enable-optimizations
[cisco@guestshell ~]sudo make altinstall
[cisco@guestshell ~]sudo rm Python-3.8.12.tgz
[cisco@guestshell ~]python3.8 -V
```

### Set Python3 as default Python version
```
[cisco@guestshell ~]sudo alternatives --install /usr/bin/python python /usr/bin/python3.8 60

[cisco@guestshell ~]sudo alternatives --config python

There is 1 program that provides 'python'.

  Selection    Command
-----------------------------------------------
*+ 1           /usr/bin/python3.8

Enter to keep the current selection[+], or type selection number: 1
```