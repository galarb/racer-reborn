from lcd_api import LcdApi
from time import sleep_ms

class I2cLcd(LcdApi):
    def __init__(self, i2c, addr, num_lines, num_columns):
        self.i2c = i2c
        self.addr = addr
        self.backlight = 0x08

        sleep_ms(20)

        # init sequence
        self._write4(0x03)
        sleep_ms(5)
        self._write4(0x03)
        sleep_ms(5)
        self._write4(0x03)
        sleep_ms(1)
        self._write4(0x02)

        super().__init__(num_lines, num_columns)

        self.write_cmd(0x28)  # 4-bit, 2 line
        self.write_cmd(0x0C)  # display on
        self.write_cmd(0x06)  # entry mode
        self.clear()

    def _write4(self, data):
        self._expander_write(data << 4)
        self._pulse(data << 4)

    def _expander_write(self, data):
        self.i2c.writeto(self.addr, bytes([data | self.backlight]))

    def _pulse(self, data):
        self._expander_write(data | 0x04)
        self._expander_write(data & ~0x04)

    def write_cmd(self, cmd):
        self._write4(cmd >> 4)
        self._write4(cmd & 0x0F)

    def write_data(self, data):
        self._write4((data >> 4) | 0x01)
        self._write4((data & 0x0F) | 0x01)
