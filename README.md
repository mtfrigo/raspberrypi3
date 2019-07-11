# raspberrypi3

## Utils

### How to know the MAC address knowing the interface

```cat /sys/class/net/wlan0/address```

Where wlan0 is the interface.


### How to connect on the EDUROAM on raspberry pi 3 B (after july 2019) (tested with Buster)

First you need, with another computer, download the file from https://cat.eduroam.org/ to Linux installer...

Then you will download a python script,

Somehow transfer this file to the Raspi (pendrive, scp with ethernet/another wifi, etc),

Before running the script you need to install the following stuff:

```
sudo apt update
sudo apt install network-manager network-manager-gnome openvpn \openvpn-systemd-resolved network-manager-openvpn \network-manager-openvpn-gnome
sudo apt purge openresolv dhcpcd5
sudo ln -sf /lib/systemd/resolv.conf /etc/resolv.conf
```

Reboot and run the script, it will ask your credentials for Eduroam

Copy the certificate generated to another folder (it worked on desktop `sudo cp /root/.cat_installer/ca.pem ~/Desktop`)

Then, edit the file created for the script in  `/etc/NetworkManager/system-connections/`

In my case it was `/etc/NetworkManager/system-connections/eduroam.nmconnection`

Edit the line which says `permissions=:user:root:;` to `permissions=`

And the line `ca-cert=/root/.cat_installer/ca.pem` to `ca-cert=/home/pi/Desktop/ca.pem`

Reboot and you are done!

### Hotspot (tested with Stretch)

```
sudo apt update
sudo apt install network-manager network-manager-gnome openvpn \openvpn-systemd-resolved network-manager-openvpn \network-manager-openvpn-gnome
sudo apt purge openresolv dhcpcd5
sudo ln -sf /lib/systemd/resolv.conf /etc/resolv.conf
```

<img src="./Hotspot/hotspot1.png" width="200">

<img src="./Hotspot/hotspot2.png" width="200">

```
sudo reboot
```

<img src="./Hotspot/hotspot3.png" width="200">

<img src="./Hotspot/hotspot4.png" width="200">

<img src="./Hotspot/hotspot5.png" width="200">

<img src="./Hotspot/hotspot6.png" width="200">

<img src="./Hotspot/hotspot7.png" width="200">

Save

```
sudo reboot
```

### How to connect to vpn in raspberry pi

You can check the full guide here: [OpenConnect](https://cs.uwaterloo.ca/twiki/view/CF/OpenConnect)

First install OpenConnect:

`apt-get install openconnect network-manager-openconnect-gnome`


Then:


`sudo openconnect -u USER_ID -b VPN_ADDRESS`

Where **USER_ID** is your vpn id and
**VPN_ADDRESS** is the address for the VPN (*vpn.informatik.uni-stuttgart.de* at the moment)