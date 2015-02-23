from cluster import *
import matplotlib.pyplot as plt
import random

K_MEANS_PLUS_PLUS = 100
LLOYD = 200

class Clustering(object):
	'''clustering object used to create clusters based on points
	'''
	def __init__(self,points = []):
		self.__points = points
		if len(points) == 0:
			print "Should not initialize clustering without points!"


	def hierarchical_cluster(self,num,linkage = DISTANCE_MEAN_CENTER):
		'''TODO
		The algorithm is O(n^3) while the best is O(n^2logn)
		'''
		if num < 1 or num > len(self.__points):
			return None

		clusters = []
		for p in self.__points:
			clusters.append(Cluster([p]))

		while len(clusters) > num:
			index1 = -1
			index2 = -1
			distance = -1
			for i in xrange(len(clusters)-1):
				for j in xrange(i+1,len(clusters)):
					d = clusters[i].distance(clusters[j],linkage=linkage)
					if distance == -1:
						distance = d
						index1 = i
						index2 = j
					elif d < distance:
						distance = d
						index1 = i
						index2 = j

			if linkage == DISTANCE_MEAN_CENTER:
				'''TODO
				is there a better implementation than using update_center???
				'''
				clusters[index1].union(clusters.pop(index2),update_center=True)
			else:
				clusters[index1].union(clusters.pop(index2))

		return clusters

	def k_center(self,k):
		'''
		   Gonzalez Algorithm
		'''
		points = self.__points[:]
		centers = []
		centers.append(points.pop(0))
		
		'''TODO
		The algorithm works but it is not efficient because distance between p and c does NOT 
		need to be calculated every time!
		Update the distance when a new c is added to the centers
		'''

		#find k centers
		while len(centers) < k:
			max_distance = -1
			index = -1
			for i in xrange(len(points)):
				min_distance = -1
				p = points[i]
				for c in centers:
					d = p.distance(c)
					if min_distance == -1:
						min_distance = d
					elif d < min_distance:
						min_distance = d

				if min_distance > max_distance:
					max_distance = min_distance
					index = i

			centers.append(points.pop(i))

		#construct the clusters as well as the cost
		clusters = []
		for c  in centers:
			clusters.append(Cluster([c]))

		cost = -1

		while(len(points) != 0):
			p = points.pop(0)
			distance = -1
			index = -1
			for i in xrange(len(centers)):
				c = centers[i]
				d = p.distance(c)
				if distance == -1:
					distance = d
					index = i
				elif d < distance:
					distance = d
					index = i
			
			cost = distance if distance > cost else cost
			clusters[index].add_points([p])

		return centers,clusters,cost

	def k_means(self,k,method=K_MEANS_PLUS_PLUS,init_centers = []):
		points = self.__points[:]
		centers = init_centers
		if method == K_MEANS_PLUS_PLUS:
			centers.append(points.pop(0))

			while len(centers) < k:
				weights = {}
				for i in xrange(len(points)):
					p = points[i]
					distance = -1
					for c in centers:
						d = p.distance(c)**2
						if distance == -1:
							distance = d
						elif d < distance:
							distance = d

					weights[i] = distance

				s = sum(weights.values())

				for key in weights:
					weights[key] /= s

				chozen = False
				chozen_point = 0
				while not chozen:
					for key in weights:
						if weights[key] > random.random():
							chozen = True
							chozen_point = key
							break
		
				centers.append(points.pop(chozen_point))

			#construct the clusters
			clusters = []
			for c  in centers:
				clusters.append(Cluster([c]))

			cost = 0

			while(len(points) != 0):
				p = points.pop(0)
				distance = -1
				index = -1
				for i in xrange(len(centers)):
					c = centers[i]
					d = p.distance(c)**2
					if distance == -1:
						distance = d
						index = i
					elif d < distance:
						distance = d
						index = i
				
				cost += distance
				clusters[index].add_points([p])

			return centers,clusters,cost

		elif method == LLOYD:
			'''TODO
			   set some repetion rounds. currently, it stops when it converges
			'''
			#init the centers
			for i in xrange(k-len(centers)):
				centers.append(points[random.randint(0,len(points)-1)])

			subsets = {}
			for c in centers:
				subsets[c] = []

			centers_to_update = centers
			while len(centers_to_update) > 0:
				centers_to_add = []
				centers_to_delete = []
				for c in subsets:
					subsets[c] = []

				#find the sets for each center
				for p in points:
					center = None
					distance = -1
					for c in subsets:
						d = p.distance(c)**2
						if distance == -1:
							distance = d
							center = c
						elif d < distance:
							distance = d
							center = c

					subsets[center].append(p)

				#check if the center needs to be updated
				for c in subsets:
					subset = subsets[c]
					if len(subset) > 0:
						m = [0 for i in subset[0].coordinates]
						for p in subset:
							coordinates = p.coordinates
							for i in xrange(len(coordinates)):
								m[i] += coordinates[i]
						
						m = map(lambda x:x/len(subset),m)
						new_center = Point(m)
						if not c.equal(new_center):
							centers_to_add.append(new_center)
							centers_to_delete.append(c)

				for c in centers_to_add:
					subsets[c] = []

				for c in centers_to_delete:
					del subsets[c]

				centers_to_update = centers_to_add

			cost = 0
			for c in subsets:
				subset = subsets[c]
				for p in subset:
					cost += p.distance(c)**2

			return subsets.keys(), [Cluster(i) for i in subsets.values()],cost

	def k_median(self,k,init_centers=[]):
		'''The idea of the algorithm is, to find the point in the subset,
		   which minimize the sum of distances to other points in the same subset and
		   use it as the new center. we keep doing this until it converges.
		'''

		points = self.__points[:]
		centers = init_centers
		for i in xrange(k-len(centers)):
				centers.append(points[random.randint(0,len(points)-1)])

		subsets = {}
		for c in centers:
			subsets[c] = []

		centers_to_update = centers

		while len(centers_to_update) > 0:
			centers_to_add = []
			centers_to_delete = []
			for c in subsets:
				subsets[c] = []

			#find the sets for each center
			for p in points:
				center = None
				distance = -1
				for c in subsets:
					d = p.distance(c)
					if distance == -1:
						distance = d
						center = c
					elif d < distance:
						distance = d
						center = c

				subsets[center].append(p)

			#check if the center needs to be updated
			for c in subsets:
				subset = subsets[c]
				distance_sum = -1
				new_center = None
				for p in subset:
					d = 0
					for q in subset:
						d += p.distance(q)
					if distance_sum == -1:
						distance_sum = d
						new_center = p
					elif d < distance_sum:
						distance_sum = d
						new_center = p

				if not c.equal(new_center):
					centers_to_add.append(new_center)
					centers_to_delete.append(c)

			for c in centers_to_add:
				subsets[c] = []

			for c in centers_to_delete:
				del subsets[c]

			centers_to_update = centers_to_add

		cost = 0
		for c in subsets:
			subset = subsets[c]
			for p in subset:
				cost += p.distance(c)

		return subsets.keys(), [Cluster(i) for i in subsets.values()],cost



	def draw_2_dimention(self,clusters):
		'''Given the clusters, draw them.
		   Note that only 2 dimentional clusters can be drawn
		'''
		colors = ['b','r','g','c','m','y','k','w']
		clen = 8
		'''TODO
		   Actually, if the number of clusters is over 8, I can't tell the difference between clusters with the same color
		'''
		for i in xrange(len(clusters)):
			cluster = clusters[i]
			x = []
			y = []
			for p in cluster.points:
				coordinates = p.coordinates
				x.append(coordinates[0])
				y.append(coordinates[1])
			style = 'o'+colors[i%clen]
			plt.plot(x,y,style)

		plt.show()

	@property
	def points(self):
		return self.__points[:]

