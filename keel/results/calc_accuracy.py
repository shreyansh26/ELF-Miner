from __future__ import print_function
import numpy as np
import os

folders_list = ['ucs', 'xcs', 'gassist_adi']

for i in folders_list[-1:]:
	file = os.path.join(i, os.listdir(i)[0])
	print(file.split('/')[0], end = ' - ')
	total = 0
	correct = 0
	with open(file, 'r') as f:
		i = -1
		for l in f:
			i += 1
			if(i<150):
				continue
			else:
				s = l.strip('\n')
				s = s.split(' ')
				# print(s)
				val1 = s[0]
				val2 = s[1]
				if val1 == val2 and val1 != '':
					correct += 1
				total += 1

	print(float(correct)/total)
