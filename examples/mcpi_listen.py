# Raspberry Pi Minecraft Block NFC Listener
# Author: Tony DiCola
# Copyright (c) 2015 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import binascii
import socket
import time

import Adafruit_PN532 as PN532
import mcpi.minecraft as minecraft

import mcpi_data


# PN532 configuration for a Raspberry Pi:
CS   = 18
MOSI = 23
MISO = 24
SCLK = 25

# Configure the key to use for writing to the MiFare card.  You probably don't
# need to change this from the default below unless you know your card has a
# different key associated with it.
CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

# Number of seconds to delay after building a block.  Good for slowing down the
# update rate to prevent flooding new blocks into the world.
MAX_UPDATE_SEC = 0.5


def create_block(mc, block_id, subtype=None):
    """Build a block with the specified id and subtype under the player in the
    Minecraft world.  Subtype is optional and can be specified as None to use
    the default subtype for the block.
    """
    # Get player tile position and real position.
    ptx, pty, ptz = mc.player.getTilePos()
    px, py, pz = mc.player.getPos()
    # Create block at current player tile location.
    if subtype is None:
        mc.setBlock(ptx, pty, ptz, block_id)
    else:
        mc.setBlock(ptx, pty, ptz, block_id, subtype)
    # Move the player's real positon up one block.
    mc.player.setPos(px, py+1, pz)


# Start with no connection to the Minecraft world, instead it will be created
# as soon as a block is swiped.
mc = None

# Create and initialize an instance of the PN532 class.
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()
pn532.SAM_configuration()

print('Minecraft Block NFC Listener')
print('')
print('Waiting for MiFare card...')
while True:
    # Wait for a card to be available.
    uid = pn532.read_passive_target()
    # Try again if no card found.
    if uid is None:
        continue
    # Found a card, now try to read block 4 to detect the block type.
    print('Found card with UID 0x{0}'.format(binascii.hexlify(uid)))
    # Authenticate and read block 4.
    if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                                   CARD_KEY):
        print('Failed to authenticate with card!')
        continue
    data = pn532.mifare_classic_read_block(4)
    if data is None:
        print('Failed to read data from card!')
        continue
    # Check if card has Minecraft block data by looking for header 'MCPI'
    if data[0:4] != b'MCPI':
        print('Card is not written with Minecraft block data!')
        continue
    # Parse out the block type and subtype.
    block_id = data[4]
    has_subtype = data[5]
    subtype_id = data[6]
    # Find the block name (it's ugly to search for it, but there are less than 100).
    for block in mcpi_data.BLOCKS:
        if block[1] == block_id:
            block_name = block[0]
            break
    print('Found block!')
    print('Type: {0}'.format(block_name))
    if has_subtype:
        subtype_name = mcpi_data.SUBTYPES[block_name][subtype_id]
        print('Subtype: {0}'.format(subtype_name))
    # Try to create the block in Minecraft.
    # First check if connected to Minecraft world.
    try:
        if mc is None:
            mc = minecraft.Minecraft.create()
        create_block(mc, block_id, subtype_id if has_subtype else None)
        time.sleep(MAX_UPDATE_SEC)
    except socket.error:
        # Socket error, Minecraft probably isn't running.
        print('Could not connect to Minecraft, is the game running in a world?')
        continue
