for i in range(1, 300):
	try:
		input_file = open(str(i) + '.txt.ssplit.ccg.nps', 'r')
	except:
		pass
	output_file = open(str(i) + '_lemma.txt', 'w')
	for line in input_file:
		output_file.write(line)