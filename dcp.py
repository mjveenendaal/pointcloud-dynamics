import numpy as np
from scipy import spatial
import csv
import time

import pca

# file paths
path_A = "output_PCA_0.csv"
path_B = "output_PCA_1.csv"


def csv2list(path):
	with open(path, 'r') as f:
		print "Reading data"
		reader = csv.reader(f)
		list_f = list(reader)
	return list_f

def build_kdtree(lst):
	print "Building KD-Tree..."
	start = time.time()
	array = np.vstack(lst)
	kdtree = spatial.cKDTree(array)
	print str(time.time()-start)+" seconds"
	return kdtree

# retrieve 6 dimensional closest point
def sixD_CP(ref, target):
	dist_list = []
	vec_list = []
	for point in ref.data:
		distance, index = target.query(point, k=1)
		RX, RY, RZ = point[:3]
		TX, TY, TZ = target.data[index][:3]
		if distance > 6.6: # heuristic noise threshold
			continue
		RP = np.array((RX, RY, RZ))
		TP = np.array((TX, TY, TZ))
		Vec = TP-RP
		eucl_dist = np.linalg.norm(RP-TP)
		coord_dist = [RX, RY, RZ, eucl_dist]
		coord_vec = [RX, RY, RZ, Vec[0], Vec[1], Vec[2]]
		dist_list.append(coord_dist)
		vec_list.append(coord_vec)
	return dist_list, vec_list

# unweighed smoothing
def uw_smoothing(datalist, N): 
	tree = build_kdtree(datalist)
	ext_list = []
	for point in tree.data:
		avg_list = []
		distance, index = tree.query(point, k=N)
		dim = point.shape[0]
		sub_idx = 3
		dim -= sub_idx
		avg_list.extend(point[0:3])
		while dim > 0:
			val_sum = 0.0
			for idx in index:
				val_sum += tree.data[idx][sub_idx]
			mean = val_sum/N
			avg_list.append(mean)
			sub_idx += 1
			dim -= 1
		ext_list.append(avg_list)
	return ext_list

def XYZtranslate(datalist, timescale):
	new = []
	for point in datalist:
		newX = point[0]+point[3]*timescale
		newY = point[1]+point[4]*timescale
		newZ = point[2]+point[5]*timescale
		subnew = [newX,newY,newZ]
		new.append(subnew)
	return new

def vec2angle(vec):
	X, Y, Z = vec[0], vec[1], vec[2]
	vecXY = np.array((X,Y))
	vecYZ = np.array((Y,Z))
	# create unit vectors
	normXY = np.linalg.norm(vecXY)
	normYZ = np.linalg.norm(vecYZ)
	if normXY != 0:
		vecXY = vecXY/normXY
	if normYZ != 0:
		vecYZ = vecYZ/normYZ
	refXY = np.array((1,0))
	refYZ = np.array((0,1))
	# alpha --> angle of vector projected onto XY plane
	alpha_rad = np.arccos(np.clip(np.dot(refXY, vecXY), -1.0, 1.0))
	alpha = np.rad2deg(alpha_rad)
	# beta --> angle of vector projected onto YZ plane 
	beta_rad = np.arccos(np.clip(np.dot(refXY, vecXY), -1.0, 1.0))
	beta = np.rad2deg(beta_rad)
	return alpha, beta

def vec2angle2(vec):
	return

def calc_angles(veclist):
	angle_list = []
	for point in veclist:
		pointlist = []
		vector = point[3:]
		coords = point[:3]
		angles = vec2angle(vector)
		pointlist.extend(coords)
		pointlist.extend(angles)
		angle_list.append(pointlist)
	return angle_list



def rotate(A, theta):
	rotated = []
	for point in A:
		x, y, z = float(point[0]), float(point[1]), float(point[2])
		X = x*np.cos(theta) - y*np.sin(theta)
		Y = x*np.sin(theta) + y*np.cos(theta)
		Z = z
		p = [X,Y,Z]
		rotated.append(p)
	return rotated


















def main():
	list_A = csv2list(path_A)
	list_B = csv2list(path_B)
	print len(list_A)
	# tree_A = build_kdtree(list_A)
	# tree_B = build_kdtree(list_B)

	# distances, vectors = sixD_CP(tree_A, tree_B)

	# smooth = uw_smoothing(vectors, 9)

	# may 2005 - jan 2006 = 8 months ; may 2005 - jun 2009 = 49 months
	# timefactor = 8 / 49 = 6.125 
	# final  = XYZtranslate(vectors, 1)

	# final = calc_angles(vectors)

	# rad = 1.0472 #60 deg
	rad = 0.523599 #30 deg

	final = rotate(list_A, rad)
	final2 = rotate(list_A, rad)
	pca.write_CSV("rotated30", "2005", final)
	pca.write_CSV("rotated30", "2006", final2)
	


if __name__ == "__main__":
    main()




