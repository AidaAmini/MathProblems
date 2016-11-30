for i in range(0, 300):
	input_file = open(str(i) + '.txt.ssplit.ccg.nps', 'r')
	output_file = open(str(i) + '.txt', 'w')
	for line in input_file:
		output_file.write(line)
