for i in range(1, 300):
	input_file = open(str(i) + '.cat', 'r')
	output_file = open(str(i) + '.txt', 'w')
	for line in input_file:
		output_file.write(line)