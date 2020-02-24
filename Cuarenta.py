import cards
import trainingfile
import random
import sys
from PyQt4 import QtCore, QtGui, uic
import numpy as np # Import required libraries
import keras # Keras specific


qtCreatorFile = "Cuarenta.ui" # Enter the .ui file name here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# Main objects
# btPlayCard
# card_deck_X
# lbCompCards
# lbMyCards
# lbTable
# lePlayCard
# teDebugWin

# lbCompEarnedCards
# lbCompPoints
# lbPlayerEarnedCards
# lbPlayerPoints

TRAINIG_FLAG = True
COMP_TURN_FLAG = False

# UI class
class MyApp(QtGui.QMainWindow, Ui_MainWindow):

	# Declare variables
	oCardDeck = cards.Deck()
	loPlayerCards = []
	loCompCards = []
	loTableCards = []
	bCompTurn = COMP_TURN_FLAG
	bTraining = TRAINIG_FLAG
	iCardCount = 0
	iCompPoints = 0
	loCompEarnedCards = []
	iPlayerPoints = 0
	loPlayerEarnedCards = []
	sNextCard = "" # For training purposes
	oTrainingFile = trainingfile.TrainingFile()
	oModel = keras.models.load_model("cuarenta_model.ml") # Load model

	def __init__(self):

		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		# Create all connections
		self.lePlayCard.textChanged.connect(self.CheckCardInput)

		# Init Variables
		self.initVars()

		# Shuffle and Deal Cards
		self.oCardDeck.shuffle()
		self.loPlayerCards = self.oCardDeck.deal()
		self.loCompCards = self.oCardDeck.deal()

		# Update UI with cards
		self.lbMyCards.setText( self.CardListToString(self.loPlayerCards) )

	def closeEvent(self, event):
		print "closing Cuarenta"
		self.oTrainingFile.pushToFiles()

	def initVars(self):
		
		self.oCardDeck = cards.Deck()
 		self.loPlayerCards = []
		self.loCompCards = []
		self.loTableCards = []
		self.bCompTurn = COMP_TURN_FLAG
		self.bTraining = TRAINIG_FLAG
		self.iCardCount = 0
		self.iCompPoints = 0
		self.loCompEarnedCards = []
		self.iPlayerPoints = 0
		self.loPlayerEarnedCards = []
		sNextCard = "" # For training purposes

#	def keyPressEvent(self, event):
#		if event.key() == QtCore.Qt.Key_Return:
			# If the user hit the Enter/Return key trigger GameRound()
#			self.GameRound()

	def CheckCardInput(self):

		# Check card is within card set
		bCardInSet = self.IsCardInSet(self.loPlayerCards, self.lePlayCard.text().toUpper()) 
		
		# If the card is in the set play game
		if bCardInSet == True:
			
			#Play game
			self.GameRound()

		else:
			# Clear content of the lable 
			self.lePlayCard.clear()

			# Indicate the user of the problem
			#print("Card NOT in card set")

	def GameRound(self):

		# Player's turn
	   	self.Play()

		# Computer's turn
		self.Play()

	def Play(self):

		# For training purposes
		# Get table and computer cards
		sTableCards = self.CardListToString(self.loTableCards)
		sCompCards = self.CardListToString(self.loCompCards)
		sPlayerCards = self.CardListToString(self.loPlayerCards)

		# IF comp turn
		if self.bCompTurn:
#			print("computer turn")
			# IF training
			if self.bTraining:

				# Create input for the ML model: Table + Computer cards vector
				# sInput_x = sTableCards + sCompCards # ([[x,x,...,x]])
				sInput_x = self.oTrainingFile.strToCSV(sTableCards,sCompCards)
				npTempInput_x = np.fromstring(sInput_x, dtype=int, sep=',')
				npInput_x = npTempInput_x.reshape(1,npTempInput_x.size)
				
				# Predict what card to put down based on the highest priority
				npOutput_Y = self.oModel.predict_proba(npInput_x)
				#print("npOutput_Y")
				#print(npOutput_Y)	
				iNextCard = np.argmax(npOutput_Y) # Next index of the next card is the Next Card.
				sNextCard = self.oCardDeck.intToCardChar(iNextCard) # Convert the index card into 40 string card. This includes J, Q, K
				# Get the index where the next card is stored
				#print("sNextCard: " + sNextCard)
				iCardIndex = -1
				iCount = -1
				for i in self.loCompCards:
					iCount = iCount + 1
					print(i.sVal)					
					if i.sVal == sNextCard:
						iCardIndex = iCount						
						break
				if iCardIndex != -1:

					print("Picking a card based on PROB()")		
					oTempCompCard = self.loCompCards[iCardIndex]
					# Append to temp list
					self.loTableCards.append( oTempCompCard )
					# Store the card for training purposes
					# sNextCard = self.loCompCards[iNextCard].sVal.upper()

					# Remove from current list
					self.loCompCards.remove( self.loCompCards[iCardIndex] )
				else:
				    	# List does not contain value			
	
					print("Picking a RAND() card")					
					# Select rand() next card from comp cards and add to table cards
					i = random.randint(0, len(self.loCompCards)-1 )
					oTempCompCard = self.loCompCards[i]
								
					# Append to temp list
					self.loTableCards.append( oTempCompCard )
					# Store the card for training purposes
					sNextCard = self.loCompCards[i].sVal.upper()

					# Remove from current list
					#print("loCompCards[i]" + self.loCompCards[i].sVal)
					self.loCompCards.remove( self.loCompCards[i] )
				
			# ELSE
			else:
				# Evaluate learning model to select next card
				print("Evaluate learning model to select next card")	
		# ELSE
		else:
			# Take user's card and add to the table
			sPlayersCard = str(self.lePlayCard.text()).upper()
			# Store the card for training purposes
			sNextCard = sPlayersCard
			# Append card to table list
			oTempCard = cards.Card( sPlayersCard )			
			self.loTableCards.append( oTempCard )
			# Remove temp card from my cards
			for i in self.loPlayerCards:
				if i.sVal == oTempCard.sVal:
					self.loPlayerCards.remove( i )
					break				
 
		# Increment card counter
		self.iCardCount = self.iCardCount + 1

		# Apply 40 rules to table cards
		iPointsEarned, loCardsEarned = self.Apply40Rules()

		# Clear the last-card flag from the now last card on the table
