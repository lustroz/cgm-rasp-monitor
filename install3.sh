sudo apt install -y python3-dev libffi-dev libssl-dev python3-pip libfreetype6-dev libjpeg-dev bluez libbluetooth-dev pi-bluetooth
sudo -H pip3 install --upgrade luma.oled
sudo pip3 install simplejson pybluez pybleno
sudo pip3 install python-telegram-bot --upgrade --default-timeout=100
sudo apt install fonts-lato
sudo sed -i "s/bluetoothd/bluetoothd -C/g" /lib/systemd/system/bluetooth.service
sudo systemctl daemon-reload 
sudo systemctl restart bluetooth
sudo systemctl enable bluetooth

