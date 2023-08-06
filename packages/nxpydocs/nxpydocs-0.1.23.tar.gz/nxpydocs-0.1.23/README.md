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
guestshell resize memory 2688
guesthshell reboot
```

### Update DNS
```console
[cisco@guestshell ~]sudo vi /etc/resolv.conf
nameserver <dns server IP address>
domain <domain that matches NX-OS configured domain>
```