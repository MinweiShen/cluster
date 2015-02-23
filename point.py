import math

class Point(object):
	'''Define point. It can be of any dimention.
	'''
	def __str__(self):
		if self.__index == -1:
			return "Point:(" + ",".join(map(lambda x:str(x),self.__coordinates)) + ")" 
		else:
			return "Point:%d, (%s)" % (self.__index,",".join(map(lambda x:str(x),self.__coordinates)))

	def __init__(self,coordinates = None,index = -1):
		self.__dimention = None
		self.__coordinates = None
		self.__index = index
		if coordinates is None:
			self.__dimention = 0
			self.__coordinates = []
		else:
			self.__coordinates = [i for i in coordinates]
			self.__dimention = len(coordinates)


	def distance(self,p):
		'''TODO
		   Add  the distance function
		'''
		if self.__dimention != p.dimention:
			return -1
		else:
			s = 0
			for a,b in zip(self.__coordinates,p.coordinates):
				s += (a-b)**2

		return math.sqrt(s)

	def equal(self,p):
		if self.__dimention != p.dimention:
			return False
		
		for a,b in zip(self.__coordinates,p.coordinates):
			if a != b:
				return False

		return True


	@property
	def dimention(self):
		return self.__dimention

	@property
	def coordinates(self):
		return self.__coordinates[:]

	@property
	def index(self):
		return self.__index