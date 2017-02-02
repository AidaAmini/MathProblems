for i in range(1, 300):
	input_file = open(str(i) + '_lemma.eq', 'r')
	output_file = open(str(i) + '_lemma.txt', 'w')
	for line in input_file:
		output_file.write(line)