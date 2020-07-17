import pandas
import csv
import math

df_look_up = None
df_assen = None
CUTOFF = 5760.0


class ObservedObject:

	def __init__(self, a, w, h, ppf):
		#Average values used for classification
		self.width = w
		self.height = h
		self.area = a
		#List of values per frames
		self.ppf = ppf

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def getArea(self):
		return self.area

	def getPpf(self):
		return self.ppf

	def setWidth(self, w):
		self.width = w

	def setHeight(self, h):
		self.height = h

	def setArea(self, a):
		self.area = a

	def setPpf(self, ppf):
		self.ppf = ppf

	def calcAxisRatio(self):
		self.axisratio = self.height/self.width
		return self.axisratio

	def calcFullness(self):
		self.fullness = self.area/(self.width*self.height)
		return self.fullness

	def toString(self):
		zin = "Object met W = " + str(self.getWidth()) + "; H = " + str(self.getHeight()) + "; Area = " + str(self.getArea()) + "; Params = " + '\n' 
		"""for p in self.getPpf():
			zin += p.toString() """
		return zin

class ParamsPerFrame:
	def __init__(self, cx, cy, area, w, h, framenr):
		self.width = w
		self.height = h
		self.area = area
		self.cx = cx
		self.cy = cy
		self.framenr = framenr

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def getArea(self):
		return self.area

	def getCx(self):
		return self.cx

	def getCy(self):
		return self.cy

	def getFrameNr(self):
		return self.framenr

	def setWidth(self, w):
		self.width = w

	def setHeight(self, h):
		self.height = h

	def setArea(self, a):
		self.area = a

	def setCx(self,cx):
		self.cx = cx

	def setCy(self, cy):
		self.cy =cy

	def setFrameNr(self, f):
		self.framenr = f

	def calcX_RightBB(self):
		x_r = self.getCx() + self.getWidth()/2.0
		return x_r
	def calcX_LeftBB(self):
		x_l = self.getCx() - self.getWidth()/2.0
		return x_l
	def calcY_UpperBB(self):
		y_u = self.getCy() - self.getHeight()/2.0
		return y_u
	def calcY_DownBB(self):
		y_d = self.getCy() + self.getHeight()/2.0
		return y_d

	def toString(self):
		zin = "Parameters in Frame = " + str(self.getFrameNr()) + "; met Cx = "+ str(self.getCx()) + "; Cy = " + str(self.getCy()) + "; W = " + str(self.getWidth()) + "; H = " + str(self.getHeight()) + "; Area = " + str(self.getArea()) + '\n'
		return zin
	

def readDetectionsCSV(fn, objecten):
	#obj = ObservedObject(None , None, None, None)
	f = open(fn)
	ppf_lijst = []
	laatste_ppf_lijst = []
	lines = f.readlines()
	index_obj = 0
	for l in range(len(lines)):
		line= lines[l]
		if l ==0 or l ==1:
			continue		
		elif line == '\n':
			#print("skip")
			continue
		elif (lines[l-1] == '\n'):
			#Voeg gemiddelden toe aan het observed object				
			gem = line.split(",")
			gem[-1] = gem[-1].replace("\n","")
			obj = ObservedObject(float(gem[0]) , float(gem[1]), float(gem[2]), None)
			objecten.append(obj)
			
			#Voeg ppf_lijst toe aan vorig object
			if len(ppf_lijst) != 0:
				#print("lijst: ")
				#for p in ppf_lijst:
					#print(p.toString())
				objecten[index_obj -1].setPpf(ppf_lijst)
				laatste_ppf_lijst = ppf_lijst
				ppf_lijst = []

			index_obj += 1
			continue
		else :
			#Schrijf de ppf_lijst van een object
			param = line.split(",")
			param[-1] = param[-1].replace("\n","")
			#cx, cy, area, w, h, framenr
			ppf = ParamsPerFrame(float(param[0]),float(param[1]),float(param[2]),float(param[3]),float(param[4]),float(param[5]))
			ppf_lijst.append(ppf)
			continue

	#Toevoegen laatste  ppf lijst aan laatste object	
	objecten[-1].setPpf(laatste_ppf_lijst)
	
	f.close()
	return objecten
	

