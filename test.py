from src import pyhog_engine_xXLarryTFVWXx as pyhog
from src.pyhog_engine_xXLarryTFVWXx import graphics

graphics.test_palette("SonicAndTails.bin")
for red in range(256):
    for blue in range(256):
        for green in range(256):
            graphics.color_to_genesis((red, green, blue))