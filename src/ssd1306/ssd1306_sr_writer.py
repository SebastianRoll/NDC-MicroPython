import machine
from ssd1306 import SSD1306_SPI, SSD1306_I2C
from writer import Writer

# Fonts
import freesans20
#import freeserif19
#import inconsolata16
WIDTH = const(128)
HEIGHT = const(32)

class SSD1306_SR():
	def __init__(self, pin_scl=22, pin_sda=23, width=128, height=32):
		# I2C
		pscl = machine.Pin(pin_scl, machine.Pin.OUT)
		psda = machine.Pin(pin_sda, machine.Pin.OUT)
		i2c = machine.I2C(scl=pscl, sda=psda)
		#    i2c = machine.I2C(2)
		ssd = SSD1306_I2C(WIDTH, HEIGHT, i2c)

		rhs = WIDTH -1
		ssd.line(rhs - 20, 0, rhs, 20, 1)
		square_side = 10
		ssd.fill_rect(rhs - square_side, 0, square_side, square_side, 1)
		self.wri2 = Writer(ssd, freesans20, verbose=False)
		#Writer.set_clip(True, True)
		Writer.set_textpos(0, 0)
		self.ssd = ssd

	def display(self, msg):
		#Writer.set_clip(True, True)
		self.ssd.fill_rect(0, 0, WIDTH, HEIGHT, 0)
		Writer.set_textpos(0, 0)
		#for msg in messages:
		#	print("MSG: ", msg)
		#	self.wri2.printstring(msg + '\n')
		self.wri2.printstring(msg)
		self.ssd.show()
