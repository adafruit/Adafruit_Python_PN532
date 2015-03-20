Adafruit Python PN532
=====================

Python library for accessing a PN532 NFC breakout over a SPI connection from a Raspberry Pi, BeagleBone Black, etc.

Designed specifically to work with the Adafruit PN532 breakout using a SPI connection ----> https://www.adafruit.com/product/364

Installation
------------

To install the library make sure your device is connected to the internet (with a wired or wireless connection), then
connect to the device's terminal and run the following commands (assuming a Debian-based operating system like
Raspbian, Debian, Ubuntu, etc.):

```
sudo apt-get update
sudo apt-get install build-essential python-dev git
git clone https://github.com/adafruit/Adafruit_Python_PN532.git
cd Adafruit_Python_PN532
sudo python setup.py install
```

Look inside the examples directory for a simple example of detecting and reading a MiFare classic card with readmifare.py.
Make sure to run examples as root using sudo, for example:

```
sudo python readmifare.py
```

Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!

Written by Tony DiCola for Adafruit Industries.
MIT license, all text above must be included in any redistribution
