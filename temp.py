import height
import numpy as np
import scipy as sp
import scipy.sparse as sparse

import matplotlib.pyplot as plt

from numpy import cos, abs, pi

from random import random as rand
from noise import snoise2


def generate(SIZE=256):

	l = rand()*1000
	
	print('Generating heightmap')
	heightmap = height.generate(SIZE=SIZE)
	print('Heightmap done')


	def xy_to_ind(x, y):
		return x*SIZE+y

	def ind_to_xy(ind):
		return ind//SIZE, ind%SIZE


	T_apport_eq = 273.15  +  40
	T_apport_pole = 273.15 - 10
	temp_lat =  lambda lat : (T_apport_eq - T_apport_pole)*cos( pi*abs(lat-SIZE/2) / SIZE) + T_apport_pole





	#equation de la chaleur k(dxx + dyy) + h = 0
	# dxx = (-2u[i, j] + u[i-1, j] + u[i+1, j])/d²
	# dyy = (-2u[i, j] + u[i, j-1] + u[i, j+1])/d²

	#emssion prop à la temperature
	#k(dxx + dyy)T + h - cT = 0


	coeff = lambda h :  0.01*(SIZE*SIZE)*(1.0 if h < 0 else 25.0)

	b = np.zeros(SIZE*SIZE)

	row = []
	column = []
	data = []

	for i in range(SIZE):
		for j in range(SIZE):
		
			h = heightmap[i, j]
			
			k = coeff(h)

			c = 1

			temp = temp_lat(j)


			indc1 = xy_to_ind(i, j)
			
			row.append(indc1)
			column.append(indc1)
			data.append(-4*k - c)

			if i < SIZE-1:
				row.append(indc1)
				column.append(xy_to_ind(i+1, j))
				data.append(k)

			if i == SIZE-1:
				row.append(indc1)
				column.append(xy_to_ind(0, j))
				data.append(k)


			if i > 0:
				row.append(indc1)
				column.append(xy_to_ind(i-1, j))
				data.append(k)

			if i == 0:
				row.append(indc1)
				column.append(xy_to_ind(SIZE-1, j))
				data.append(k)

			if j < SIZE-1:
				row.append(indc1)
				column.append(xy_to_ind(i, j+1))
				data.append(k)


			if j > 0:
				row.append(indc1)
				column.append(xy_to_ind(i, j-1))
				data.append(k)

			value_noise = snoise2(8*i/SIZE + l, 8*j/SIZE + l,  octaves=5, persistence=0.3, repeatx=8)

			b[indc1] = -temp*(1+value_noise/250)

			if j == 0 or j == SIZE-1:
					b[indc1] -= k*T_apport_pole

	matrix = sparse.coo_matrix((data, (row, column)), shape=(SIZE*SIZE, SIZE*SIZE))

	x = sp.sparse.linalg.spsolve(matrix, b)


	temp_map =  np.zeros((SIZE, SIZE))
	for i in range(SIZE*SIZE):
		xx, yy = ind_to_xy(i)
		temp_map[xx, yy] = x[i] - 273.15 - (0 if heightmap[xx, yy ] < 0 else heightmap[xx, yy ]/250)

	return heightmap, temp_map
	


if __name__ == '__main__':
	_, temp_map = generate()	
	plt.imshow(np.transpose(temp_map))
	plt.show()
