from neopixel import NeoPixel
import time

class SmartNeoPixel:

    def __init__(self, pin, n, brightness=1.0):
        self.np = NeoPixel(pin, n)
        self.n = n
        self.brightness = brightness

    def set_brightness(self, brightness):
        self.brightness = max(0, min(1, brightness))

    def _apply_brightness(self, r, g, b):
        r = int(r * self.brightness)
        g = int(g * self.brightness)
        b = int(b * self.brightness)
        return r, g, b

    def set_pixel(self, i, color):
        r, g, b = color
        r, g, b = self._apply_brightness(r, g, b)

        self.np[i] = (r, g, b)

    def fill(self, color):
        for i in range(self.n):
            self.set_pixel(i, color)

    def write(self):
        self.np.write()

    def set_color(self, i, r, g, b):
        r, g, b = self._apply_brightness(r, g, b)

        # swap R and G if your LEDs require GRB order
        self.np[i] = (g, r, b)

    def blink_idle(self):

        # first state
        self.set_color(0, 255, 0, 0)   # Red
        self.set_color(1, 0, 255, 0)   # Green
        self.write()

        time.sleep(0.5)

        # swapped state
        self.set_color(0, 0, 255, 0)   # Green
        self.set_color(1, 255, 0, 0)   # Red
        self.write()

        time.sleep(0.5)
