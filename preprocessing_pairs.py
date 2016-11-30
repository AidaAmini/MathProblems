def read_pairs(file_name):
	res = []
	input_file = open(file_name, 'r')
	for line in input_file:
		line = line[:-2]
		if line == '':
			break
		parts = line.split('	')
		res.append(parts[0].lower())
		res.append(parts[1].lower())
	return res

def omit_number_beginning_expect_question(word):
	result_list = []
	# for word in question_strings_np:
	parts = word.split(' ')
	if '-' in word:
		parts = word.split('-')		
	# comma_dot_flag = False
	flag = False
	written_number_list = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'hundered']
	if parts[0] in written_number_list:
		res_word = ''
		for i in range(1, len(parts)):
			res_word = res_word + parts[i] + ' '
		return res_word[:-1]

	for char in parts[0]:
		if not (char >='0' and char <= '9') :				
			if (char ==',' or char == '.'):
				continue
			flag = True
	if flag == False:
		res_word = ''
		for i in range(1, len(parts)):
			res_word = res_word + parts[i] + ' '
		return res_word[:-1]

	return word


if __name__ =="__main__":
	final_pairs = []
	input_dir = 'data/parallels2/'
	output_dir = "data/parallel_types2/"
	suffix = "_lemma.txt"
	for i in range(1, 400):
		print i
		final_pairs = []
		question_strings_np = read_pairs(input_dir + str(i) + suffix)
		output_file = open(output_dir + str(i) + suffix, 'w')
		for j in range(0, len(question_strings_np)):
			question_strings_np[j] = omit_number_beginning_expect_question(question_strings_np[j])
		for j in range(0, len(question_strings_np)):
			if question_strings_np[j] != question_strings_np[j+1]:
				if not question_strings_np[j] + "\t" + question_strings_np[j+1] in final_pairs:
					final_pairs.append(question_strings_np[j] + "\t" + question_strings_np[j+1])
			j = j+1
			if j == len(question_strings_np) - 1:
				break
		for j in range(0, len(final_pairs)):
			output_file.write(final_pairs[j] + '\n')


			







