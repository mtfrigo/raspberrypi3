# Hotspot

The following guide aim to use the Raspiberry Pi as a Hotspot.

There are two differents approches, the first one the Raspi is connect to the Ethernet as a uplink. The second one the Raspi is connect to a wifi.

## Software and Hardware

Raspiberry Pi 3B

Raspibian GNU/Linux 10

Buster

Raspibian

For the wifi implementation:

Edimax EW-7811UN

## 1: Hotspot with Ethernet client

```
sudo apt update
sudo apt install network-manager network-manager-gnome openvpn \openvpn-systemd-resolved network-manager-openvpn \network-manager-openvpn-gnome
sudo apt purge openresolv dhcpcd5
sudo ln -sf /lib/systemd/resolv.conf /etc/resolv.conf
```

<img src="./hotspot1.png" width="300">

<img src="./hotspot2.png" width="300">

```
sudo reboot
```

<img src="./hotspot3.png" width="300">

<img src="./hotspot4.png" width="300">

<img src="./hotspot5.png" width="300">

<img src="./hotspot6.png" width="300">

<img src="./hotspot7.png" width="300">

Save

```
sudo reboot
```
