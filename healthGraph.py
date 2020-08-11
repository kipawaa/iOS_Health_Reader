import matplotlib.pyplot as plt
import numpy as np
import os

# global variable telling the program to search local directory
directory = os.fsencode(".")

class dataEntry:
	def __init__(self, recordType, source, creation, start, end, value):
		self.recordType = recordType
		self.source = source
		self.created = creation
		self.start = start
		self.end = end
		self.value = value

	def out(self):
		# outputs the data contained in this dataEntry object
		return str("type:\t" + self.recordType + "\tsource:\t" + self.source + "\tcreated:\t" + self.created + "\tstart\t" + self.start + "\tend:\t" + self.end + "\tvalue:\t" + self.value)

	def duration(self):
		# returns the duration (start - end) of the health event in the format "Hours : Minutes : Seconds"
		start = self.start[self.start.index(" ") :].split(":")
		end = self.end[self.end.index(" ") :].split(":")

		hours = int(end[0]) - int(start[0])
		minutes = int(end[1]) - int(start[1])
		seconds = int(end[2]) - int(start[2])

		return str(hours) + " : " + str(minutes) + " : " + str(seconds)

# gets the health data out of inputFile and returns it as a list of dataEntry objects
def getData(inputFile):
	# opens the file with data
	dataFile = open(inputFile)
	
	# list for storing the data received
	data = []
	
	for line in dataFile:
		# determine if the current line is a data entry line
		if "Record type" in line:
			string = line
			string = string.split('" ')
	
			# initializes data values so that unfound values are easy to locate
			recordType = "N/A"
			source = "N/A"
			creation = "N/A"
			start = "N/A"
			end = "N/A"
			value = "N/A"
			
			# break the string containing the health data into a more use-able list
			for i in range(len(string)):
				numQuotes = 2
				if string[i] == '"':
					numQuotes += 1
	
				if string[i] == ' ' and numQuotes % 2 == 0:
					string.pop(i)
	
			# determine and copy the data of interest
			for i in string:
				if i.find('Record type') != -1:
					recordType = i[i.index('=') + 2 : -2]
				if i.find('sourceName') != -1:
					source = i[i.index('=') + 2:]
				if i.find('creationDate') != -1:
					creation = i[i.index('=') + 2 : i.index(' -')]
				if i.find('startDate') != -1:
					start = i[i.index('=') + 2 : i.index(' -')]
				if i.find('endDate') != -1:
					end = i[i.index('=') + 2 : i.index(' -')]
				if i.find('value') != -1:
					value = i[i.index('=') + 2 : i.rindex('"')]
			
			# copy the data from the variables into a dataEntry object
			entry = dataEntry(recordType, source, creation, start, end, value)
			
			# add the object to the list
			data.append(entry)
	
	# close the data file
	dataFile.close()

	# return the data
	return data

# takes a list of dataEntry objects and sorts them into a dictionary (recordType : list_of_corresponding_objects) by recordType
def sortData(data):
	sortedData = {}

	for entry in data:
		# creates a new entry in the dictionary for this entry's recordType if it hasn't yet been created
		if entry.recordType not in sortedData:
			sortedData[entry.recordType] = []

		sortedData[entry.recordType].append(entry)
	
	return sortedData

if __name__ == '__main__':
	# asks the user to input the name of the file containing the data of interest
	fileName = input("input the name of the file containing your health data: ")
	
	print("gathering data...")

	# collects the data from the file
	data = getData(fileName)
	
	print("data collected successfully")

	# sorts the data into a dictionary organized by recordType
	data = sortData(data)

	user = int(input("what would you like to do with this data?\n1: output raw data formatted for excel/sheets/numbers\n2: view graph of data types\n"))
	if (user == 1):
		print("outputting data...")
		for category in data:
			for entry in data[category]:
				print(entry.out())
		print("data output complete.")
	elif (user == 2):
		print("which data category would you like to view?")
		for i in range(len(data)):
			print(str(i) + ": " + list(data.keys())[i])
		
		dataChoice = int(input("enter your choice: "))
		plt.plot([i.value for i in data[list(data.keys())[dataChoice]]], [i.start for i in data[list(data.keys())[dataChoice]]], 'ro')
		plt.show()
		plt.close('all')
	print("program complete.")
