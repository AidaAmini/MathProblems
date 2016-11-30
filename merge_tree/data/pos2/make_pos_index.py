for i in range(0, 300):
	input_file = open(str(i) + '_lemma.pos', 'r')
	output_file = open(str(i) + '_lemma.txt', 'w')
	for line in input_file:
		output_file.write(line)
