import threading
import sys
import os

TERMINAL_WIDTH=os.get_terminal_size()[0]

def non_blocking(func):
	def wrapper(*args, **kwargs):
		thread = threading.Thread(target=func, args=args, kwargs=kwargs)
		thread.start()
		return thread
	return wrapper

class TemplateProgress:

	def __init__(self, filled, unfilled, msg=""):
		self.width = TERMINAL_WIDTH
		self._value = 0

		self.msg = msg.strip() + ' '

		self.__UNFILLED_CHAR = unfilled
		self.__FILL_CHAR = filled

		self.width -= len(self.msg)

		self.__percentage = f" {self._value}/{self.width}"
		self.width -= len(self.__percentage)
  
		self.__format = f"{self.msg}[{self.__FILL_CHAR * self._value + self.__UNFILLED_CHAR * (self.width - self._value)}]{self.__percentage}"
		
  
	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, val):
		if val > self.width:
			val = self.width
		self._value = val

	def print(self, msg):
		sys.stdout.write("\r")
		sys.stdout.write(' ' * len(self.__format))
		sys.stdout.write("\r")

		print(msg)
		self.render()

	def render(self):
		self.__percentage = f""
		self.__format = f"{self.msg}[{self.__FILL_CHAR * self._value + self.__UNFILLED_CHAR * (self.width - self._value)}]{self.__percentage}"
  
		print(self.__format,sep="", end="\r")

	def update(self, val):
		self.value = val
		self.render()

class FixedProgress(TemplateProgress):
	def __init__(self, width, chars=("#",".")):
		super().__init__(chars[0], chars[1])
		self.width = width

class Progress(TemplateProgress):
    def __init__(self, chars=("#",".")):
        super().__init__(chars[0], chars[1])