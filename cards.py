import random

class Card():

	def __init__(self,sVal):
		self.sVal = sVal
		self.bLast = True

class Deck():

	def __init__(self):
		
		# Create card deck
		lVal = ["A","2","3","4","5","6","7","J","Q","K"]
		self.lCards = []
		
		for i in range(0,4):
			for j in lVal:				
				self.lCards.append( Card(j) )

	def num(self):
		return len(self.lCards)

	def shuffle(self):

		lTemp = []		

		while len(self.lCards) > 0:
			# Take a rand() card
			i = random.randint(0, len(self.lCards)-1 )
			# Append to temp list
			lTemp.append( self.lCards[i] )
			# Remove from current list
			self.lCards.remove( self.lCards[i] )
			# Set cur = temp

		self.lCards = lTemp

	def deal(self):
		lTemp = []

		iNumCardsToDeal = 5
		if len( self.lCards ) >= iNumCardsToDeal:
			for i in range(0,iNumCardsToDeal):
				lTemp.append( self.lCards.pop(0) )

		return lTemp

	def printCards(self):
		for i in self.lCards:
			print( i.sVal )

	def intToCardChar(self,iVal):
		# Cards in 40 look like this ["A","2","3","4","5","6","7","J","Q","K"]
		# This functions take an integer and maps in into it's corresponding char
		sCardStr = "NAN"
		if iVal > 0 and iVal < 11:
			if iVal == 1:
				sCardStr = "A"
			elif iVal == 8:
				sCardStr = "J"
			elif iVal == 9:
				sCardStr = "Q"
			elif iVal == 10:
				sCardStr = "K"
			else:
				sCardStr = str(iVal)
		return sCardStr
