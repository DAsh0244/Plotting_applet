#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Constants that will be drawn on for global config options"""


from collections import namedtuple
"""Constant Declarations"""
EXT = namedtuple('EXT', ['TXT', 'CSV', 'MAT'])
STYP = namedtuple('STYP', ['SERIAL', 'USB', 'NI_DAQ'])
BORD = namedtuple('BORD', ['MSB', 'LSB'])
BDPH = namedtuple('BDPH', ['FOUR', 'EIGHT', 'TEN', 'TWELVE', 'SIXTEEN', 'TWENTYFOUR', 'THIRTYTWO', 'SIXTYFOUR'])
BYTE = namedtuple('BYTE', ['FIVEBITS', 'SIXBITS', 'SEVENBITS', 'EIGHTBITS'])

"""Carried over constants for convenience use"""
from serial import FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
BYTESIZES = BYTE(FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS)


"""To be used Constants"""
EXTENSION = EXT('.txt', '.csv', '.mat')
STREAMTYPE = STYP(0, 1, 2)
BITORDER = BORD(0, 1)
BITDEPTHS = BDPH(4, 8, 10, 12, 16, 24, 32, 64)
MAXCHUNKS = 20
CHUNKSIZE = 100
BUFFERSIZE = CHUNKSIZE * 3
# BUFFERSIZE = 5
DATASIZE = CHUNKSIZE * MAXCHUNKS
WINDOWSIZE = CHUNKSIZE * 10

# del EXT,STYP,BORD,BDPH, BYTE
