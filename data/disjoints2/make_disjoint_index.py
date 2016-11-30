for i in range(0, 400):
	input_file = open(str(i) + '_lemma.dis', 'r')
	output_file = open(str(i) + '_lemma.txt', 'w')
	for line in input_file:
		output_file.write(line)
	# open(str(i) + ".dis", 'w')