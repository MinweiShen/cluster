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


	def __init__(self,points,linkage=DISTANCE_MAX):
		""" Init Cluster instances.

		Args:
			points (list): a list of Point instances.
			linkage (int): define the distance between Clusters. Now, only 3 linkages are supported.
				DISTANCE_MAX: distance between Clusters is the distance between farest Points from both Clusters.
				DISTANCE_MIN: distance between Clusters is the distance between nearest Points from both Clusters.
				DISTANCE_MEAN_CENTER: distance between Clusters is the distance between mean centers of both Clusters.

		Attributes:
			__points (list): list of Point instances.
			__size (int): number of points
			__center (Point): the center Point
			__linkage (int): linkage
		"""
		self.__points = []
		self.__size = 0
		self.__center = None
		self.__linkage = linkage

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
		


	def union(self,c):
		""" Union with another cluster.

		Args:
			c (Cluster): another Cluster.
		"""
		self.__points += c.points
		self.__size += len(c.points)

	def add_points(self,points):
		""" Add some Points into the cluster.

		Args:
			points (list): list of Point instances to add.
		"""
		self.__points += points
		self.__size += len(points)
		# if update_center:
		# 	m = [0 for i in self.__points[0].coordinates]
		# 	for p in self.__points:
		# 		coordinates = p.coordinates
		# 		for i in xrange(len(coordinates)):
		# 			m[i] += coordinates[i]
		# 	m = map(lambda x:x/self.__size,m)
		# 	self.__center = Point(m)

	def distance(self,cl):
		""" Calculate the distance between two Clusters.

		Args:
			cl (Cluster): another Cluster.

		Returns:
			float: distance between two Clusters.
		"""		
		if self.__size == 0 or cl.size == 0:
			return -1

		if self.__linkage == DISTANCE_MEAN_CENTER:
			m1 = [0 for i in self.__points[0].coordinates]
			for p in self.__points:
				coordinates = p.coordinates
				for i in xrange(len(coordinates)):
					m1[i] += coordinates[i]
			m1 = map(lambda x:x/self.__size,m1)
			center1 = Point(m1)

			m2 = [0 for i in cl.points[0].coordinates]
			for p in cl.points:
				coordinates = p.coordinates
				for i in xrange(len(coordinates)):
					m2[i] += coordinates[i]
			m2 = map(lambda x:x/self.__size,m2)
			center2 = Point(m2)

			return center1.distance(center2)

		elif self.__linkage == DISTANCE_MAX:
			result = -1
			for p1 in self.__points:
				for p2 in cl.points:
					d = p1.distance(p2)
					if d > result:
						result = d
			return result
		elif self.__linkage == DISTANCE_MIN:
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

	def set_center(self,c):
		""" Set the center of the cluster

		Args:
			c (Point): the new center for the cluster
		"""
		self.__center = c


	@property
	def points(self):
		return self.__points[:]

	@property
	def center(self):
		return self.__center

	@property
	def size(self):
		return self.__size

	@property
	def linkage(self):
		return self.__linkage




