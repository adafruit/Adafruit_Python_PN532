# Raspberry Pi Minecraft Block NFC Writer
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
import sys

import Adafruit_PN532 as PN532

import mcpi_data

# Hack to make code compatible with both Python 2 and 3 (since 3 moved
# raw_input from a builtin to a different function, ugh).
try:
    input = raw_input
except NameError:
    pass


# PN532 configuration for a Raspberry Pi:
CS   = 18
MOSI = 23
MISO = 24
SCLK = 25

# Configure the key to use for writing to the MiFare card.  You probably don't
# need to change this from the default below unless you know your card has a
# different key associated with it.
CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]


# Create and initialize an instance of the PN532 class.
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()
pn532.SAM_configuration()

# Step 1, wait for card to be present.
print('Minecraft Block NFC Writer')
print('')
print('== STEP 1 =========================')
print('Place the card to be written on the PN532...')
uid = pn532.read_passive_target()
while uid is None:
    uid = pn532.read_passive_target()
print('')
print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
print('')
print('==============================================================')
print('WARNING: DO NOT REMOVE CARD FROM PN532 UNTIL FINISHED WRITING!')
print('==============================================================')
print('')

# Step 2, pick a block type.
print('== STEP 2 =========================')
print('Now pick a block type to write to the card.')
block_choice = None
while block_choice is None:
    print('')
    print('Type either L to list block types, or type the number of the desired block.')
    print('')
    choice = input('Enter choice (L or block #): ')
    print('')
    if choice.lower() == 'l':
        # Print block numbers and names.
        print('Number\tBlock name')
        print('------\t----------')
        for i, b in enumerate(mcpi_data.BLOCKS):
            block_name, block_id = b
            print('{0:>6}\t{1}'.format(i, block_name))
    else:
        # Assume a number must have been entered.
        try:
            block_choice = int(choice)
        except ValueError:
            # Something other than a number was entered.  Try again.
            print('Error! Unrecognized option.')
            continue
        # Check choice is within bounds of block numbers.
        if not (0 <= block_choice < len(mcpi_data.BLOCKS)):
            print('Error! Block number must be within 0 to {0}.'.format(len(mcpi_data.BLOCKS)-1))
            continue
# Block was chosen, look up its name and ID.
block_name, block_id = mcpi_data.BLOCKS[block_choice]
print('You chose the block type: {0}'.format(block_name))
print('')

# Get the block subtype if it has any available.
subtype_choice = None
if block_name in mcpi_data.SUBTYPES:
    print('Now pick a subtype for the block.')
    print('')
    print('Number\tSubtype')
    print('------\t-------')
    # Print all the subtypes for this block.
    block_subtypes = mcpi_data.SUBTYPES[block_name]
    for subtype_id, subtype_name in block_subtypes.items():
        print('{0:>6}\t{1}'.format(subtype_id, subtype_name))
    # Get a subtype id from the user.
    while subtype_choice is None:
        print('')
        try:
            subtype_choice = int(input('Enter subtype number: '))
        except ValueError:
            # Something other than a number was entered.  Try again.
            print('Error! Unrecognized subtype number.')
            continue
        if subtype_id not in block_subtypes:
            print('Error! Subtype number must be one shown above!')
            continue
if subtype_choice is not None:
    print('You also chose the subtype: {0}'.format(block_subtypes[subtype_choice]))
    print('')

# Confirm writing the block type.
print('== STEP 3 =========================')
print('Confirm you are ready to write to the card:')
print('Block: {0}'.format(block_name))
if subtype_choice is not None:
    print('Subtype: {0}'.format(block_subtypes[subtype_choice]))
print('')
choice = input('Confirm card write (Y or N)? ')
if choice.lower() != 'y' and choice.lower() != 'yes':
    print('Aborted!')
    sys.exit(0)
print('Writing card (DO NOT REMOVE CARD FROM PN532)...')

# Write the card!
# First authenticate block 4.
if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                               CARD_KEY):
    print('Error! Failed to authenticate block 4 with the card.')
    sys.exit(-1)
# Next build the data to write to the card.
# Format is as follows:
# - Bytes 0-3 are a header with ASCII value 'MCPI'
# - Byte 4 is the block ID byte
# - Byte 5 is 0 if block has no subtype or 1 if block has a subtype
# - Byte 6 is the subtype byte (optional, only if byte 5 is 1)
data = bytearray(16)
data[0:4] = b'MCPI'  # Header 'MCPI'
data[4]   = block_id & 0xFF
if subtype_choice is not None:
    data[5] = 1
    data[6] = subtype_choice & 0xFF
# Finally write the card.
if not pn532.mifare_classic_write_block(4, data):
    print('Error! Failed to write to the card.')
    sys.exit(-1)
print('Wrote card successfully! You may now remove the card from the PN532.')
