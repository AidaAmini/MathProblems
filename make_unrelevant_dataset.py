def make_unrelevant_dataset():
	pair_file = open('pair.txt', 'r')
	score_file = open('s_norm_joint_pair.txt')
	non_relevant_file = open('non_relevant_pairs.txt','w')
	pair_line = pair_file.readline()
	score_line= score_file.readline()
	while pair_line != '':
		if pair_line.startswith('problem:'):
			non_relevant_file.write(pair_line)
			pair_line = pair_file.readline()
			if pair_line == '':
				break
		if score_line.startswith('1'):
			socre_parts = score_line.split(' ')
			# print socre_parts[1]
			if float(socre_parts[1]) < 1:
				non_relevant_file.write(pair_line)
		score_line = score_file.readline()
		pair_line = pair_file.readline()

def find_eq_coverage():
	pair_file = open('non_relevant_pairs.txt', 'r')
	pair_line = pair_file.readline()
	total_eq_found = 0
	total_eq_pair = 0
	extra_pair_fount = 0
	while pair_line != '':
		pair_line = pair_line[:-1]
		if pair_line.startswith('problem:'):
			question_index = pair_line.split(' ')[1]
			eq_list = read_equvalence("../../data/equivalence/" + question_index + '_lemma.eq')
			total_eq_pair = total_eq_pair + len(eq_list)/2
			pair_line= pair_file.readline()
			problem_pair_find = []

			while pair_line != '' and (not pair_line.startswith('problem:')):
				pair_line = pair_line[:-1]
				problem_pair_find.append(pair_line)
				pair_line = pair_file.readline()
						
			problem_correct_found = 0
			for problem_pair in problem_pair_find:
				if problem_pair in eq_list:
					total_eq_found = total_eq_found + 1
				else:
					extra_pair_fount = extra_pair_fount + 1
	print extra_pair_fount
	print total_eq_found
	print total_eq_pair


def read_equvalence(file_name):
	resulted_list = []	
	input_file = open(file_name, 'r')
	for line in input_file:
		line = line[:-2]
		if line == '':
			break
		resulted_list.append(line)
		parts = line.split('	')
		resulted_list.append(parts[1] + '	' + parts[0])
	return resulted_list


make_unrelevant_dataset()
find_eq_coverage()