for i in range(300, 400):
	input_file = open(str(i) + '.txt.ssplit.ccg', 'r')
	output_file = open(str(i) + '.txt', 'w')
	for line in input_file:
		output_file.write(line)
