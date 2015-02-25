import random

import matplotlib.pyplot as plt

from cluster import *


# The following variables are for different k_means algorithms
K_MEANS_PLUS_PLUS = 100
LLOYD = 200

class Clustering(object):
    """ The clustering method class. Different clustering methods are implemented.
    """
    def __init__(self,points):
        """ Init Clustering instance.

        Args:
            points (list): a list of Point instances.
        """
        self.__points = points
        if len(points) == 0:
            print "Should not initialize clustering without points!"



    def hierarchical_cluster(self,k,linkage = DISTANCE_MEAN_CENTER):
        """ Return the hierarchical clusters.

        Note:
            The algorithm is O(n^3) while the best one is O(n^2logn).
            I will re-write this soon.

        Args:
            k (int): the number of clusters you want to have.
            linkage (int): how to define the distance between clusters.
                See more information in Cluster.py

        Returns:
            clusters (list): list of Cluster instances.
        """
        if k < 1 or k > len(self.__points):
            return None

        clusters = []
        for p in self.__points:
            clusters.append(Cluster([p],linkage=linkage))

        while len(clusters) > k:
            index1 = -1
            index2 = -1
            distance = -1
            for i in xrange(len(clusters)-1):
                for j in xrange(i+1,len(clusters)):
                    d = clusters[i].distance(clusters[j])
                    if distance == -1:
                        distance = d
                        index1 = i
                        index2 = j
                    elif d < distance:
                        distance = d
                        index1 = i
                        index2 = j

            clusters[index1].union(clusters.pop(index2))

        return clusters

    def k_center(self,k,init_centers=[]):
        """ Return clusters.

        Node:
            This function uses the Gonzalez Algorithm.

        Args:
            k (int): the number of clusters wanted.
            init_centers (list,optional): the initial centers.

        Returns:
            clusters (list): list of the clusters
            cost (float): the cost of the entire clustering. In this case, it's the maximum distance of 
                          any (point, center) pair.

        """
        points = self.__points[:]
        centers = init_centers
        if len(centers) == 0:
            centers.append(points.pop(0))
        else:
            for p in init_centers:
                if p in points:
                    points.remove(p)

        cost = -1
        """ TODO

        The algorithm works but it is not efficient because distance between p and c does NOT
        need to be calculated every time!
        Update the distance when a new c is added to the centers
        """

        # Find k centers
        while len(centers) < k:
            max_distance = -1
            index = -1
            for i in xrange(len(points)):
                min_distance = -1
                p = points[i]
                for c in centers:
                    d = p.distance(c)
                    cost = d if d > cost else cost
                    if min_distance == -1:
                        min_distance = d
                    elif d < min_distance:
                        min_distance = d

                if min_distance > max_distance:
                    max_distance = min_distance
                    index = i

            centers.append(points.pop(i))

        # Construct the clusters.
        clusters = []
        for c  in centers:
            new_cluster = Cluster([c])
            new_cluster.set_center(c)
            clusters.append(new_cluster)

        """ TODO

        I don't think this is efficient. Is there another way?
        """
        cost = -1
        while(len(points) != 0):
            p = points.pop(0)
            distance = -1
            index = -1
            for i in xrange(len(clusters)):
                c = clusters[i].center
                d = p.distance(c)
                cost = d if d > cost else cost
                if distance == -1:
                    distance = d
                    index = i
                elif d < distance:
                    distance = d
                    index = i

            clusters[index].add_points([p])
        return clusters,cost

    def k_means(self,k,method=K_MEANS_PLUS_PLUS,init_centers = []):
        """ Return clusters.

        Args:
            k (int): the number of clusters as a result.
            method (int): the algorithm used to cluster.
                K_MEANS_PLUS_PLUS: the k-means++ algorithm
                LLOYD: the Lloyd algorithm
            init_centers (list): list of initial center.

        Note:
            The length of init_centers CAN'T exceed k.

        Returns:
            clusters (list): list of the clusters
            cost (float): the cost of the entire clustering. In this case, it's the sum of the square distance
                          of any (point, center) pair.
        """
        points = self.__points[:]
        centers = init_centers
        for p in init_centers:
            if p in points:
                points.remove(p)

        if method == K_MEANS_PLUS_PLUS:
            if len(centers) == 0:
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

            # Construct the clusters
            clusters = []
            for c  in centers:
                new_cluster = Cluster([c])
                new_cluster.set_center(c)
                clusters.append(new_cluster)

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

            return clusters,cost

        elif method == LLOYD:
            """TODO

            Set some repetion rounds. currently, it stops when it converges
            """
            # Init the centers
            for i in xrange(k-len(centers)):
                centers.append(points[random.randint(0,len(points)-1)])

            subsets = {}
            for c in centers:
                subsets[c] = []

            centers_to_add = centers
            cost = 0
            while len(centers_to_add) > 0:
                cost = 0
                centers_to_add = []
                centers_to_delete = []
                for c in subsets:
                    subsets[c] = []

                # Find the sets for each center
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

                    cost += d
                    subsets[center].append(p)

                # Check if the center needs to be updated
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

            clusters = []
            for c,cl in subsets.items():
                new_cluster = Cluster(cl)
                new_cluster.set_center(c)
                clusters.append(new_cluster)

            return clusters,cost

    def k_median(self,k,init_centers=[]):
        """ Return clusters.

        Note:
            The idea of the algorithm is, to find the point in the subset,
            which minimize the sum of distances to other points in the same subset and
            use it as the new center. we keep doing this until it converges.

        Args:
            k (int): the number of clusters wanted.
            init_centers (list): list of initial centers.

        Note:
            The length of init_centers CAN'T exceed k.

        Returns:
            clusters (list): list of the clusters
            cost (float): the cost of the entire clustering. In this case, it is the sum of distance of any (point, center) pair.
        """

        points = self.__points[:]
        centers = init_centers
        for p in init_centers:
            if p in points:
                points.remove(p)

        for i in xrange(k-len(centers)):
                centers.append(points.pop(random.randint(0,len(points)-1)))

        subsets = {}
        for c in centers:
            subsets[c] = []

        centers_to_add = centers

        cost = 0
        while len(centers_to_add) > 0:
            centers_to_add = []
            centers_to_delete = []
            for c in subsets:
                subsets[c] = []

            # Find the sets for each center
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

                cost += distance
                subsets[center].append(p)

            # Check if the center needs to be updated
            for c in subsets:
                subset = subsets[c]
                subset.append(c)
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
                points.remove(c)

            for c in centers_to_delete:
                del subsets[c]
                points.append(c)


        clusters = []
        for c,cl in subsets.items():
            new_cluster = Cluster(cl)
            new_cluster.set_center(c)
            clusters.append(new_cluster)

        return clusters, cost



    def draw_2_dimentional_graph(self,clusters):
        """ Return a graph for given clusters.

        Note:
            It only works for 2 dimentional clusters. Also, when the number of clusters exceeds 8, I can't tell clusters with the same color.

        Args:
            clusters (list): list of clusters.
        """
        colors = ['b','r','g','c','m','y','k','w']
        clen = 8
        """TODO

        Actually, if the number of clusters is over 8, I can't tell the difference between clusters with the same color.
        Is there a way to solve this?
        """
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

