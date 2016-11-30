def make_np_visual_file(start_index, end_index):
	output_file = open('np_visual.txt','w')
	for i in range(start_index, end_index):
		input_file = open('data/np_pos/' + str(i) + '_lemma.txt')
		for line in input_file:
			output_file.write(line)

make_np_visual_file(150, 248)