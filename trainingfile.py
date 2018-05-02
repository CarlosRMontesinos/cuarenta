import io
import datetime

class TrainingFile:

	lData = []

	oDate = datetime.datetime.now()
	print(oDate)	

	sFilePath = "../../Data/"
	sFileTimeStamp = str(oDate.year) + str(oDate.month) + str(oDate.day) + str(oDate.hour) + str(oDate.minute) + str(oDate.second) 	
	sTestFileName = "Test_" + sFileTimeStamp + ".csv"
	sTrainFileName = "Train_" + sFileTimeStamp + ".csv"
	sTestFileFullPath = sFilePath + sTestFileName
	sTrainFileFullPath = sFilePath + sTrainFileName

	sFileName = str(oDate.year) + str(oDate.month) + str(oDate.day) + str(oDate.hour) + str(oDate.minute) + str(oDate.second) + ".csv"
	sFileFullPath = sFilePath + sFileName
	
	# Create file
#	oFile = io.open(sFileFullPath,"w+")
#	oFile.write(unicode("TableCards,CompCards,NextCompCards,PointsEarned\n"))
#	print(sFileFullPath)	
#	oFile.close()

#	def __init__(self):
		
		# Create column titles
		#self.oFile.write(unicode("TableCards,CompCards,NextCompCards,PointsEarned"))
#		print("init()")

	def push(self,sTableCards,sCompCards,sNextCompCard,sPointsEarned):
		
		# Parameter definiions during the training stage
		# sTableCards -> Tables on the table before the computer draws next card
		# sCompCards -> Computers cards before the computer draws next card
		# sNextCompCard -> Card drawn by the computer using the rand() function
		# sPointsEarned -> Points earned after the table has been evaluated
		sDataLine = sTableCards + "," + sCompCards + "," + sNextCompCard + "," + sPointsEarned + "\n"
		oFile = io.open(self.sFileFullPath,"a")
		oFile.write(unicode(sDataLine))
		oFile.close()

	def pushToStruct(self,sTableCards,sCompCards,sNextCompCard,sPointsEarned):
		
		# Parameter definiions during the training stage
		# sTableCards -> Tables on the table before the computer draws next card
		# sCompCards -> Computers cards before the computer draws next card
		# sNextCompCard -> Card drawn by the computer using the rand() function
		# sPointsEarned -> Points earned after the table has been evaluated
		self.lData.append( sTableCards + "," + sCompCards + "," + sNextCompCard + "," + sPointsEarned )

	def pushToFiles(self):
		
		# Split data into training and test 70%/30%
		# Print Training Data
#		iSplit70 = int( len(self.lData) * 0.7)
#		iSplit30 = len(self.lData) - iSplit70

#		if iSplit70 >= 7:
			# Print Training Data
#			oFile = io.open(self.sTrainFileFullPath,"w+")
			# Print first line (# Data Rows, # Label Columns) 
#			oFile.write( unicode( str(iSplit70) + ",3\n") )
#			for sDataLine in self.lData[0:iSplit70-2]:
#	  			oFile.write( unicode( sDataLine + "\n") )
#			oFile.close()		

			# Print Testing Data
#			oFile = io.open(self.sTestFileFullPath,"w+")
			# Print first line (# Data Rows, # Label Columns) 
#			oFile.write( unicode( str(iSplit30) + ",3\n") )
#			for sDataLine in self.lData[iSplit70-1: len(self.lData)-1]:
#	  			oFile.write( unicode( sDataLine + "\n") )
#			oFile.close()

		iNumOfLabels = 3
		if len(self.lData) > 0:
			# Print Training Data
			oFile = io.open(self.sTrainFileFullPath,"w+")
			# Print first line (# Data Rows, # Label Columns) 
			oFile.write( unicode( str( len(self.lData) ) + "," + str(iNumOfLabels) + "\n") )
			for sDataLine in self.lData:
	  			oFile.write( unicode( sDataLine + "\n") )
			oFile.close()	

		else:
			print("### NOT ENOUGH DATA COLLECTED TO CREATE FILES ###")
