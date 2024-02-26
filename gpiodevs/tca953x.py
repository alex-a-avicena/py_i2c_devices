# -*- coding: utf-8 -*-
"""
DESCRIPTION

Created on November 21, 2023
"""

from typing import Optional, Union
import logging

from pyftdi.i2c import I2cController

class _TCA953x(object):
    def __init__(self, address=None, i2c_controller=None):

        self.address = address
        self.bus = i2c_controller

        self.logger = logging.getLogger(__name__)
        self.logFormatter = logging.Formatter("%(asctime)s  In thread %(threadName)-4.20s: %(levelname)-8.8s - %(message)s")
        if not self.logger.handlers:
            self.consoleHandler = logging.StreamHandler()
            self.consoleHandler.setFormatter(self.logFormatter)
            self.logger.addHandler(self.consoleHandler)
            self.logger.setLevel(logging.DEBUG)

        self.num_ports = 0
        self.port_pins = 0

        self.INPUT = 0x01
        self.OUTPUT = 0x00
        self.LOW = 0x00
        self.HIGH = 0x01

        self.PORT_MAP = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

        self.PORT0_INP_REG_ADDR = 0x00
        self.PORT1_INP_REG_ADDR = 0x00
        self.PORT0_OUT_REG_ADDR = 0x00
        self.PORT1_OUT_REG_ADDR = 0x00
        self.PORT0_INV_REG_ADDR = 0x00
        self.PORT1_INV_REG_ADDR = 0x00
        self.PORT0_DIR_REG_ADDR = 0x00
        self.PORT1_DIR_REG_ADDR = 0x00
        self.PORT0_SPECIAL_FUNC = 0x00

        self.PORT0_DIR = 0xff
        self.PORT1_DIR = 0xff
        self.PORT0_VAL = 0x00
        self.PORT1_VAL = 0x00


        self.PIN_LUT_FOUR_PIN    = {
                            
                                    "P00":0,
                                    "P01":1,
                                    "P02":2,
                                    "P03":3

                                    }

        self.PIN_LUT_SINGLE_PORT = {
                            
                                    "P00":0,
                                    "P01":1,
                                    "P02":2,
                                    "P03":3,
                                    "P04":4,
                                    "P05":5,
                                    "P06":6,
                                    "P07":7

                                    }
        
        self.PIN_LUT_DOUBLE_PORT = {
                    
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

    def bin_str_fmt(self, value):
        bin_str = bin(value)
        bin_str = bin_str[2:]
        bin_str = bin_str.zfill(self.num_ports * self.port_pins)
        str_len = len(bin_str)
        print_str = "0b"

        iters = range(int(str_len/4))

        for i in iters:
            print_str = print_str + " " + bin_str[((i * 4)):(((i + 1) * 4))]

        return print_str
    
    def set_direction(self, pins : Union[int, str, list], direction : Union[int, str]):

        output = False

        if (direction == self.OUTPUT or direction == "output"):
            output = True
        elif (direction == self.INPUT or direction == "input"):
            output  = False
        else:
            msg = self.ident + ".set_direction(): port direction '" + direction + "' is not valid"
            self.logger.error(msg)
            return
            
        if (self.bus != None and self.num_ports >= 1):
            self.bus.write([self.PORT0_DIR_REG_ADDR])
            self.PORT0_DIR = self.bus.read(1)
        if (self.bus != None and self.num_ports == 2):
            self.bus.write([self.PORT1_DIR_REG_ADDR])
            self.PORT1_DIR = self.bus.read(1)

        if (self.num_ports == 2):
            dir = (self.PORT1_DIR << 8 ) | self.PORT0_DIR
        elif (self.num_ports == 1):
            dir = self.PORT0_DIR

        if (type(pins) != list):
            pins = [pins]

        for pin in pins:
            if (type(pin) == str):
                try:
                    if (self.num_ports == 1):
                        if (self.port_pins == 4):
                            pin = self.PIN_LUT_FOUR_PIN[pin]
                        else:
                            pin = self.PIN_LUT_SINGLE_PORT[pin]
                    elif (self.num_ports == 2):
                        pin = self.PIN_LUT_DOUBLE_PORT[pin]
                except KeyError:
                    msg = self.ident + ".set_direction(): pin '" + pin + "' is not valid"
                    self.logger.error(msg)
                    pin = -1

            n_pins = (self.num_ports * self.port_pins) - 1

            if (pin >= 0 and pin <= n_pins):
                if (output == True):
                    dir = dir & ~(0x01 << pin)
                else:
                    dir = dir | (0x01 << pin)

            elif (pin != -1):
                msg = self.ident + ".set_direction(): pin " + str(pin) + " is not valid"
                self.logger.error(msg)

            if (pin < 0 or pin > n_pins):
                msg = self.ident + ".set_direction(): invalid pin setting"
                self.logger.warning(msg)

        msg = self.ident + ".set_direction(): Port direction set to " + self.bin_str_fmt(dir)
        self.logger.debug(msg)

        dir_bytes = dir.to_bytes(self.num_ports, byteorder = "big")

        write_bytes = []

        if (self.num_ports == 2):
            if (dir_bytes[1] != self.PORT1_DIR):
                write_bytes.append(self.PORT1_DIR_REG_ADDR)
                write_bytes.append(dir_bytes[0])
                self.PORT1_DIR = dir_bytes[0]

            if (dir_bytes[0] != self.PORT0_DIR):
                write_bytes.append(self.PORT0_DIR_REG_ADDR)
                write_bytes.append(dir_bytes[1])
                self.PORT0_DIR = dir_bytes[1]

        else:

            if (dir_bytes[0] != self.PORT0_DIR):
                write_bytes.append(self.PORT0_DIR_REG_ADDR)
                write_bytes.append(dir_bytes[0])
                self.PORT0_DIR = dir_bytes[0]


        if (self.bus != None):
            self.bus.write(write_bytes)
        
        return(write_bytes)
    
    def get_direction(self):
        pass

    def write_pins(self, pins : Union[int, str, list], pin_setting : Union[int, str]):
        
        value = False

        if (pin_setting == self.HIGH or pin_setting == "high"):
            value = True
        elif (pin_setting == self.LOW or pin_setting == "low"):
            value  = False
        else:
            msg = self.ident + ".write_pins(): pin setting '" + pin_setting + "' is not valid"
            self.logger.error(msg)
            return
            
        if (self.bus != None and self.num_ports >= 1):
            self.bus.write([self.PORT0_OUT_REG_ADDR])
            self.PORT0_VAL = self.bus.read(1)
        if (self.bus != None and self.num_ports == 2):
            self.bus.write([self.PORT1_OUT_REG_ADDR])
            self.PORT1_VAL = self.bus.read(1)

        if (self.num_ports == 2):
            val = (self.PORT1_VAL << 8 ) | self.PORT0_VAL
        elif (self.num_ports == 1):
            val = self.PORT0_VAL

        if (type(pins) != list):
            pins = [pins]

        for pin in pins:
            if (type(pin) == str):
                try:
                    if (self.num_ports == 1):
                        if (self.port_pins == 4):
                            pin = self.PIN_LUT_FOUR_PIN[pin]
                        else:
                            pin = self.PIN_LUT_SINGLE_PORT[pin]
                    elif (self.num_ports == 2):
                        pin = self.PIN_LUT_DOUBLE_PORT[pin]
                except KeyError:
                    msg = self.ident + ".write_pins(): pin '" + pin + "' is not valid"
                    self.logger.error(msg)
                    pin = -1

            n_pins = (self.num_ports * self.port_pins) - 1

            if (pin >= 0 and pin <= n_pins):
                if (value == True):
                    val = val | (0x01 << pin)
                else:
                    val = val & ~(0x01 << pin)

            elif (pin != -1):
                msg = self.ident + ".write_pins(): pin " + str(pin) + " is not valid"
                self.logger.error(msg)

            if (pin < 0 or pin > n_pins):
                msg = self.ident + ".write_pins(): invalid pin setting"
                self.logger.warning(msg)

        msg = self.ident + ".write_pins(): Port set to " + self.bin_str_fmt(val)
        self.logger.debug(msg)

        val_bytes = val.to_bytes(self.num_ports, byteorder = "big")

        write_bytes = []

        if (self.num_ports == 2):
            if (val_bytes[1] != self.PORT1_VAL):
                write_bytes.append(self.PORT1_OUT_REG_ADDR)
                write_bytes.append(val_bytes[0])
                self.PORT1_VAL = val_bytes[0]

            if (val_bytes[0] != self.PORT0_VAL):
                write_bytes.append(self.PORT0_VAL_REG_ADDR)
                write_bytes.append(val_bytes[1])
                self.PORT0_VAL = val_bytes[1]

        else:

            if (val_bytes[0] != self.PORT0_VAL):
                write_bytes.append(self.PORT0_OUT_REG_ADDR)
                write_bytes.append(val_bytes[0])
                self.PORT0_VAL = val_bytes[0]


        if (self.bus != None):
            self.bus.write(write_bytes)
        
        return(write_bytes)

    def read_pins(self):
        pass

    def write_port(self):
        pass

    def read_port(self):
        pass
####################################################################################################################################################################################################################################################
#   4 I/O Devices   ################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################

class TCA9536(_TCA953x):
    def __init__(self, address, i2c_controller = None):
        super().__init__()

        self.num_ports = 1
        self.port_pins = 4

        self.ident = "TCA9536"

        self.PORT0_INP_REG_ADDR = 0x00
        self.PORT0_OUT_REG_ADDR = 0x01
        self.PORT0_INV_REG_ADDR = 0x02
        self.PORT0_DIR_REG_ADDR = 0x03    
        self.PORT0_SPECIAL_FUNC = 0x50

        self.PORT0_DIR = 0x0f
        self.PORT0_VAL = 0x00

class TCA9537(_TCA953x):
    def __init__(self, address, i2c_controller = None):
        super().__init__()

        self.num_ports = 1
        self.port_pins = 4

        self.ident = "TCA9536"

        self.PORT0_INP_REG_ADDR = 0x00
        self.PORT0_OUT_REG_ADDR = 0x01
        self.PORT0_INV_REG_ADDR = 0x02
        self.PORT0_DIR_REG_ADDR = 0x03    

        self.PORT0_DIR = 0x0f
        self.PORT0_VAL = 0x00

####################################################################################################################################################################################################################################################
#   8 I/O Devices   ################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################

class TCA9534(_TCA953x):
    def __init__(self, address, i2c_controller = None):
        super().__init__()

        self.num_ports = 1
        self.port_pins = 8

        self.ident = "TCA9534"

        self.PORT0_INP_REG_ADDR = 0x00
        self.PORT0_OUT_REG_ADDR = 0x01
        self.PORT0_INV_REG_ADDR = 0x02
        self.PORT0_DIR_REG_ADDR = 0x03    

class TCA9538(_TCA953x):
    def __init__(self, address, i2c_controller = None):
        super().__init__()

        self.num_ports = 1
        self.port_pins = 8

        self.ident = "TCA9538"

        self.PORT0_INP_REG_ADDR = 0x00
        self.PORT0_OUT_REG_ADDR = 0x01
        self.PORT0_INV_REG_ADDR = 0x02
        self.PORT0_DIR_REG_ADDR = 0x03

####################################################################################################################################################################################################################################################
#   16 I/O Devices   ###############################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################
class TCA9535(_TCA953x):
    """
    ADDRESS SPACE:

        0x20 : A2 = L, A1 = L, A0 = L
        0x21 : A2 = L, A1 = L, A0 = H
        0x22 : A2 = L, A1 = H, A0 = L
        0x23 : A2 = L, A1 = H, A0 = H
        0x24 : A2 = H, A1 = L, A0 = L
        0x25 : A2 = H, A1 = L, A0 = H
        0x26 : A2 = H, A1 = H, A0 = L
        0x27 : A2 = H, A1 = H, A0 = H

    """

    def __init__(self, address, i2c_controller = None):
        super().__init__(address, i2c_controller)

        self.num_ports = 2
        self.port_pins = 8
        
        self.ident = "TCA9539"

        self.PORT0_INP_REG_ADDR = 0x00
        self.PORT1_INP_REG_ADDR = 0x01
        self.PORT0_OUT_REG_ADDR = 0x02
        self.PORT1_OUT_REG_ADDR = 0x03
        self.PORT0_INV_REG_ADDR = 0x04
        self.PORT1_INV_REG_ADDR = 0x05
        self.PORT0_DIR_REG_ADDR = 0x06
        self.PORT1_DIR_REG_ADDR = 0x07

class TCA9539(_TCA953x):
    """
    ADDRESS SPACE:

        0x74 : A1 = L, A0 = L
        0x75 : A1 = L, A0 = H
        0x76 : A1 = H, A0 = L
        0x77 : A1 = H, A0 = H
    
    """
    def __init__(self, address, i2c_controller = None):
        super().__init__(address, i2c_controller)

        self.num_ports = 2
        self.port_pins = 8
        
        self.ident = "TCA9539"

        self.PORT0_INP_REG_ADDR = 0x00
        self.PORT1_INP_REG_ADDR = 0x01
        self.PORT0_OUT_REG_ADDR = 0x02
        self.PORT1_OUT_REG_ADDR = 0x03
        self.PORT0_INV_REG_ADDR = 0x04
        self.PORT1_INV_REG_ADDR = 0x05
        self.PORT0_DIR_REG_ADDR = 0x06
        self.PORT1_DIR_REG_ADDR = 0x07

####################################################################################################################################################################################################################################################
#   Example Usage   ################################################################################################################################################################################################################################
####################################################################################################################################################################################################################################################

if __name__ == "__main__":
    dev1 = TCA9538(address = 0x77)
    write_val = dev1.set_direction([0, 1, 2, 3, 4, 5, 6, 7], "output")
    print(write_val)
    write_val = dev1.set_direction([0, 2, 4, 6], dev1.INPUT)
    print(write_val)
    write_val = dev1.set_direction(["P06"], 0)
    print(write_val)

    dev2 = TCA9539(address = 0x74)
    write_val = dev2.set_direction([0, 1, 2, 3, 4, 5, 6, 7, 15], "output")
    print(write_val)
    write_val = dev2.set_direction(["P00"], dev2.INPUT)
    print(write_val)

    dev3 = TCA9536(address = 0x75)
    write_val = dev3.set_direction([0, 1, 2, 3], "output")
    write_val = dev3.set_direction(["P00"], "input")
    print(write_val)

    dev3.write_pins([0, 2], "high")
