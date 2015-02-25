import math

def Euclidean_distance(p1,p2):
	""" Return the Euclidean distance

	Args:
		p1 (Point): first point.
		p2 (Point): second point.

	Returns:
		float: the Euclidean distance between points. 
	"""
	if p1.dimention != p2.dimention:
		return -1

	s = 0
	for a,b in zip(p1.coordinates,p2.coordinates):
		s += (a-b)**2

	return math.sqrt(s)


class Point(object):
	""" Point is the basic element is the cluster.
	"""
	def __str__(self):
		if self.__index == -1:
			return "Point:(" + ",".join(map(lambda x:str(x),self.__coordinates)) + ")" 
		else:
			return "Point:%d, (%s)" % (self.__index,",".join(map(lambda x:str(x),self.__coordinates)))

	def __init__(self,coordinates,index = -1,distance_function = Euclidean_distance):
		""" Init a point instance.

		Args:
			coordinates (list): a list of coordinates.
			index (int, optional): the index of the point.
			distance_function (function, optional): the distance function used to determine the distance_function
													between 2 points.

		Attributes:
			__coordinates (list): a list of coordinates.
			__coordinates (int): the dimention of the point.
			__index (int): the index of the point
			__distance_function (function): distance function, the default is Euclidean distance
		"""

		self.__coordinates = coordinates
		self.__dimention = len(coordinates)
		self.__index = index
		self.__distance_function = distance_function

	def distance(self,p):
		""" Return the distance from Point p.

		Args:
			p (Point): another point.
			distance_function (function,optional): distance_function, default uses the Euclidean distance.

		Returns:
			float: the distance between self and p.
		"""
		return self.__distance_function(self,p)

	def equal(self,p):
		""" Check if the p is the same as self.

		Args:
			p (Point): another point.

		Returns:
			bool: True if the are the same, otherwise False.
		"""
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