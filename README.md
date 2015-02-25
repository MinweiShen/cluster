#Cluster

This is a python module for clustering data.
It is mainly composed of three classes, as is introduced below.

## Point
This class define the basic element, point, in a cluster. The default distance function uses Euclidean distance. However, you can use any other distances as you want, just initialize the Point instance with your distance function like:
```python
p = Point([0,0],distance_function=your_function)
```
Properties and functions you may use are:
```python
p.coordinates # a list of coordinates
p.dimention # the dimention of this point
p.index # the index for the point, default is -1
p1.distance(p2) # return the distance
p1.equal(p2) # return True if the two points are equal
```

## Cluster
This class defines the cluster.
Cluster instances are initialzed with a list of points, like:
```python
cluster = Cluster([p1,p2],linkage=DISTANCE_MIN)
```
linkage defines the distance between clusters. It is optional and the default is DISTANCE_MAX.

* DISTANCE_MAX: distance between clusters is the distance between farest points from both clusters.
* DISTANCE_MIN: distance between clusters is the distance between nearest points from both clusters.
* DISTANCE_MEAN_CENTER: distance between clusters is the distance between mean centers of both clusters. Mean centers are calculated. They are the average of all the points in that cluster.

Properties and functions you may use are:
```python
cluster.size # number of points in that cluster
cluster.points # a list of points
cluster.center # the center of the cluster
cluster.linkage # linkage of the cluster
c1.union(c2) # combine 2 clusters. c1 will have all the points of c1 and c2.
c1.add_points([p1,p2]) # add a list of points to c1
c1.set_center(p1) # set the center of c1 to p1
```
## Clustering
The most import class in this module. All the clustering methods are defined in this class.

An instance of Clustering is initilized with a list of points, like:
```python
cl = Clustering([p1,p2,p3])
```
The different clustering methods you can use are:
```
def hierarchical_cluster(self,k,linkage = DISTANCE_MEAN_CENTER):
def k_center(self,k,init_centers=[])
def k_means(self,k,method=K_MEANS_PLUS_PLUS,init_centers = [])
def k_median(self,k,init_centers=[])
def draw_2_dimention(self,clusters)
```
All the functions and options are well docemented in the source file. You can refer to it when you want. 

## How to use
There are example codes in ```clustering.py``` which you may check out.

Basically, you can use it in this way:
```python
points = []
# Create a list of points
for i in xrange(n):
    p = Point([x,y])
    points.append(p)
    
cl = Clustering(points)
clusters,cost = cl.k_means(3,method=K_MEANS_PLUS_PLUS)

print cost
for c in clusters:
    for p in c.points:
        print p
```