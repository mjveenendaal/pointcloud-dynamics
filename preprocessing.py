# -*- coding: utf-8 -*-

import numpy as np
from scipy import spatial
from multiprocessing import Pool
import csv

# filenames
fn_2005 = "AA200505.txt"
fn_2006 = "AA200601.txt"
fn_2009 = "AA200906.txt"

# sets of (x, y)
set_XY_2005 = set()
set_XY_2006 = set()
set_XY_2009 = set()

# lists of [(x,y), z]
list_XYZ_2005 = []
list_XYZ_2006 = []
list_XYZ_2009 = []

with open(fn_2005, "r") as f:
	data = f.readlines()
	for line in data:
		str_coords = line.split()
		iX, iY, iZ = float(str_coords[0]), float(str_coords[1]), -float(str_coords[2])
		set_XY_2005.add((iX, iY))
		list_XYZ_2005.append([iX, iY, iZ])

with open(fn_2006, "r") as f:
	data = f.readlines()
	for line in data:
		str_coords = line.split()
		iX, iY, iZ = float(str_coords[0]), float(str_coords[1]), -float(str_coords[2])
		set_XY_2006.add((iX, iY))
		list_XYZ_2006.append([iX, iY, iZ])

only_in_2005 = set_XY_2005 - set_XY_2006
only_in_2006 = set_XY_2006 - set_XY_2005

for coords in list_XYZ_2005:
	if coords[0] in only_in_2005:
		list_XYZ_2005.remove(coords)

set_XY_20052006 = set()

for coords in list_XYZ_2006:
	if coords[0] in only_in_2006:
		list_XYZ_2006.remove(coords)
	else:
		set_XY_20052006.add(coords[0])

with open(fn_2009, "r") as f:
	data = f.readlines()
	for line in data:
		str_coords = line.split()
		iX, iY, iZ = float(str_coords[0]), float(str_coords[1]), float(str_coords[2])
		set_XY_2009.add((iX, iY))
		list_XYZ_2009.append([iX, iY, iZ])


only_in_2009 = set_XY_2009 - set_XY_20052006

# floating point precision problem
# too many points are in only_in_2009
# compare 2009 

dataset2005 = np.vstack(list_XYZ_2005)

kdtree2005 = spatial.cKDTree(dataset2005)

dataset2006 = np.vstack(list_XYZ_2006)

kdtree2006 = spatial.cKDTree(dataset2006)

exp_point_list = []

counter = 0

distance_threshold = 1.0

for coord in list_XYZ_2009:
	ext_coord = []
	distance, index = kdtree2005.query(coord, k=2)
	if distance[0] < distance_threshold:
		ext_coord.append(dataset2005[index[0]][0])
		ext_coord.append(dataset2005[index[0]][1])
		ext_coord.append(dataset2005[index[0]][2])
	else:
		PA = np.array(coord[:-1])
		PB = np.array([dataset2005[index[0]][0],dataset2005[index[0]][1]])
		twoD_dist = np.linalg.norm(PA-PB)
		if twoD_dist < distance_threshold:
			ext_coord.append(dataset2005[index[0]][0])
			ext_coord.append(dataset2005[index[0]][1])
			ext_coord.append(dataset2005[index[0]][2])
		else:
			continue
	distance2, index2 = kdtree2006.query(coord, k=2)
	if distance2[0] < distance_threshold:
		ext_coord.append(dataset2006[index2[0]][2])
		ext_coord.append(coord[2])
	else:
		PA = np.array(coord[:-1])
		PB = np.array([dataset2006[index2[0]][0],dataset2006[index2[0]][1]])
		twoD_dist = np.linalg.norm(PA-PB)
		if twoD_dist < distance_threshold:
			ext_coord.append(dataset2006[index2[0]][2])
			ext_coord.append(coord[2])
		else:
			continue
	if (ext_coord[0] - dataset2006[index2[0]][0]) < 1:
		exp_point_list.append(ext_coord)
		counter += 1
	else:
		continue

print counter
		
output = open("output.csv", "w")
writer = csv.writer(output, lineterminator='\n')
writer.writerows(exp_point_list)
output.close()





# multiprocessing approach
 
# def lookup(nested_list, coord_tuple):
# 	for entry in nested_list:
# 		if entry[0] == coord_tuple:
# 			print "match for: "+str(coord_tuple)
# 			return entry[1]
# 			break
# 		else:
# 			continue

# ext_pt_list = []
# counter = 0

# for entry in coord_match:
# 	pool = Pool(3)
# 	result2005 = pool.apply_async(lookup, [list_XYZ_2005, entry[0]])
# 	result2006 = pool.apply_async(lookup, [list_XYZ_2006, entry[0]])
# 	result2009 = pool.apply_async(lookup, [list_XYZ_2009, entry[1]])
# 	ext_coord_list = [entry[0][0], entry[0][1], result2005.get(timeout=100), result2006.get(timeout=100), result2009.get(timeout=100)]
# 	ext_pt_list.append(ext_coord_list)
# 	if counter % 1000 == 0:
# 		print ext_coord_list
# 	counter += 1


















# for coord in only_in_2009:
# 	c_A = np.array(coord)
# 	for coord_ref in set_XY_20052006:
# 		c_B = np.array(coord_ref)
# 		dist = np.sqrt(np.sum((c_A-c_B)**2))
# 		if dist < 0.1:
# 			counter += 1



## filename list
# fn_list = [fn_2005,fn_2006,fn_2009]

# array_list = []

# for fn in fn_list:
# 	array_list.append(np.loadtxt(fn, delimiter=" "))

# print array_list

# for t_f in fn_list:
# 	l = int(len(t_f.readlines()))
# 	array_XYZ = np.zeros((l,3))
# 	print t_f.re
# 	for line in t_f:
# 		print line
		
