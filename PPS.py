import json

class PPS:
	ppsList = []
	def getNewPosition(self,position):
		if position > len(self.ppsList) + 1:
			return "ERROR"
		elif len(self.ppsList) == 0:
			return 1
		elif position == len(self.ppsList) + 1:
			return self.ppsList[len(self.ppsList)-1][0] + 1	
		elif position==1:
			return (float) (self.ppsList[position-1][0])/2
		else:
			return (float)(self.ppsList[position-2][0] + self.ppsList[position-1][0])/2

	def insertCharacter(self,s,position):
		pos = self.getNewPosition(position)
		self.ppsList.insert(position - 1,[pos,s])
		return pos

	def deleteCharacter(self,s,position):
		posReturn = self.ppsList[position - 1][0]
		del self.ppsList[position - 1]
		return posReturn

	def print_pps(self):
		for obj in self.ppsList:
			print obj[1] + " " + str(obj[0])
		print "============"
	def get_pps(self):
		return self.ppsList
	def clear(self):
		del self.ppsList[:]
	def constructPPSFromDB(self,string):
		self.clear()
		for p,c in enumerate(string):
			self.insertCharacter(c,p+1)

# x = PPS()
# x.insertCharacter('a',1)
# x.print_pps()
# x.insertCharacter('b',2)
# x.print_pps()
# x.insertCharacter('c',3)
# x.print_pps()
# x.insertCharacter('d',4)
# x.print_pps()
# x.insertCharacter('f',2)
# x.print_pps()
# x.deleteCharacter('b',3)
# x.print_pps()
# x.insertCharacter('f',3)
# x.print_pps()


