def foo():
		#open the output file
		fp = open(reportFile, 'w+')

		#write the header
		fp.write('<html><body><h1>Scores</h1><br><table border ="1">')
		fp.write('<tr><td>Total Score</td><td>' + str(overallScore) + '</td></tr>')
		fp.write('<tr><td>Items copied</td><td>' + str(scores[0]) + '</td></tr>')
		fp.write('<tr><td>Unique Items</td><td>' + str(scores[1]) + '</td></tr>')
		fp.write('<tr><td>Repeated Items</td><td>' + str(scores[2]) + '</td></tr>')
		fp.write('<tr><td>Number of Holes</td><td>' + str(scores[3]) + '</td></tr>')
		fp.write('<tr><td>Number of Misplaced Items</td><td>' + str(scores[4]) + '</td></tr></table>')

		#write the header for their copied text
		fp.write('<h1>Copied Text</h1><br>')

		#write the copied text to the file
		for curCopy in copyLines:
			fp.write(curCopy + '<br>')

		#pop the end of the hitCounter so we only output the part of the text they copied
		while hitCounter and hitCounter[-1] == 0:
			hitCounter.pop()

		#write the header for the matching text
		fp.write('<br><h1>Matching Text</h1><br>')
		fp.write('<font color = "black">Correctly copied</font><br>')
		fp.write('<font color = "red">Missed items</font><br>')
		fp.write('<font color = "green">Repeated items</font><br><br>')

		#init the counter of the index
		indexCounter = 0

		#cycle the original lines
		for curLine in self.originalLines:
			#cycle the words in this line
			for curItem in self.getItemsFromLine(curLine):
				#check that we are still in the copied part
				if indexCounter >= len(hitCounter):
					break

				#misses are red
				if hitCounter[indexCounter] == 0:
					fp.write('<font color = "red">')

				#hits are black
				if hitCounter[indexCounter] == 1:
					fp.write('<font color = "black">')

				#repeats are green
				if hitCounter[indexCounter] > 1:
					fp.write('<font color = "green">')

				#write the word
				fp.write(curItem + self.spaceBetweenItems)

				#increment the index Counter
				indexCounter += 1

				#close the font tag
				fp.write('</font>')

			#write a newline
			fp.write('<br>')

		#close the last font tag and the file
		fp.write('</font></body></html>')
		fp.close
