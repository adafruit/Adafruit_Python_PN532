# Raspberry Pi Minecraft Block NFC Data
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

# List of tuples with block names and types.
# This is taken from the list at:
#   http://www.stuffaboutcode.com/p/minecraft-api-reference.html
BLOCKS = [
    ('Air'                , 0),
    ('Bed'                , 26),
    ('Bedrock'            , 7),
    ('Bedrock, invisible' , 95),
    ('Bookshelf'          , 47),
    ('Brick block'        , 45),
    ('Cactus'             , 81),
    ('Chest'              , 54),
    ('Clay'               , 82),
    ('Coal ore'           , 16),
    ('Cobweb'             , 30),
    ('Cobblestone'        , 4),
    ('Crafting table'     , 58),
    ('Diamond ore'        , 56),
    ('Diamond block'      , 57),
    ('Dirt'               , 3),
    ('Door, iron'         , 71),
    ('Door, wood'         , 64),
    ('Farmland'           , 60),
    ('Fence'              , 85),
    ('Fence gate'         , 107),
    ('Fire'               , 51),
    ('Flower, yellow'     , 37),
    ('Flower, cyan'       , 38),
    ('Furnace, inactive'  , 61),
    ('Furnace, active'    , 62),
    ('Glowstone block'    , 89),
    ('Gold block'         , 41),
    ('Gold ore'           , 14),
    ('Glass'              , 20),
    ('Grass'              , 2),
    ('Grass, tall'        , 31),
    ('Glass pane'         , 102),
    ('Glowing obsidian'   , 246),
    ('Gravel'             , 13),
    ('Ice'                , 79),
    ('Iron block'         , 42),
    ('Iron ore'           , 15),
    ('Ladder'             , 65),
    ('Lapis lazuli ore'   , 21),
    ('Lapis lazuli block' , 22),
    ('Lava, flowing'      , 10),
    ('Lava, stationary'   , 11),
    ('Leaves'             , 18),
    ('Melon'              , 103),
    ('Moss stone'         , 48),
    ('Mushroom, brown'    , 39),
    ('Mushroom, red'      , 40),
    ('Nether reactor core', 247),
    ('Obsidian'           , 49),
    ('Redstone ore'       , 73),
    ('Sand'               , 12),
    ('Sandstone'          , 24),
    ('Sapling'            , 6),
    ('Snow'               , 78),
    ('Snow block'         , 80),
    ('Stairs, wood'       , 53),
    ('Stairs, cobblestone', 67),
    ('Stone'              , 1),
    ('Stone, brick'       , 98),
    ('Stone slab'         , 44),
    ('Stone slab, double' , 43),
    ('Sugar cane'         , 83),
    ('Torch'              , 50),
    ('TNT'                , 46),
    ('Water, flowing'     , 8),
    ('Water, stationary'  , 9),
    ('Wood'               , 17),
    ('Wood planks'        , 5),
    ('Wool'               , 35)
]

# Mapping of block types to possible subtypes.
# The key of each item is the block name and the value is a list of tuples with
# the subtype value and name.  Again this is taken from the same source as the
# block list above.
SUBTYPES = {
    'Stone': {
        0: 'White',
        1: 'Orange',
        2: 'Magenta',
        3: 'Light Blue',
        4: 'Yellow',
        5: 'Lime',
        6: 'Pink',
        7: 'Grey',
        8: 'Light grey',
        9: 'Cyan',
        10: 'Purple',
        11: 'Blue',
        12: 'Brown',
        13: 'Green',
        14: 'Red',
        15: 'Black'
    },
    'Wood': {
        0: 'Oak',
        1: 'Spruce',
        2: 'Birch'
    },
    'Sapling': {
        0: 'Oak',
        1: 'Spruce',
        2: 'Birch'
    },
    'Grass, tall': {
        0: 'Shrub',
        1: 'Grass',
        2: 'Fern'
    },
    'Torch': {
        1: 'Pointing east',
        2: 'Pointing west',
        3: 'Pointing south',
        4: 'Pointing north',
        5: 'Facing up'
    },
    'Stone, brick': {
        0: 'Stone brick',
        1: 'Mossy stone brick',
        2: 'Cracked stone brick',
        3: 'Chiseled stone brick'
    },
    'Stone slab': {
        0: 'Stone',
        1: 'Sandstone',
        2: 'Wooden',
        3: 'Cobblestone',
        4: 'Brick',
        5: 'Stone Brick'
    },
    'Stone slab, double': {
        0: 'Stone',
        1: 'Sandstone',
        2: 'Wooden',
        3: 'Cobblestone',
        4: 'Brick',
        5: 'Stone Brick'
    },
    'TNT': { 
        0: 'Inactive',
        1: 'Ready to explode'
    },
    'Leaves': {
        1: 'Oak leaves',
        2: 'Spruce leaves',
        3: 'Birch leaves'
    },
    'Sandstone': {
        0: 'Sandstone',
        1: 'Chiseled sandstone',
        2: 'Smooth sandstone'
    },
    'Stairs, wood': {
        0: 'Ascending east',
        1: 'Ascending west',
        2: 'Ascending south',
        3: 'Ascending north',
        4: 'Ascending east (upside down)',
        5: 'Ascending west (upside down)',
        6: 'Ascending south (upside down)',
        7: 'Ascending north (upside down)'
    },
    'Stairs, cobblestone': {
        0: 'Ascending east',
        1: 'Ascending west',
        2: 'Ascending south',
        3: 'Ascending north',
        4: 'Ascending east (upside down)',
        5: 'Ascending west (upside down)',
        6: 'Ascending south (upside down)',
        7: 'Ascending north (upside down)'
    },
    'Ladder': {
        2: 'Facing north',
        3: 'Facing south',
        4: 'Facing west',
        5: 'Facing east'
    },
    'Chest': {
        2: 'Facing north',
        3: 'Facing south',
        4: 'Facing west',
        5: 'Facing east'
    },
    'Furnace, inactive': {
        2: 'Facing north',
        3: 'Facing south',
        4: 'Facing west',
        5: 'Facing east'
    },
    'Furnace, active': {
        2: 'Facing north',
        3: 'Facing south',
        4: 'Facing west',
        5: 'Facing east'
    },
    'Water, stationary': {
        0: 'Level 0 (highest)',
        1: 'Level 1',
        2: 'Level 2',
        3: 'Level 3',
        4: 'Level 4',
        5: 'Level 5',
        6: 'Level 6',
        7: 'Level 7 (lowest)'
    },
    'Lava, stationary': {
        0: 'Level 0 (highest)',
        1: 'Level 1',
        2: 'Level 2',
        3: 'Level 3',
        4: 'Level 4',
        5: 'Level 5',
        6: 'Level 6',
        7: 'Level 7 (lowest)'
    },
    'Nether reactor core': {
        0: 'Unused',
        1: 'Active',
        2: 'Stopped / used up'
    }
}
