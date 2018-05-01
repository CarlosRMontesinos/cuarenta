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
