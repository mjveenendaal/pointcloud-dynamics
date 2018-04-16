import numpy as np
from scipy import spatial
import csv
import time


# Parameters
thinning_factor = 1
number_of_neighbors = 20 # trade-off between locality of the value, and precision of the calculation

# Calculation method: there are two methods provided for calculating the PCA eigenvalues
calculation_method = "svd"
# calculation_method = "cov"

def list2kdtrees(pts_list):
	kdt_list = []
	data_array = np.vstack(pts_list)
	length, dim = data_array.shape
	n_Z = dim-2
	column = 2
	while n_Z != 0:
		print "Building KDtree"
		data_array_X = data_array[:,0]
		data_array_Y = data_array[:,1]
		data_array_Z = data_array[:,column]
		new_array = np.transpose(np.vstack([data_array_X, data_array_Y,data_array_Z]))
		tree = spatial.cKDTree(new_array)
		kdt_list.append(tree)
		column +=1
		n_Z -=1 
	return kdt_list

def PCA_cov(data):
	m, n = data.shape
	data -= data.mean(axis=0)
	R = np.cov(data, rowvar=False)
	EVal, EVec = np.linalg.eigh(R)
	sorted_index = np.argsort(EVal)[::-1]
	sorted_EVec = EVec[:,sorted_index]
	sorted_EVal = EVal[sorted_index]
	return sorted_EVal

def PCA_pp(kdtree, pt, NN, method):
	# get the nearest neighbors and put their XYZ values in a list
	NearestNeighbors = kdtree.query(pt, k=NN) 
	distances, indexes = NearestNeighbors
	N_pt_list = []
	for i in indexes:
		N_point = kdtree.data[i]
		N_pt_list.append(N_point)
	M = np.vstack(N_pt_list)
	if method == "svd":
		# singular value decomposition
		M -= M.mean(axis=0)
		u, s, vh = np.linalg.svd(M, full_matrices=True)
		# Eigenvalue = singular value squared
		EV = np.square(s)
	if method == "cov":
		EV = PCA_cov(M)
	return EV


def PCA_kdtree(kdtree, tv, NN, method):
	start = time.time()
	ext_list = []
	for point in kdtree.data:
		EX, EY, EZ = PCA_pp(kdtree, point, NN, method)
		coord_EV = [point[0], point[1], point[2], EX, EY, EZ]
		ext_list.append(coord_EV)
	print "PCA time:"
	print str(time.time()-start)
	return ext_list

def PCA_kdlist(kdtlist, tv, NN, method):
	ext_PCA_list = []
	for kdtree in kdtlist:
		extlist = PCA_kdtree(kdtree, tv, NN, method)
		ext_PCA_list.append(extlist)
	return ext_PCA_list

def write_CSV(prefix, i, exp_point_list):
	filepath = prefix+str(i)+".csv"
	output = open(filepath, "w")
	writer = csv.writer(output, lineterminator='\n')
	writer.writerows(exp_point_list)
	output.close()

def main():
	with open('output.csv', 'r') as f:
		print "Reading data"
		reader = csv.reader(f)
		point_list = list(reader)

	list_of_trees = list2kdtrees(point_list)
	list_EV = PCA_kdlist(list_of_trees, thinning_factor, number_of_neighbors, calculation_method)

	for i, list_pts in enumerate(list_EV):
		write_CSV("output_PCA_", i, list_pts)
	





if __name__ == "__main__":
    main()