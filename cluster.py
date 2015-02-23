from point import *

DISTANCE_MAX = 1
DISTANCE_MIN = 2
DISTANCE_MEAN_CENTER= 3

class Cluster(object):
	'''Define cluster. This contains points.
	'''
	def __str__(self):
		return "The cluster is of size %d\n" % self.__size


	def __init__(self,points = None):
		self.__points = []
		self.__size = 0
		self.__center = None

		if points is not None:
			self.__points = points[:]
			self.__size = len(points)

			m = [0 for i in self.__points[0].coordinates]
			for p in self.__points:
				coordinates = p.coordinates
				for i in xrange(len(coordinates)):
					m[i] += coordinates[i]
			m = map(lambda x:x/self.__size,m)
			self.__center = Point(m)


	def union(self,c,update_center=True):
		'''union two clusters. combine their points. 
		   update count and center
		'''
		self.__points += c.points
		self.__size += len(c.points)
		if update_center:
			m = [0 for i in self.__points[0].coordinates]
			for p in self.__points:
				coordinates = p.coordinates
				for i in xrange(len(coordinates)):
					m[i] += coordinates[i]
			m = map(lambda x:x/self.__size,m)
			self.__center = Point(m)

	def add_points(self,points,update_center=True):
		self.__points += points
		self.__size += len(points)
		if update_center:
			m = [0 for i in self.__points[0].coordinates]
			for p in self.__points:
				coordinates = p.coordinates
				for i in xrange(len(coordinates)):
					m[i] += coordinates[i]
			m = map(lambda x:x/self.__size,m)
			self.__center = Point(m)

	def distance(self,cl,linkage=DISTANCE_MAX):
		'''get the distance between 2 clusters. there are different scales
		'''
		if len(self.__points) == 0 or len(cl.points) == 0:
			return -1

		if linkage == DISTANCE_MEAN_CENTER:
			return self.__center.distance(cl.center)
		elif linkage == DISTANCE_MAX:
			#return the distance between the farest points
			result = -1
			for p1 in self.__points:
				for p2 in cl.points:
					d = p1.distance(p2)
					if d > result:
						result = d
			return result
		elif linkage == DISTANCE_MIN:
			#return the distance between the nearest points
			result = -1
			for p1 in self.__points:
				for p2 in cl.points:
					d = p1.distance(p2)
					if result == -1:
						result = d
					elif d < result:
						result = d
			return result
		else:
			print "No such scale"
			return

	@property
	def points(self):
		return self.__points[:]

	@property
	def center(self):
		return self.__center

	@property
	def size(self):
		return self.__size




