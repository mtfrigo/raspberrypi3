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

## 1: Hotspot with Ethernet connection

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

Save and Reboot

## 2.1: Hotspot with Wi-Fi connection 

It is important to note that you need a WiFi dongle because of the raspiberry hardware limitation.

"The Raspberry Pi is able to work as a wireless hotspot and simultanous connect to another hotspot as client. But the wifi device on the RasPi has a general limitation. The client connection cannot be bridged because lack of WDS (wireless distribution system) that is needed for bridging on wireless."

The WiFi dongle used is [Edimax EW-7811UN](https://www.edimax.com/edimax/merchandise/merchandise_detail/data/edimax/in/wireless_adapters_n150/ew-7811un/)

1. The following commands must be run.

```
sudo apt update
sudo apt install network-manager network-manager-gnome openvpn \openvpn-systemd-resolved network-manager-openvpn \network-manager-openvpn-gnome
sudo apt purge openresolv dhcpcd5
sudo ln -sf /lib/systemd/resolv.conf /etc/resolv.conf
```

2. Delete `Wireless & Wired Network` and the respective `Space` from Task Bar.

<img src="./hotspot1.png" width="300">
<img src="./hotspot2.png" width="300">

3. Reboot `sudo reboot`

4. Now before setting up the Hotspot you have to connect to your WiFi connection.

It is important to point that you have to connect as client to the WiFi with the WiFi dongle, because it doesn't work as a WiFi repeater (but the build in WiFi hardware on Raspi does).

You just have to click on the WiFi you want to connect on the **WiFi Networks (Edimax EW-7811Un)**, and set the correct password. 

<img src="./wifihotspot.png" width="300">

5. Now you should create the Hotspot. 

<img src="./wifi1.png" width="300">
<img src="./wifi2.png" width="300">
<img src="./wifi3.png" width="300">

6. It is important here to setup this connection to the Raspberry Pi build in WiFi hardware. For this, you have to select the wlan that begin with **B8** in the device selector. And dont forget to select Mode as **Hotspot**.

Connection name does not matter, it is the name that gonna be shown to you.

SSID is the connection name that will be displayed.

<img src="./wifi4.png" width="300">

7. Set up a password for the connection.

<img src="./wifi5.png" width="300">

8. Set up the priority as 1, otherwise the connection as client could get the Raspberry Pi hardware and the Hotspot wont work!

<img src="./wifi8.png" width="300">

9. Save and Reboot.

## 2.2: Hotspot with Eduroam connection 

It is basically the same as above, but you have to setup the client connection as Eduroam.

1. Follow the above instructions to number 3.

2.1. First you have to download the Linux Script from [eduroam-cat](https://cat.eduroam.org/)

2.2 You have to transfer to your Raspi the script `eduroam-linux-Universitat_Stuttgart-STUDENT.py` (it could be via SSH)

2.3 Run the script with sudo `sudo python path/eduroam-linux-Universitat_Stuttgart-STUDENT.py`

2.4 It will ask you credentials.

2.5 After installation, copy the certificate from `/root/.cat_installer/ca.pem/` to another folder (it worked on Desktop)

`sudo cp /root/.cat_installer/ca.pem /home/pi/Desktop`

2.6 Edit the eduroam config file created by the installation. Remove the root permission and change the certificate path to the new one.

`sudo nano /etc/NetworkManager/system-connections/eduroam.nmconnection`

Edit the line `permissions=:user::root:;` to `permissions=`

Edit the line `ca-cert=/root/.cat_installer/ca.pem` to `ca-cert=/home/pi/Desktop/ca.pem`

Save and exit.

3. Now your eduroam should work after rebooting, but first follow the remaining steps from the guide above (5 to 9).

## 3: Hotspot with VPN

To use VPN you just need to install openconnect with `sudo apt-get install openconnect`

And then, run the command

`sudo openconnect -u USER_ID -b VPN_ADDRESS`

Where **USER_ID** is your vpn id and **VPN_ADDRESS** is the address for the VPN (*vpn.informatik.uni-stuttgart.de at the moment*)

