#/usr/bin/python

import os
import re


class syslib:
	def __init__(self,str):
		self.used = 0
		self.fullpath = str
		self.hs = hash(str)

systemLibaryList=[]

def dirTransverse(path):
	items=os.listdir(path)
	for i in items :
		if i == '.' or i == '..':
			#print("is dot")
			continue
		elif os.path.isdir(path+"/"+i):
			dirTransverse(path+"/"+i)
		elif os.path.isfile(path+"/"+i) and re.search(r'(\.so)',i,re.I) is not None:
			systemLibaryList.append(syslib(path+"/"+i))

def orderDir():
	sorted(systemLibaryList, cmp=lambda x,y:cmp(x.hs,y.hs), reverse=False)

def findandMarklib(Hlib):
	for i in systemLibaryList:
		if Hlib == i.hs:
			i.used=1
			break
	str = i.fullpath
	while(os.path.islink(str)):
		str=os.readlink(str)
		print(str)
		findandMarklib(hash(str))

def getMaps(path):
	if not os.path.exists(path+"/"+"maps"):
		return

	f=open(path+"/"+"maps")
	if f is None:
		return
		
	#print(path)

	str=f.readline()
	previous = ""
	while str != "":
		ret=re.search(r'\w+[ ]{3,8}(.*\.so.*)', str, re.I) 
		if ret is None:
			str=f.readline()
			continue
		if previous == ret.group(1) :
			str=f.readline()
			continue
		else:
			previous=ret.group(1)

		Hlib = hash(ret.group(1).strip(' \r\n\t'))
		findandMarklib(Hlib)
		str=f.readline()

	f.close()

def procTransverse(dir):
	items=os.listdir(dir)
	for i in items:
		try:
			ret = int(i, 10)
		except ValueError:
			pass
		else:
			getMaps(dir+"/"+i)

def linkmark(item):
	if os.path.islink(item.fullpath):
		if ( os.path.isabs(os.readlink(item.fullpath))):
			l = os.readlink(item.fullpath)
		else:
			l = os.path.realpath(os.path.dirname(item.fullpath)+'/'+os.readlink(item.fullpath))
		#print("link is:"+l+" origin is:"+item.fullpath)
		hs = hash(l)	
		for i in systemLibaryList:
			if i.hs == hs:
				item.used = linkmark(i)
				#print("Link:"+item.fullpath)
				return item.used
	else:
		return item.used

def findNotUsedLink():
	for i in systemLibaryList:
		if not i.used:
			linkmark(i)

#order the database
orderDir()

#build up the base libarary first
dirTransverse("/lib")
dirTransverse("/usr/lib")

#parse /proc to compare with base libarary
procTransverse("/proc")
#getMaps("/proc"+"/"+"3965")

#mark used link
findNotUsedLink()
 
j=0
f2 = open("./usedlib.txt", "w+")
f = open("./notusedlib.txt", "w+")

for i in systemLibaryList:
	if not i.used:
		f.write(i.fullpath + "\n")	
		j +=1
	else:
		f2.write(i.fullpath+"\n")

f.close()
f2.close()

print( "total library:" + str(len(systemLibaryList)))
print( "Not used libary:" + str(j))


