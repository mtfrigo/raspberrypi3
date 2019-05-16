#Install

http://www.bluez.org/download/

```
gwet http://www.bluez.org/download/
```


tar xvf bluez....

cd bluez....

nano README (check the dependencies)

apt-cache search .... (like libglib)

then 

e.g.  sudo apt-get install libglib2.0-dev libdbus-1-dev libudev-dev libical-dev libreadline-dev

./configure

make

sudo make install

systemctl status bluetooh

sudo nano /lib/systemd/system/bluetooth.service

change the line ExecStart=...

to

ExecStart=/usr/local/libexec/bluetooth/bluetoohd --experimental
(add --experimental at the end)

sudo systemctl start bluetooth

sudo bluetoothctl

scan on
connect <MAC>

menu gatt

list-attributes
select-attribute <attribute>

e.g.
write 0x30 (write 0 in hex)