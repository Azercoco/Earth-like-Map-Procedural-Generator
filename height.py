import numpy as np
import matplotlib.pyplot as plt

from numpy import exp, abs
from scipy.integrate import quad
from scipy.special import erfc
from random import random as rand
from noise import snoise2


def generate(SIZE=256, MAX_DEPHT=-8000, MAX_HEIGHT=6000, mean_ocean_depht=-4500, mean_land_height=840):

	height_distib = []

	l = rand() * 20000

	heigthamp = np.zeros((SIZE, SIZE))

	height_distribution = lambda x : exp(-((x-mean_ocean_depht)/2000)**2) + exp( - 1.41 *abs((x-mean_land_height)/1000)**0.61)

	total, err = quad(height_distribution, MAX_DEPHT, MAX_HEIGHT)

	std = 0.25675
	precompute = {}


	def getAltitude(distib, a, b):

		r = 0

		if (a+b)//2 in precompute:
			r = precompute[(a+b)//2]
		else:
			r, err = quad(height_distribution, MAX_DEPHT, (a+b)//2)
			r = r/total
			precompute[(a+b)//2] = r

		if abs(a - b) <= 2:
			return (a+b)//2

		if r > distib:
			return getAltitude(distib, a, (a+b)//2)
		else:
			return getAltitude(distib, (a+b)//2, b)



	for i in range(SIZE):
		for j in range(SIZE): 
			value_noise = snoise2(2*i/SIZE + l, 2*j/SIZE + l,  octaves=7, persistence=0.5, repeatx=2)
			value_uniform = 0.5*erfc( - value_noise/(std*(2**0.5)))
			heigthamp[i, j] = getAltitude(value_uniform, MAX_DEPHT, MAX_HEIGHT)
			height_distib.append(heigthamp[i, j])



	return heigthamp


if __name__ == '__main__':
	h = generate()
	plt.imshow(h)
	plt.show()