# -*- coding: utf-8 -*-
"""
DESCRIPTION

Created on November 21, 2023
"""

from typing import Optional, Union
import logging

class _TCA953x(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logFormatter = logging.Formatter("%(asctime)s  In thread %(threadName)-4.20s: %(levelname)-8.8s - %(message)s")
        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setFormatter(self.logFormatter)
        self.logger.addHandler(self.consoleHandler)
        self.logger.setLevel(logging.DEBUG)

    def bin_str_fmt(self, value):
        bin_str = bin(value)
        str_len = len(bin_str) - 2
        print_str = "0b"

        iters = range(int(str_len/4))

        for i in iters:
            print_str = print_str + " " + bin_str[((i * 4) + 2):(((i + 1) * 4) + 2)]

        return print_str

class TCA9538(_TCA953x):
    def __init__(self, address, i2c_controller = None):
        super().__init__()
        
        self.address = address
        self.bus = i2c_controller

        self.P00 = 0x01
        self.P01 = 0x02
        self.P02 = 0x04
        self.P03 = 0x08
        self.P04 = 0x10
        self.P05 = 0x20
        self.P06 = 0x40
        self.P07 = 0x80

class TCA9539(_TCA953x):
    def __init__(self, address, i2c_controller = None):
        super().__init__()

        self.address = address
        self.bus = i2c_controller

        self.ident = "TCA9539"

        self.PORT_MAP = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

        self.__PORT0_INP_REG_ADDR = 0x00
        self.__PORT1_INP_REG_ADDR = 0x01
        self.__PORT0_OUT_REG_ADDR = 0x02
        self.__PORT1_OUT_REG_ADDR = 0x03
        self.__PORT0_INV_REG_ADDR = 0x04
        self.__PORT1_INV_REG_ADDR = 0x05
        self.__PORT0_DIR_REG_ADDR = 0x06
        self.__PORT1_DIR_REG_ADDR = 0x07

        self.PORT0_DIR = 0x00
        self.PORT1_DIR = 0x00
        self.PORT0_VAL = 0xff
        self.PORT1_VAL = 0xff

        self.PIN_LUT = {
                            
                            "P00":0,
                            "P01":1,
                            "P02":2,
                            "P03":3,
                            "P04":4,
                            "P05":5,
                            "P06":6,
                            "P07":7,
                            "P10":8,
                            "P11":9,
                            "P12":10,
                            "P13":11,
                            "P14":12,
                            "P15":13,
                            "P16":14,
                            "P17":15,

                            }

        self.INPUT = 0
        self.OUTPUT = 1
        self.LOW = 0
        self.HIGH = 1

    def set_direction(self, pins : Union[int, str, list], dir : Union[int, str]):

        if (self.bus != None):
            self.bus.write([self.__PORT0_DIR_REG_ADDR])
            self.PORT0_DIR = self.bus.read(1)
            
            self.bus.write([self.__PORT1_DIR_REG_ADDR])
            self.PORT1_DIR = self.bus.read(1)

        dir = (self.PORT1_DIR << 8 ) | self.PORT0_DIR

        if (type(pins) != list):
            pins = [pins]

        for pin in pins:
            if (type(pin) == str):
                pin = self.PIN_LUT[pin]

            if (pin >= 0 and pin <= 15):
                dir = dir | (0x01 << pin)
            else:
                pass
        msg = self.ident + ".set_direction(): Setting port directions to " + self.bin_str_fmt(dir)
        self.logger.debug(msg)

        dir_bytes = dir.to_bytes(2, byteorder = "big")

        msb = dir_bytes[0]
        lsb = dir_bytes[1]

        write_bytes = []

        if (msb != self.PORT1_DIR):
            write_bytes.append(self.__PORT1_DIR_REG_ADDR)
            write_bytes.append(msb)
            self.PORT1_DIR = msb

        if (lsb != self.PORT0_DIR):
            write_bytes.append(self.__PORT0_DIR_REG_ADDR)
            write_bytes.append(lsb)
            self.PORT0_DIR = lsb

        if (self.bus != None):
            self.bus.write(write_bytes)
        else:
            return(write_bytes)
    
    def get_direction(self):
        pass

    def write_pin(self):
        pass

    def read_pin(self):
        pass

    def write_port(self):
        pass

    def read_port(self):
        pass


if __name__ == "__main__":
    dev = TCA9539(address = 0x77)
    write_val = dev.set_direction(["P00", 15], "HIGH")
    print(write_val)
