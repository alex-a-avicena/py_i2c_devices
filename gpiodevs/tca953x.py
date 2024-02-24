# -*- coding: utf-8 -*-
"""
DESCRIPTION

Created on November 21, 2023
"""

from typing import Optional, Union

class TCA9538():
    def __init__(self, address, i2c_controller):
        pass

class TCA9539():
    def __init__(self, address, i2c_controller):

        self.address = address

        self.P00 = 0x01
        self.P01 = 0x02
        self.P02 = 0x04
        self.P03 = 0x08
        self.P04 = 0x10
        self.P05 = 0x20
        self.P06 = 0x40
        self.P07 = 0x80

        self.P10 = 0x01
        self.P11 = 0x02
        self.P12 = 0x04
        self.P13 = 0x08
        self.P14 = 0x10
        self.P15 = 0x20
        self.P16 = 0x40
        self.P17 = 0x80

        self.__PORT0_INP_REG = 0x00
        self.__PORT1_INP_REG = 0x01
        self.__PORT0_OUT_REG = 0x02
        self.__PORT1_OUT_REG = 0x03
        self.__PORT0_INV_REG = 0x04
        self.__PORT1_INV_REG = 0x05
        self.__PORT0_DIR_REG = 0x06
        self.__PORT1_DIR_REG = 0x07

        self.pin_lut_str = {
                            
                            "P00":self.P00,
                            "P01":self.P01,
                            "P02":self.P02,
                            "P03":self.P03,
                            "P04":self.P04,
                            "P05":self.P05,
                            "P06":self.P06,
                            "P07":self.P07,
                            "P10":self.P10,
                            "P11":self.P11,
                            "P12":self.P12,
                            "P13":self.P13,
                            "P14":self.P14,
                            "P15":self.P15,
                            "P16":self.P16,
                            "P17":self.P17,

                            }

        self.INPUT = 0
        self.OUTPUT = 1
        self.LOW = 0
        self.HIGH = 1

    def set_direction(self, pins : Union[int, str, list], dir : Union[int, str]):

        reg_value = 0x00

        if (type(pins) != list):
            pins = [pins]
        
        for pin in pins:
            if (type(pin) == str):
                pin  = self.pin_lut_str[pin]
            reg_value = reg_value | pin

        print(bin(reg_value))
    
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
    dev = TCA9539(i2c_address = 0x77)
    dev.set_direction(["P00", dev.P01, 0x04], "HIGH")
