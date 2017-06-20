# simple python client to parse cst files to proper rep

import re
import os

path = os.path.abspath("test.txt")

# format codes
# numbers in results block per sweep 
ilines = 3 +2 # ignore the 2
sweeps = 20

file = open(path,'r')
str = file.readlines()
str1 = ''.join(str)
n = list()

list1 = re.findall(r"[-+]?\d*\.\d+|\d+",str1)

print list1

def indeces(ilines,i):
	global n
	if not n:
		n = [0, 1]
	else:
		N = [0, 1]
		N[-2] = n[-2] + ilines
		N[-1] = n[-1] + ilines
		n = n + N

	return n

for i in range(sweeps):
	n = indeces(ilines,i)

for o, i in enumerate(n):
  i -= o
  del list1[i]

print n 
print list1

res = open('res.txt','w')

i = 0
while i < len(list1):
	for j in range(ilines-2):
		res.write("%s\t" % list1[(i)+(j)])
    
	res.write("\n")
	i += ilines-2



