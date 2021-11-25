
install gtts
pip3 install gtts

install playsound
pip3 install playsound

install PyQT5

apt-get install python3-pyqt5

instal escpos

pip3 install python-escpos

install dotenv

pip3 install python-dotenv


LCD SHOW

https://www.waveshare.com/wiki/3.5inch_RPi_LCD_(A)

Screen orientation settings
After touch driver is installed, the screen orientation can be set by these commands:

0 degree rotation
cd LCD-show/
./LCD35-show 0
90 degree rotation
cd LCD-show/
./LCD35-show 90
180 degree rotation
cd LCD-show/
./LCD35-show 180
270 degree rotation
cd LCD-show/
./LCD35-show 270


Touch screen calibration
This LCD can be calibrated through the xinput-calibrator program. Note: The Raspberry Pi must be connected to the network, or else the program won't be successfully installed.

Run the following command to install:
sudo apt-get install xinput-calibrator 
Click the "Menu" button on the taskbar, choose "Preference" -> "Calibrate Touchscreen".
Finish the touch calibration following the prompts. Maybe rebooting is required to make calibration active.
You can create a 99-calibration.conf file to save the touch parameters (not necessary if file exists).
sudo mkdir /etc/X11/xorg.conf.d
sudo nano /etc/X11/xorg.conf.d/99-calibration.conf
Save the touch parameters (may differ depending on LCD) to 99-calibration.conf, as shown in the picture:
5inch HDMI LCD FAQ1.jpg

Press the keys Ctrl+X, and select option Y to save the modification.
The modification will be valid after rebooting the system. Enter the following command for system reboot:
sudo reboot


Install Virtual Keyabord
1. Install matchbox-keyboard
sudo apt-get install update
sudo apt-get install matchbox-keyboard
sudo nano /usr/bin/toggle-matchbox-keyboard.sh
2. Copy the statements below to toggle-matchbox-keyboard.sh and save.

#!/bin/bash
#This script toggle the virtual keyboard
PID=`pidof matchbox-keyboard`
if [ ! -e $PID ]; then
killall matchbox-keyboard
else
matchbox-keyboard -s 50 extended&
fi
3. Execute the commands:

sudo chmod +x /usr/bin/toggle-matchbox-keyboard.sh
sudo mkdir /usr/local/share/applications
sudo nano /usr/local/share/applications/toggle-matchbox-keyboard.desktop
4. Copy the statements to toggle-matchbox-keyboard.desktop and save.

[Desktop Entry]
Name=Toggle Matchbox Keyboard
Comment=Toggle Matchbox Keyboard`
Exec=toggle-matchbox-keyboard.sh
Type=Application
Icon=matchbox-keyboard.png
Categories=Panel;Utility;MB
X-MB-INPUT-MECHANSIM=True
5. Execute commands as below. Note that you need to use "Pi " user permission instead of root to execute this command

nano ~/.config/lxpanel/LXDE-pi/panels/panel
6. Find the statement which is similar to below: (It maybe different in different version)

Plugin {
type = launchbar
Config {
Button {
id=lxde-screenlock.desktop
}
Button {
id=lxde-logout.desktop
}
}
7. Append these statements to add an button option:

Button {
id=/usr/local/share/applications/toggle-matchbox-keyboard.desktop
}
RPILCD-INSTALL-KEYBOARD01.png
8. reboot your Raspberry Pi. If the virtual keyboard is installed correctly, you can find that there is a keyboard icon on the left of the bar

sudo reboot