def convertCSV():
	#assen - axis en fullness	
	dfassen = pandas.read_csv('./Axis-202481590918158.csv')
	global df_assen 
	df_assen = dfassen
	print(df_assen)

	#look-up waarde
	f = open('./Histogram_202481590918158.csv','r')
	content = f.read()
	#print(content)
	lijst = content.replace(",{","").replace("{","").replace("}", '\n')
	#print(lijst)

	fw = open("./Histogram.csv", "w")
	header = ""
	for i in range(149):
		header += str(i) + ","
	header += str(149)
	header += '\n'

	fw.write(header)
	fw.write(lijst)
	fw.close()
	f.close()

	df = pandas.read_csv('./Histogram.csv')
	global df_look_up 
	df_look_up= df
	print(df_look_up)
	#print(df.size)
	#print(df.iloc[0,0])
	#print(df.columns)
	
def classify(obj):
	klassen = {"Car":0,"Bike":1,"Pedestrian":2,"Truck":3,"None":-1}
	print(obj.toString())
	full = obj.calcFullness()
	print("Fullness: " + str(full))
	axis = obj.calcAxisRatio()
	print("AxiRatio: " +str(axis))
	sqrtarea = math.sqrt(obj.getArea())

	"""print("Object met fullness: " + str(full) + '\n')
	print("Object met axisratio: " + str(axis) + '\n')
	print("Object met area: " + str(obj.getArea()) + '\n')
	print("Object met sqrtarea: " + str(sqrtarea) + '\n')"""

	global df_look_up
	global df_assen
	df = df_look_up
	dfa = df_assen

	xco =-1
	yco = -1
	
	# zoek waarde in look-up matrix mbv axis (y-as)(rijen)
	for y in range(dfa.shape[0]-1):
		if(dfa.iloc[y,0]<=axis<dfa.iloc[y+1,0]):
			yco = y
			break
	# zoek waarde in look-up matrix mbv fullness(x-as)(kolommen)
	for x in range(dfa.shape[0]-1):
		if(dfa.iloc[x,1]<=full<dfa.iloc[x+1,1]):
			xco = x
			break
	if(yco == -1 or xco == -1):
		klasse =-1
		print("OEPS")
	else: 
		# zoek klasse op mbv index
		#print("rij: " + str(yco) + " kolom: " + str(xco)) 
		klasse = df.iloc[yco,xco]
	if(sqrtarea>=CUTOFF):
		klasse = 3
	for key, value in klassen.items():
		if(klasse == value):
			print("Klasse: " + key + " met value: " + str(value))
			return key

def writeClassFileDetection(fn, img_frame, x_r, x_l, y_u, y_d):
	f = open(fn, "a")
	#confidence score is steeds 1 vanwege matrix
	#lijn = "<" + str(img_frame)+ "> "+ "<" + str(1)+ "> "+"<" + str(x_l)+ "> "+"<" + str(y_u)+ "> "+"<" + str(x_r)+ "> " +"<" + str(y_d)+ ">" + '\n'
	lijn = str(img_frame) +" "+ str(1)+ " " + str(x_l) + " " + str(y_u)+ " " + str(x_r)+ " " + str(y_d)+'\n'
	f.write(lijn)
	f.close()	

def main():
	convertCSV()
	#weggebruiker = ObservedObject(350,260,90000)
	#classify(weggebruiker)
	objecten = []
	objecten = readDetectionsCSV("./output_gem_appart_MAH00199_reduced.csv", objecten)
	#objecten = readDetectionsCSV("./output_gem_appart_thuis_pi4.csv", objecten)
	for obj in objecten:

		klasse = classify(obj)
		fn = "./Detecties/" + klasse + ".txt"
		for ppf in obj.getPpf():
			x_r = ppf.calcX_RightBB()
			x_l = ppf.calcX_LeftBB()
			y_u = ppf.calcY_UpperBB()
			y_d = ppf.calcY_DownBB()
			nr = str(int(ppf.getFrameNr())).zfill(6)
			img_frame = "frame_"+ nr
			writeClassFileDetection(fn, img_frame, x_r, x_l, y_u, y_d)
		
			
		#print(obj.toString())
	print("Aantal objecten: " + str(len(objecten)))
	#classify(0.8,0.5)

main()

