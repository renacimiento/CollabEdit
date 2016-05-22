class PPS:
	ppsList = []
	def getNewPosition(self,position):
		if position > len(self.ppsList) + 1:
			return "ERROR"
		elif len(self.ppsList) == 0:
			return 1
		elif position == len(self.ppsList) + 1:
			return self.ppsList[len(self.ppsList)-1][0] + 1	
		else: 
			return (float)(self.ppsList[position-2][0] + self.ppsList[position-1][0])/2

	def insertCharacter(self,s,position):
		self.ppsList.insert(position - 1,[self.getNewPosition(position),s])

	def deleteCharacter(self,s,position):
		del self.ppsList[position - 1]

	def print_ppsList(self):
		for obj in self.ppsList:
			print obj[1] + " " + str(obj[0])
		print "============"
x = PPS()
x.insertCharacter('a',1)
x.print_pps()
x.insertCharacter('b',2)
x.print_pps()
x.insertCharacter('c',3)
x.print_pps()
x.insertCharacter('d',4)
x.print_pps()
x.insertCharacter('f',2)
x.print_pps()
x.deleteCharacter('b',3)
x.print_pps()
x.insertCharacter('f',3)
x.print_pps()


