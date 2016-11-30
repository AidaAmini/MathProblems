for i in range(0, 300):
	try:
		input_file = open(str(i) + '.txt.ssplit.ccg.nps', 'r')
	except:
		pass
	output_file = open(str(i) + '_lemma.txt', 'w')
	for line in input_file:
		output_file.write(line)
