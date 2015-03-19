from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name              = 'Adafruit_PN532',
      version           = '1.0.0',
      author            = 'Tony DiCola',
      author_email      = 'tdicola@adafruit.com',
      description       = 'Python library for accessing a PN532 NFC breakout over a SPI connection from a Raspberry Pi, BeagleBone Black, etc.',
      license           = 'MIT',
      url               = 'https://github.com/adafruit/Adafruit_Python_PN532/',
      dependency_links  = ['https://github.com/adafruit/Adafruit_Python_GPIO/tarball/master#egg=Adafruit-GPIO-0.9'],
      install_requires  = ['Adafruit-GPIO>=0.9'],
      packages          = find_packages())
