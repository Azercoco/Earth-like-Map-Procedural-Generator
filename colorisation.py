import temp

import numpy as np
import matplotlib.pyplot as plt


from numpy import exp, abs
from random import random as rand
from noise import snoise2



l = rand() * 20000

SIZE = 512

heightmap, temperature = temp.generate(SIZE=SIZE)

def precipitation(j):
	lat = (j/SIZE - 1/2)*90
	return 5/ (1+ (lat/10)**2) + 2.5/(1+((lat-50)/10)**2) + 2.5/(1+((lat+50)/10)**2) - 1

prec0 = precipitation(0)

biome_list = []

biome_Model = {"maxA": None, "minA" : None, "A":None, "vA":None, "T":None, "vT":None, "H":None, "vH":None, "r":0, "g":0, "b":0}

biome_deep_water =    {"maxA": 0, "minA" : None, "A":-6000, "vA":3000, "T":40, "vT":30, "H":None, "vH":None, "r":16, "g":25, "b":36}
biome_median_water =  {"maxA": 0, "minA" : None, "A":-1000, "vA":1000, "T":40, "vT":30, "H":None, "vH":None, "r":32, "g":56, "b":73}
biome_shallow_water = {"maxA": 0, "minA" : None, "A":-300, "vA":300, "T":40, "vT":30, "H":None, "vH":None, "r":79, "g":170, "b":168}

biome_ice =           {"maxA": None, "minA" : 0, "A":None, "vA":None, "T":-10, "vT":5, "H":None, "vH":None, "r":255, "g":255, "b":255}
biome_water_ice =           {"maxA": 0, "minA" : None, "A":None, "vA":None, "T":-15, "vT":5, "H":None, "vH":None, "r":255, "g":255, "b":255}

biome_tundra =        {"maxA": None, "minA" : 0, "A":0, "vA":2000, "T":-5, "vT":5, "H":0.5, "vH":2, "r":93, "g":80, "b":35}

biome_boreal_forest = {"maxA": None, "minA" : 0, "A":500, "vA":1500, "T":5, "vT":5, "H":2, "vH":2, "r":12, "g":63, "b":7}

biome_forest = 		  {"maxA": None, "minA" : 0, "A":500, "vA":1500, "T":15, "vT":5, "H":2.5, "vH":3, "r":67, "g":88, "b":29}

biome_cold_desert =   {"maxA": None, "minA" : 0, "A":500, "vA":1500, "T":10, "vT":7, "H":0, "vH":1, "r":245, "g":200, "b":151}
biome_warm_desert =   {"maxA": None, "minA" : 0, "A":500, "vA":1500, "T":25, "vT":7, "H":0, "vH":1, "r":245, "g":200, "b":151}

biome_savanah =    	  {"maxA": None, "minA" : 0, "A":0, "vA":2000, "T":25, "vT":5, "H":1, "vH":1.5, "r":66, "g":105, "b":13}
biome_humid_savanah = {"maxA": None, "minA" : 0, "A":0, "vA":2000, "T":25, "vT":5, "H":2, "vH":1.5, "r":53, "g":112, "b":46}
biome_jungle =    	  {"maxA": None, "minA" : 0, "A":500, "vA":1000, "T":25, "vT":5, "H":3, "vH":1.5, "r":5, "g":50, "b":5}

biome_alpine_tundra  = 	  {"maxA": None, "minA" : 0, "A":4500, "vA":2000, "T":0, "vT":5, "H":0.5, "vH":3, "r":204, "g":167, "b":129}
biome_high_moutain  = 	  {"maxA": None, "minA" : 0, "A":6000, "vA":2000, "T":-5, "vT":5, "H":None, "vH":None, "r":136, "g":113, "b":77}



biome_list.append(biome_deep_water)
biome_list.append(biome_median_water)
biome_list.append(biome_shallow_water)

biome_list.append(biome_ice)
biome_list.append(biome_water_ice)

biome_list.append(biome_tundra)
biome_list.append(biome_boreal_forest)
biome_list.append(biome_forest)

biome_list.append(biome_cold_desert)
biome_list.append(biome_warm_desert)

biome_list.append(biome_savanah)
biome_list.append(biome_humid_savanah)
biome_list.append(biome_jungle)

biome_list.append(biome_alpine_tundra)
biome_list.append(biome_high_moutain)


n = len(biome_list)

ll = []

for i in range(n):
	ll.append(rand()*1000)

rgb_map = np.zeros((SIZE, SIZE, 3))

for i in range(SIZE):
	for j in range(SIZE):

		value_noise = snoise2(8*i/SIZE + l, 8*j/SIZE + l,  octaves=7, persistence=0.6, repeatx=8)

		A = heightmap[i, j]
		T = temperature[i, j]
		H = (4*precipitation(j)/prec0) * (1+value_noise/4)

		tot_prob = 0
		r = 0
		g = 0
		b = 0

		for k in range(n):
		
			biome = biome_list[k]
			lll = ll[k]

			if (biome["maxA"] is None or A <= biome["maxA"]) and (biome["minA"] is None or A >= biome["minA"]):
				p = 1

				t = 0

				if not biome["A"] is None:
					t += 1
					p *= exp( - ((biome["A"] - A) / (biome["vA"] )) ** 2)
				if not biome["H"] is None:
					t += 1
					p *= exp( - ((biome["H"] - H) / (biome["vH"] )) ** 2)
				if not biome["T"] is None:
					t += 1
					p *= exp( - ((biome["T"] - T) / (biome["vT"] )) ** 2)

				p ** (1/t)

				ss = snoise2(8*i/SIZE + lll, 8*j/SIZE + lll,  octaves=5, persistence=0.3, repeatx=8)/6

				p = p*(1+ss)

				
				r += p*biome["r"]
				g += p*biome["g"]
				b += p*biome["b"]

				tot_prob += p

		if tot_prob > 0:
			r = r/tot_prob
			g = g/tot_prob
			b = b/tot_prob

		randr = rand()*0.1 -0.05


		r = r*(1+randr)
		b = b*(1+randr)
		g = g*(1+randr)

		rgb_map[j, i] = min(r/256, 1), min(g/256, 1), min(b/256, 1)

dir_output = "Map"

plt.imsave(dir_output+"/map.png", rgb_map)

	