if __name__ == '__main__':
    print "Example"

    # Create list of points
    f = open("data.txt")
    points = []
    for line in f.readlines():
        l = line.split()
        index = int(l[0])
        x = float(l[1])
        y = float(l[2])
        p = Point([x,y],index)
        points.append(p)

    # init Clustering instance
    cl = Clustering(points)

    """Note

    hierarchical_cluster on the example data set may be very slow. It works for smaller data set.
    """
    #clusters = cl.hierarchical_cluster(4,DISTANCE_MAX)
    #clusters = cl.hierarchical_cluster(4,DISTANCE_MIN)
    #clusters = cl.hierarchical_cluster(4,DISTANCE_MEAN_CENTER)
    #clusters,cost= cl.k_center(3)
    #clusters,cost= cl.k_means(3,method=LLOYD)
    #clusters,cost= cl.k_means(3,method=K_MEANS_PLUS_PLUS)
    #clusters,cost= cl.k_means(3,method=K_MEANS_PLUS_PLUS,init_centers=[])
    clusters,cost= cl.k_median(3)

    
    # Report points in a cluster
    cluster_index = 0
    for c in clusters:
        print "cluster %d" % cluster_index
        print "the center is ",c.center
        for p in c.points:
            print p
        cluster_index += 1

    print "the cost is %f" % cost
    
    # Draw the graph for the clustering
    cl.draw_2_dimentional_graph(clusters)
