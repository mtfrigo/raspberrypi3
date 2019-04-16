# raspberrypi3

## Utils

### How to know the MAC address knowing the interface

```cat /sys/class/net/wlan0/address```


### How to connect on the EDUROAM on raspberry pi 3 B

Edit the following files

It could be with your favorite text editor

e.g. `sudo nano`

/etc/network/interfaces

```
source-directory /etc/network/interfaces.d

auto lo
iface lo inet loopback

iface eth0 inet manual

allow-hotplug wlan0
iface wlan0 inet manual
wpa-conf /et/wpa_supplicant/wpa_supplicant.conf
iface  default inet dhcp
```


/etc/wpa_supplicaant/wpa_supplicant.conf


``` 
ctrl_interface=DIR=/var/run/wpa_supplicabt GROUP=netdev
update_config = 1
country = GB

network={
    ssid="eduroam"
    priority=1
    key_mgmt=WPA-EAP
    auth_alg=OPEN
    eap=PEAP
    identity="YOUR ID"
    password="YOUR PASSWORD"
    phase2="auto=NONE"
}
```

Then reboot.