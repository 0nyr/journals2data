# gecko is a driver for Selenium so as to run Firefox in headless
# mode.

# [1: install geckodriver]
echo "This will install geckodriver-v0.29.1-linux64
maybe you should download a newer version of geckodriver
GitHub: https://github.com/mozilla/geckodriver/releases"

# variables
URL=https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz

# delete if already exist
sudo rm -rf /opt/geckodriver/geckodriver-v0.29.1-linux64
sudo rm /usr/local/bin/geckodriver

# get file from GitHub, extract it and create command shortcut
sudo mkdir -p /opt/geckodriver/geckodriver-v0.29.1-linux64
wget $URL
chmod 775 geckodriver-v0.29.1-linux64.tar.gz
sudo tar -xvf geckodriver-v0.29.1-linux64.tar.gz -C /opt/geckodriver/geckodriver-v0.29.1-linux64/
ls -alt /opt/geckodriver/geckodriver-v0.29.1-linux64/

# create command shortcut
sudo ln -s /opt/geckodriver/geckodriver-v0.29.1-linux64/geckodriver /usr/local/bin/geckodriver

# delete archive
rm geckodriver-v0.29.1-linux64.tar.gz


exit 0