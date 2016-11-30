for i in range(1, 370):
	input_file = open(str(i) + '_lemma.par', 'r')
	output_file = open(str(i) + '_lemma.txt', 'w')
	for line in input_file:
		output_file.write(line)
	open(str(i) + ".par", 'w')