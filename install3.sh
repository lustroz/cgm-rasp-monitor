sudo apt install bluez libbluetooth-dev pi-bluetooth
sudo apt install -y python3-dev python3-pip libfreetype6-dev libjpeg-dev
sudo sed -i "s/bluetoothd/bluetoothd -C/g" /lib/systemd/system/bluetooth.service
sudo systemctl daemon-reload 
sudo systemctl restart bluetooth
sudo systemctl enable bluetooth
sudo -H pip3 install --upgrade luma.oled
sudo pip3 install simplejson pybluez pybleno
sudo apt install fonts-lato

