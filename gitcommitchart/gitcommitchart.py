
import os

''' output gittxt first '''
commitFile="/mnt/40g/python/practice/gitcommitchart/commits.txt"
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

	
'''Generate the html file'''
header='''
<html>
<head>
<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.css">
<script src="https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.js"> </script>

</head>
'''

body1='''
<body><h1>It works!</h1>
<p>This is the default web page for this server.</p>
<p>The web server software is running but no content has been added, yet.</p>
'''

chart1='''
<div class="ct-chart ct-perfect-fourth"></div>
'''

name=[]
commit=[]
max= 10
for i in ldbs:
	name.append(i[0])
	commit.append(i[1])
	max -= 1
	if max == 0:
		break

chart2='''
<script>
var data1 = {
  labels: ''' + str(name) + ''',
  series: [
	''' + str(commit) + '''
  ]
};

var options1 = {
  width: 900,
  height: 700
};

new Chartist.Line('.ct-chart', data1, options1);

</script>


<p>The web server software is running but no content has been added, yet.</p>

<div class="ct-chart2 ct-perfect-fourth"></div>

<script>
var data2 = {
  labels: ''' + str(name) + ''',
  series: [
	''' + str(commit) + '''
  ]
};

options2 = {
  seriesBarDistance: 400,
  reverseData: true,
  horizontalBars: true,
  axisY: {
    offset: 70
  }
}


new Chartist.Bar('.ct-chart2', data2, options2 );
</script>

'''

body2='''
</body>
</html>
'''

f = open("./index.html","w+")
if f is not None:
	f.write(header)
	f.write(body1)
	f.write(chart1)
	f.write(chart2)
	f.write(body2)




