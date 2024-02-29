# -*- coding: utf-8 -*-
"""
DESCRIPTION

Created on November 21, 2023
"""

from typing import Optional, Union
import logging

from pyftdi.i2c import I2cController

class ASD112C04(object):
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

        self.CFG_REG_0_ADDR = 0x00
        self.CFG_REG_1_ADDR = 0x01
        self.CFG_REG_2_ADDR = 0x02
        self.CFG_REG_3_ADDR = 0x03

        self.CFG_REG_0_VAL = 0x00
        self.CFG_REG_1_VAL = 0x00
        self.CFG_REG_2_VAL = 0x00
        self.CFG_REG_3_VAL = 0x00

    def configure(self):
        pass

    def begin_conversion(self):
        pass

    def reset(self):
        pass

    def readback_config(self):
        pass