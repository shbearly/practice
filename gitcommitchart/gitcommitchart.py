
import os

''' output gittxt first '''
commitFile="/mnt/40g/python/gitcommitchart/commits.txt"
os.system('pushd /mnt/40g/usgv2/intel_usg; git --no-pager log --pretty="format:%h/%an/%ad" > ' + commitFile +'; pushd')

'''parse the file'''
class commit:
	def __init__(self, name, date):
		self.name = name
		self.date = date

dbs={}

def readFile(file):
	f = open(file)
	for str in f:
		l=str.split('/',-1)
		dbs[l[1]] = 1 if l[1] not in dbs else dbs[l[1]]+1 
	f.close()

readFile(commitFile)

ldbs=sorted(dbs.items(), key=lambda i:i[1], reverse=True)

for i in ldbs:
	print(i[1], i[0])
	


