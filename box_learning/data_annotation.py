from file_refrence import file_refrence

file_path_refrence = file_refrence()
def make_whole_problem_file(start_index, end_index):
	output_file = open('data/all_problem_no_lemma.txt', 'w')
	for i in range(start_index, end_index):
		if i in file_path_refrence.problematic_indexes:
			continue
		output_file.write("problem " + str(i) + '\n')
		input_file = open(file_path_refrence.whole_question_path + str(i) + '.txt', 'r')
		line = input_file.readline()
		output_file.write(line)

make_whole_problem_file(0, 550)