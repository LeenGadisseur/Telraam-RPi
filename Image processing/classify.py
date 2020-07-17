import pandas
import csv

df_look_up = None
df_assen = None
CUTOFF = 57600

class ObservedObject:
	def __init__(self, w, h, a):
		self.width = w
		self.height = h
		self.area = a

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def getArea(self):
		return self.area

	def calcAxisRatio(self):
		self.axisratio = self.width/self.height
		return self.axisratio

	def calcFullness(self):
		self.fullness = self.area/(self.width*self.height)
		return self.fullness

	

def convertCSV():
	#assen - axis en fullness	
	dfassen = pandas.read_csv('./Axis-202481590918158.csv')
	global df_assen 
	df_assen = dfassen
	print(df_assen)

	#look-up waarde
	f = open('./Histogram_202481590918158.csv','r')
	content = f.read()
	print(content)
	lijst = content.replace(",{","").replace("{","").replace("}", '\n')
	print(lijst)

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
	
def classify(full, axis):
	klassen = {"Car":0,"Bike":1,"Pedestrian":2,"Truck":3,"Geen klasse":-1}

	global df_look_up
	global df_assen
	df = df_look_up
	dfa = df_assen

	# zoek waarde in look-up matrix mbv axis (x-as)
	for x in range(dfa.shape[0]-1):
		if(dfa.iloc[x,0]<=axis<dfa.iloc[x+1,0]):
			xco = x
			break
	# zoek waarde in look-up matrix mbv fullness(y-as)	
	for y in range(dfa.shape[0]-1):
		#print(dfa.iloc[y,1])
		if(dfa.iloc[y,1]<=full<dfa.iloc[y+1,1]):
			yco = y
			break

	# zoek klasse op mbv index
	print("rij: " + str(yco) + " kolom: " + str(xco)) 
	klasse = df.iloc[yco,xco]
	
	for key, value in klassen.items():
		if(klasse == value):
			print("Klasse: " + key + " met value: " + str(value))

	

def main():
	convertCSV()
	#classify(0.8,0.5)

main()

