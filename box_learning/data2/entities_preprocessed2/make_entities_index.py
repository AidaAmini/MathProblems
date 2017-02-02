for i in range(300, 400):
	input_file = open(str(i) + '_lemma.ent', 'r')
	output_file = open(str(i) + '_lemma.txt', 'w')
	for line in input_file:
		output_file.write(line)
