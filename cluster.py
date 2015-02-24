from point import *


# The following variables are used to specify 
# how to calculate the distance between clusters
DISTANCE_MAX = 1
DISTANCE_MIN = 2
DISTANCE_MEAN_CENTER= 3

class Cluster(object):
	""" The cluster class. It contains a list of Point instances.
	"""

	def __str__(self):
		return "The cluster is of size %d\n" % self.__size


	def __init__(self,points):
		""" Init Cluster instances.

		Args:
			points (list): a list of Point instances.

		Attributes:
			__points (list): list of Point instances.
			__size (int): number of points
			__center (Point): the center Point, mainly used for k_center algorithm
		"""
		self.__points = []
		self.__size = 0
		self.__center = None

		if points is not None:
			self.__points = points[:]
			self.__size = len(points)

			# Calculate the self.__center
			m = [0 for i in self.__points[0].coordinates]
			for p in self.__points:
				coordinates = p.coordinates
				for i in xrange(len(coordinates)):
					m[i] += coordinates[i]
			m = map(lambda x:x/self.__size,m)
			self.__center = Point(m)
		


	def union(self,c,update_center=True):
		""" Union with another cluster.

		Args:
			c (Cluster): another Cluster.
			update_center (bool,optional): default is True. However, since center is only used for 
				k_center algorithm, you can disable it if you don't use k_center algorithm.
		"""
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
		""" Add some Points into the cluster.

		Args:
			points (list): list of Point instances.
			update_center (bool,optional): default is True. However, since center is only used for 
				k_center algorithm, you can disable it if you don't use k_center algorithm.
		"""
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
		""" Calculate the distance between two Clusters.

		Args:
			cl (Cluster): another Cluster.
			linkage (int): define the distance between Clusters. Now, only 3 linkage are supported.
				DISTANCE_MAX: distance between Clusters is the distance between farest Points from both Clusters.
				DISTANCE_MIN: distance between Clusters is the distance between nearest Points from both Clusters.
				DISTANCE_MEAN_CENTER: distance between Clusters is the distance between centers of both Clusters.

		Returns:
			float: distance between two Clusters.
		"""		
		if self.__size == 0 or cl.size == 0:
			return -1

		if linkage == DISTANCE_MEAN_CENTER:
			return self.__center.distance(cl.center)
		elif linkage == DISTANCE_MAX:
			result = -1
			for p1 in self.__points:
				for p2 in cl.points:
					d = p1.distance(p2)
					if d > result:
						result = d
			return result
		elif linkage == DISTANCE_MIN:
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
			print "No such linkage"
			return -1

	@property
	def points(self):
		return self.__points[:]

	@property
	def center(self):
		return self.__center

	@property
	def size(self):
		return self.__size




