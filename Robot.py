import RPi.GPIO as GPIO
import time,serial

#Setting up GPIO mode
GPIO.setmode(GPIO.BOARD)
class Pin:
	errolib = {'pin': 'This pin is either not setuped or can not been changed',\
		'getdata': 'The connection to the sensor suddenly lost'}
	pinlib = {'pwmRght' : 12,\
		'FrRght' : 16,\
		'RvRght': 18,\
		'FrLft': 22,\
		'RvLft': 24,\
		'pwmLft': 26,\
		'Trg': 32}
	clk = 500
	pwmRght = 0
	pwmLft = 0

	def __init__(self,clk = None):
		#Sensor Trigger pin
		GPIO.setup(self.pinlib['Trg'],GPIO.OUT)	#sensetive to rising edge and will write data on serial
		#Right Motor pins
		GPIO.setup(self.pinlib['pwmRght'],GPIO.OUT)		#PWM pin
		GPIO.setup(self.pinlib['FrRght'],GPIO.OUT)
		GPIO.setup(self.pinlib['RvRght'],GPIO.OUT)
		#Left Motor pins
		GPIO.setup(self.pinlib['pwmLft'],GPIO.OUT)		#PWM pin
		GPIO.setup(self.pinlib['FrLft'],GPIO.OUT)
		GPIO.setup(self.pinlib['RvLft'],GPIO.OUT)
		#Make no move in the begining
		self.pin('FrRght',0)
		self.pin('RvRght',0)
		self.pin('FrLft',0)
		self.pin('RvLft',0)
		#Overloading the constructor
		if(clk is not None):
			self.clk = clk
		#Setting PWM
		self.pwmRght = GPIO.PWM(self.pinlib['pwmRght'],self.clk)
		self.pwmLft = GPIO.PWM(self.pinlib['pwmLft'],self.clk)
		#Starting PWM
		self.pwmRght.start(0)
		self.pwmLft.start(0)

	def __del__(slef):
		GPIO.cleanup()

	def pin(self,pin,status):
		if(pin=="pwmRght" or pin=="redLED"):
			try:
				self.pwmRght.ChangeDutyCycle(abs(status))
			except:
				print(self.errorlib['pin'])
		elif(pin=="pwmLft" or pin=="blueLED"):
			try:
				self.pwmLft.ChangeDutyCycle(abs(status))
			except:
				print(self.errorlib['pin'])

		elif(status==1):
			try:
				GPIO.output(self.pinlib[pin],GPIO.HIGH)
			except:
				print(self.errorlib['pin'])
		elif(status==0):
			try:
				GPIO.output(self.pinlib[pin],GPIO.LOW)
			except:
				print(self.errorlib['pin'])




	def blink(self,delay,LED,LED2 = None,cross= None):
		self.pin('FrRght',0)
		self.pin('RvRght',0)
		self.pin('FrLft',0)
		self.pin('RvLft',0)
		if (LED2 is None):
			self.pin(LED,100)
			time.sleep(delay/2)
			self.pin(LED,0)
			time.sleep(delay/2)
		if ((LED2 is not None) and (cross is None) ):
			self.pin(LED,100)
			self.pin(LED2,100)
			time.sleep(delay/2)
			self.pin(LED,0)
			self.pin(LED2,0)
			time.sleep(delay/2)
		if((cross is not None) and (cross is not None) and cross):
			self.pin(LED,100)
			self.pin(LED2,0)
			time.sleep(delay/2)
			self.pin(LED,0)
			self.pin(LED2,100)
			time.sleep(delay/2)
			self.pin(LED,0)
			self.pin(LED2,0)





class Motor:
	Pin = 0
	def __init__(self,Pin):
		self.Pin = Pin

	def speed(self,spdRght,spdLft,stop = None):
		if(stop is not None):
			self.Pin.pin('pwmRght',0)	#Right STOP
			self.Pin.pin('FrRght',1)
			self.Pin.pin('RvRght',1)
			self.Pin.pin('pwmLft',0)		#Left STOP
			self.Pin.pin('FrLft',1)
			self.Pin.pin('RvLft',1)
			return

		#protecting from over voltage!!!
		if(abs(spdRght)>100):
			spdRght = 100*spdRght/abs(spdRght)
		if(abs(spdLft)>100):
			spdLft = 100*spdLft/abs(spdLft)

		#setting Right motor pwm
		if(spdRght>0):
			self.Pin.pin('FrRght',1)		#RIGHT Straight
			self.Pin.pin('RvRght',0)
			self.Pin.pin('pwmRght',spdRght)
		else:
			self.Pin.pin('FrRght',0)		#RIGHT revers
			self.Pin.pin('RvRght',1)
			self.Pin.pin('pwmRght',abs(spdRght))

		#setting Left motor pwm
		if(spdLft>0):
			self.Pin.pin('FrLft',1)	#Left Straight
			self.Pin.pin('RvLft',0)
			self.Pin.pin('pwmLft',spdLft)
		else:
			self.Pin.pin('FrLft',0)		#Left revers
			self.Pin.pin('RvLft',1)
			self.Pin.pin('pwmLft',abs(spdLft))



class Connect:

	port = "/dev/ttyACM0"
	baudrate = 9600
	myser = 0
	Pin = 0
	Motor = 0
	connection = False

	def __init__(self,Pin,Motor,port = None,baudrate = None):
		if(port is not None):
			self.port = port
		if(baudrate is not None):
			self.baudrate = baudrate
		self.Pin = Pin
		self.Motor = Motor

	def __del__(self):
		if(self.connection):
			try:
				self.myser.close()
			except:
				print("The connection to seensors was Lost!!!")
	def getdata(self):

		#Trigerring sensors to get data
		self.Pin.blink(.0001,'Trg')		#Setting pin HIGH for 50u

		#data = {USonic 1,Usonic 2,Usonic 3,Usonic 4,Usonic 5,EncoderRight,EncoderLeft}
		data = [-1,-1,-1,-1,-1,.5,.5]
		if self.connection:
			try:					#Try if connection is still ok
				for i in range(0,7):
					temp = self.myser.readline()
					data[i] = int(temp.decode('utf-8'))
				return data
			except:
				print(errolib['getdata'])
				return -1
		else:
			return 0

	def connect(self):
		self.Motor.speed(0,0,1)
		try:
			self.myser.close()
		except:
			for i in range(0,6):
				self.Pin.blink(.75,'blueLED')
		try:
			self.myser = serial.Serial(self.port,self.baudrate)
			self.connection = True
			return self.connection
		except:
			for i in range(0,60):
				self.Pin.blink(0.25,'redLED')
			try:
				self.myser = serial.Serial(self.port,self.baudrate)
				self.connection = True
				for i in range(0, 4):
					self.Pin.blink(1,'redLED','blueLED')
				return self.connection
			except:
				connection = False
				for i in range(0, 4):
					self.Pin.blink(1,'redLED','blueLED',1)
				self.connection = False
				return self.connection
