 import Robot,numpy


class Begin:

	errorlib = {'connection': '''Can\'t connect to the sensor board ... \n
				There is probably an error with the following\n
				1.The wire is broken\n
				2.The Port is not found because it has beed changed or entered Wrongly eg. \'/dev/ttyACM0\'\n\n''',\
		'reconnect': 'Do you want to reconnect?[Y,n]\n',\
		'[Y,n]': 'You must enter \'y\' or \'n\'.\n press Enter for Y is the default\n',\
		'noSensor': 'The Robot is not connected to the sensor board! It will operate with out it ;)',\
		'connected': 'The Robot is succesfully connected to the board sensor :)'}
	Pin = 0
	Motor = 0
	Connect = 0
	Connection = False

	def __init__(self,clk = None,port = None,baudrate = None):
		#Overloading the constructor
		if clk is not None:
			self.Pin = Robot.Pin(clk)
		else:
			self.Pin = Robot.Pin()
		self.Motor = Robot.Motor(self.Pin)
		if port is not None:
			if baudrate is not None:
				self.Connect = Robot.Connect(self.Pin,self.Motor,port,baudrate)
			else:
				self.Connect = Robot.Connect(self.Pin,self.Motor,port)

		else:
			self.Connect = Robot.Connect(self.Pin,Self.Motor)

	def start(self):
		connected = self.Connect.connect()
		if(not connected):
			print(self.errorlib['connection'])
			print(self.errorlib['reconnect'])
			ans = self.YesNoQes()
			if(ans):
				self.start()
		elif(connected):
			print(self.errorlib['connected'])
		self.connection = self.Connect.connection
		return self.Connect.connection

	def getdata(self,autostart):
		data = 0
		if autostart is not None:
			self.start()
		data = self.Connect.getdata()
		if(data == 0 or data == -1):
			print(self.errorlib['connection'])
			print(self.errorlib['reconnect'])
			ans = self.YesNoQes()
			if(ans):
				self.start()
				if(self.Connect.connection):
					data = self.Connect.getdata()
					if(data==-1):
						getdata(1)
		self.connection = self.Connect.connection
		return data #if it is connected it will return an array 
			    #if not it will return 0 for no sensor and -1 for broken while running

	def YesNoQes(self):
		while True:
			answer = input()
			if(answer == 'n' or answer == 'N'):
				return 0
			elif(answer == 'y' or ansewr == 'Y' or answer == '\n'):
				return 1
			else:
				print(self.errorlib['[Y,n]'])
				self.YesNoQes()
