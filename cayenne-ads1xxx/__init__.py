"""
This module provides classes for interfacing with ADS1XXX extensions.
"""
from time import sleep
from myDevices.devices.i2c import I2C
from myDevices.devices.analog import ADC
from myDevices.plugins.analog import AnalogInput
from myDevices.utils.types import signInteger


class ADS1XXX(ADC, I2C):
    """Base class for interacting with ADS1XXX extensions."""

    VALUE     = 0x00
    CONFIG    = 0x01
    LO_THRESH = 0x02
    HI_THRESH = 0x03
    
    CONFIG_STATUS_MASK  = 0x80
    CONFIG_CHANNEL_MASK = 0x70
    CONFIG_GAIN_MASK    = 0x0E
    CONFIG_MODE_MASK    = 0x01
    
    def __init__(self, slave, channel_count, resolution):
        """Initializes ADS1XXX device.

        Arguments:
        slave: The slave address
        channel_count: Number of channels on the device
        resolution: Bits of resolution
        """
        I2C.__init__(self, int(slave))
        ADC.__init__(self, channel_count, resolution, 4.096)
        self._analogMax = 2**(resolution-1)
        
        config = self.readRegisters(self.CONFIG, 2)
        
        mode = 0 # continuous
        config[0] &= ~self.CONFIG_MODE_MASK
        config[0] |= mode
        
        gain = 0x1 # FS = +/- 4.096V
        config[0] &= ~self.CONFIG_GAIN_MASK
        config[0] |= gain << 1
        
        self.writeRegisters(self.CONFIG, config)
    
    def __str__(self):
        """Returns friendly name."""
        return "%s(slave=0x%02X)" % (self.__class__.__name__, self.slave)
        
    def __analogRead__(self, channel, diff=False):
        """Read the analog input. Overrides ADC.__analogRead__.

        channel: Channel on the device
        diff: True if using differential input
        """
        config = self.readRegisters(self.CONFIG, 2)
        config[0] &= ~self.CONFIG_CHANNEL_MASK
        if diff:
            config[0] |= channel << 4
        else:
            config[0] |= (channel + 4) << 4
        self.writeRegisters(self.CONFIG, config)
        sleep(0.001)
        d = self.readRegisters(self.VALUE, 2)
        value = (d[0] << 8 | d[1]) >> (16-self._analogResolution)
        return signInteger(value, self._analogResolution)


class ADS1014(ADS1XXX):
    """Class for interacting with a ADS1014 device."""

    def __init__(self, slave=0x48):
        """Initializes ADS1014 device.

        Arguments:
        slave: The slave address
        """
        ADS1XXX.__init__(self, slave, 1, 12)

class ADS1015(ADS1XXX):
    """Class for interacting with a ADS1015 device."""

    def __init__(self, slave=0x48):
        """Initializes ADS1015 device.

        Arguments:
        slave: The slave address
        """
        ADS1XXX.__init__(self, slave, 4, 12)

class ADS1114(ADS1XXX):
    """Class for interacting with a ADS1114 device."""

    def __init__(self, slave=0x48):
        """Initializes ADS1114 device.

        Arguments:
        slave: The slave address
        """
        ADS1XXX.__init__(self, slave, 1, 16)

class ADS1115(ADS1XXX):
    """Class for interacting with a ADS1115 device."""

    def __init__(self, slave=0x48):
        """Initializes ADS1115 device.

        Arguments:
        slave: The slave address
        """
        ADS1XXX.__init__(self, slave, 4, 16)

class ADSTest(ADS1XXX):
    """Class for simulating an ADS1115 device."""

    def __init__(self):
        """Initializes the test class."""
        self.registers = {}
        ADS1115.__init__(self)

    def readRegister(self, addr):
        """Read value from a register."""
        if addr not in self.registers:
            self.registers[addr] = 0
        return self.registers[addr]

    def readRegisters(self, addr, size):
        """Read value from a register."""
        if addr not in self.registers:
            self.registers[addr] = bytearray(size)
        return self.registers[addr]

    def writeRegister(self, addr, value):
        """Write value to a register."""
        self.registers[addr] = value

    def writeRegisters(self, addr, value):
        """Write value to a register."""
        self.registers[addr] = value        