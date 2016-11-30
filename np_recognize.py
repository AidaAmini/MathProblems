from file_refrence import file_refrence
from math_modifiers import math_modifiers
import sys


def find_unit_type(np1):
		return math_modifiers.check_for_unit(np1)


if __name__ =="__main__":
	data_start = int(sys.argv[1])
	data_end = int(sys.argv[2])
	mode = str(sys.argv[3])
	normalized_mode = int(sys.argv[4])
	file_path_refrence = file_refrence()
	file_lemma_suffix = '_lemma.txt'
	file_suffix = '.txt'

	if mode == 'type':
		if normalized_mode == 1:
			input_file = open(file_path_refrence.score_file_name_relevant_np_type_normalized, 'r')
		else:
			input_file = open(file_path_refrence.score_file_name_relevant_np_type, 'r')
	else:
		if normalized_mode == 1:
			input_file = open(file_path_refrence.score_file_name_relevant_np_entity_normalized, 'r')
		else:
			input_file = open(file_path_refrence.score_file_name_relevant_np_entity, 'r')

	res = input_file.readline()[:-1]
	# for i in range(data_start, data_end):
	seen_np = []
	index_list = []
	# if i in file_path_refrence.problematic_indexes:
	# 	continue
	question_strings_np = []
	if mode == 'type':
		input_noun = open(file_path_refrence.np_visualization_file_type ,'r')
		resulted_noun_file = open(file_path_refrence.relevant_np_type_after_classifier  + file_suffix,'w')	
	else:
		input_noun = open(file_path_refrence.np_visualization_file_entity ,'r')
		resulted_noun_file = open(file_path_refrence.relevant_np_entity_after_classifier + file_suffix,'w')

	for np in input_noun:
		words = np.split('\t')
		question_strings_np.append(words[0])
		index_list.append(words[1][:-1])
		# if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
		# 	question_strings_np.append(np[:-3].lower())
		# else:
		# 	question_strings_np.append(np[:-1].lower())
	# print question_strings_np
	last_seen_index = 0
	for i in range(0, len(question_strings_np)):
		np1 = question_strings_np[i]
		cur_index = index_list[i]
		if cur_index != last_seen_index:
			seen_np = []
			if mode == 'type':
				resulted_noun_file = open(file_path_refrence.relevant_np_type_after_classifier + str(cur_index)  + file_suffix,'w')		
			else:
				resulted_noun_file = open(file_path_refrence.relevant_np_entity_after_classifier + str(cur_index)  + file_suffix,'w')	
			last_seen_index = cur_index
			np_file = open(file_path_refrence.question_string_nps_relevant_np_type_path + str(cur_index) + file_lemma_suffix, 'r')
			for ex_np in np_file:
				ex_np = ex_np[:-1]
				if (len (ex_np.split(' ')) == 1)  and find_unit_type(ex_np) != '000':
					# print ex_np
					# print cur_index
					resulted_noun_file.write(ex_np + '\n')
					continue

		res = input_file.readline()[:-1]
		if res.startswith('1'):
			if np1 in seen_np:
				continue
			seen_np.append(np1)
			resulted_noun_file.write(np1 + '\n')

