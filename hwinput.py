from RPi import I2C as i2c

class HwInput(object):

	def __init__(self):
		i2c.init("/dev/i2c-1")

	def readPots(self):
		i2c.open(0x4c)
		i2c.write([0x40])
		i2c.read(1)
		input0 = i2c.read(1)
		i2c.write([0x41])
		i2c.read(1)
		input1 = i2c.read(1)
		i2c.write([0x42])
		i2c.read(1)
		input2 = i2c.read(1)
		i2c.write([0x43])
		i2c.read(1)
    		input3 = i2c.read(1)
		i2c.close()
		return [float(input2[0])/255, float(input1[0])/255, float(input0[0])/255]