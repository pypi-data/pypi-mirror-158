# nxpydocs
Automated NXOS Business Ready Documents from th guestshell Python

## Enable guestshell
```console
switch# guestshell enable
```
Wait until the guestshell becomes active

## Resize guestshell diskspace
```console
guestshell resize rootfs 2000
guesthshell reboot
```

## Update DNS
```console
[cisco@guestshell ~]sudo vi /etc/resolv.conf
nameserver <dns server IP address>
domain <domain that matches NX-OS configured domain>
```

## Update yum
```console
[cisco@guestshell ~]yum update -y
```
## Install Python3
```console
[cisco@guestshell ~]sudo yum install -y python3
```

## Set Python3 as default Python version
```
[cisco@guestshell ~]sudo alternatives --install /usr/bin/python python /usr/bin/python3.6 60

[cisco@guestshell ~]sudo alternatives --config python

There is 1 program that provides 'python'.

  Selection    Command
-----------------------------------------------
*+ 1           /usr/bin/python3.6

Enter to keep the current selection[+], or type selection number: 1
```