#		iLen = len( self.loTableCards )		
#		if iLen >= 1:
#			self.loTableCards[iLen-1].bLast = False

		# Grant points and cards
#		print( iPointsEarned )
#		print( self.CardListToString(loCardsEarned) )

		if self.bCompTurn:
			self.iCompPoints = self.iCompPoints + iPointsEarned
			self.loCompEarnedCards.extend(loCardsEarned)
		else:
			self.iPlayerPoints = self.iPlayerPoints + iPointsEarned
			self.loPlayerEarnedCards.extend(loCardsEarned)

		# Store data for training purposes
		if TRAINIG_FLAG == True and iPointsEarned > 0:
			if self.bCompTurn:
				self.oTrainingFile.pushToStruct(sTableCards,sCompCards,sNextCard )
			else:
				self.oTrainingFile.pushToStruct(sTableCards,sPlayerCards,sNextCard )

		# IF there is a winner
			# Declare winner
			# Re-initialize game
		# ELSE/home/roboticsphd/Documents/Projects/qtProjects
			# toggle computer turn flag
		#print(self.bCompTurn)
		self.bCompTurn = not self.bCompTurn

		# Update UI
		self.lePlayCard.clear()
	#	self.lbCompCards.clear()
		self.lbMyCards.clear()
		self.lbTable.clear()
	
	#	self.lbCompCards.setText( self.CardListToString(self.loCompCards) )
		self.lbMyCards.setText( self.CardListToString(self.loPlayerCards) )
		self.lbTable.setText( self.CardListToString(self.loTableCards) )

		self.lbCompPoints.setText( str(self.iCompPoints)  )
		#print(self.CardListToString(self.loCompEarnedCards ))
		self.lbCompEarnedCards.setText( self.CardListToString(self.loCompEarnedCards ) )
		self.lbPlayerPoints.setText( str(self.iPlayerPoints) )
		#print(self.CardListToString(self.loPlayerEarnedCards ))
		self.lbPlayerEarnedCards.setText( self.CardListToString(self.loPlayerEarnedCards ) )

		# Check if players ran out of cards
#		print( "iCardCount: " + str(self.iCardCount) )	
		if self.iCardCount == 10 or self.iCardCount == 20 or self.iCardCount == 30:
			self.loPlayerCards = self.oCardDeck.deal()
			self.loCompCards = self.oCardDeck.deal()
		#	self.lbCompCards.setText( self.CardListToString(self.loCompCards) )
			self.lbMyCards.setText( self.CardListToString(self.loPlayerCards) )
			self.lbTable.setText( self.CardListToString(self.loTableCards) )
		elif self.iCardCount == 40:

			# Clean all variables
			self.initVars()

			# Start all over
			self.oCardDeck.shuffle()
			self.loPlayerCards = self.oCardDeck.deal()
			self.loCompCards = self.oCardDeck.deal()
		#	self.lbCompCards.setText( self.CardListToString(self.loCompCards) )
			self.lbMyCards.setText( self.CardListToString(self.loPlayerCards) )
			self.lbTable.setText( self.CardListToString(self.loTableCards) )

	def IsCardInSet(self,loCardSet, sCardToCheck):
		
		#scan all card's .val to check
		for i in loCardSet:
			if i.sVal == sCardToCheck:
				return True

		return False	

	def CardListToString(self,loCards):
		sTemp = ""

		for i in loCards:
			sTemp = sTemp + " " + i.sVal

		return sTemp

	def Apply40Rules(self):
		
		# Local variables
		iRetPoint = 0
		loCardsEarned = []
		iCardsOnTable = len(self.loTableCards)

		# Ensure there are at least 2 cards on the table
		if iCardsOnTable >= 2:
			# Test for immediate pair
			sLastCard = self.loTableCards[iCardsOnTable-1].sVal 
			sSecLastCard = self.loTableCards[iCardsOnTable-2].sVal  
			if sLastCard == sSecLastCard:  

				# Check if the match was an immediate match to award points
				if self.loTableCards[iCardsOnTable-2].bLast:
					iRetPoint = 2

				# Remove cards from the table
				loCardsEarned.append( self.loTableCards.pop() )
				loCardsEarned.append( self.loTableCards.pop() )

				# Clear the last-card flag from the now last card on the table
				#iLen = len( self.loTableCards )		
				#if iLen >= 1:
				#	self.loTableCards[iLen-1].bLast = False
			else:
				# Clear the last flag from the now second to last card
				iLen = len( self.loTableCards )				
				self.loTableCards[iLen-2].bLast = False
		
		# If we've hit the end of a hand clear the last flag from the now last card 
		if self.iCardCount == 10 or self.iCardCount == 20 or self.iCardCount == 30: 
			# Clear the last-card flag from the now last card on the table
			iLen = len( self.loTableCards )		
			if iLen >= 1:
				self.loTableCards[iLen-1].bLast = False

			# Test for immediate pair + escalera

			# Test for escalera


		# Return points earned and cards earned
		return( iRetPoint, loCardsEarned )

# Main code
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())
