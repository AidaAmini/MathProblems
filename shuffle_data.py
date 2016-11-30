import sys 
import random
from file_refrence import file_refrence

def shuffle_files(start_index, end_index):
	file_lemma_suffix = '_lemma.txt'
	file_lemma_suffix_story = 'story_lemma.txt'
	file_suffix = '.txt'
	file_path_refrence = file_refrence()
	index_list = []
	for i in range(start_index, end_index):
		if i in file_path_refrence.problematic_indexes:
			continue
		index_list.append(i)
	random.shuffle(index_list)
	print len(index_list)
	i = -1
	# print index_list
	for j in range(0, len(index_list)):
		# print i
		i = i+1
		if i in file_path_refrence.problematic_indexes:
			print 'jjjjjjjjj'
			print i
			i = i+1
			while i in file_path_refrence.problematic_indexes:
				print 'whillleeee'
				print i
				i = i+1
		file_index = index_list[j]

		input_file = open(file_path_refrence.whole_question_path[:-1] + '2/' + str(file_index) + file_suffix)
		output_file = open(file_path_refrence.whole_question_path + str(i) + file_suffix, 'w')
		for line in input_file:
			output_file.write(line) 
		input_file = open(file_path_refrence.whole_question_path[:-1] + '2/' + str(file_index) + file_lemma_suffix)
		output_file = open(file_path_refrence.whole_question_path + str(i) + file_lemma_suffix, 'w')
		for line in input_file:
			output_file.write(line) 

		# input_file = open(file_path_refrence.question_strings_path[:-1] + '2/' + str(i) + file_suffix)
		# output_file = open(file_path_refrence.question_strings_path + str(i) + file_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 
		input_file = open(file_path_refrence.question_strings_path[:-1] + '2/' + str(file_index) + file_lemma_suffix)
		output_file = open(file_path_refrence.question_strings_path + str(i) + file_lemma_suffix, 'w')
		for line in input_file:
			output_file.write(line) 

		# input_file = open(file_path_refrence.ccg_parse_path[:-1] + '2/' + str(i) + file_suffix)
		# output_file = open(file_path_refrence.ccg_parse_path + str(i) + file_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 
		input_file = open(file_path_refrence.ccg_parse_path[:-1] + '2/' + str(file_index) + file_lemma_suffix)
		output_file = open(file_path_refrence.ccg_parse_path + str(i) + file_lemma_suffix, 'w')
		for line in input_file:
			output_file.write(line) 

		# input_file = open(file_path_refrence.gold_entity_path[:-1] + '2/' + str(i) + file_suffix)
		# output_file = open(file_path_refrence.gold_entity_path + str(i) + file_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 
		input_file = open(file_path_refrence.gold_entity_path[:-1] + '2/' + str(file_index) + file_lemma_suffix)
		output_file = open(file_path_refrence.gold_entity_path + str(i) + file_lemma_suffix, 'w')
		for line in input_file:
			output_file.write(line) 

		# input_file = open(file_path_refrence.gold_type_path[:-1] + '2/' + str(i) + file_suffix)
		# output_file = open(file_path_refrence.gold_type_path + str(i) + file_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 
		input_file = open(file_path_refrence.gold_type_path[:-1] + '2/' + str(file_index) + file_lemma_suffix)
		output_file = open(file_path_refrence.gold_type_path + str(i) + file_lemma_suffix, 'w')
		for line in input_file:
			output_file.write(line) 

		# input_file = open(file_path_refrence.question_string_nps_relevant_np_type_path[:-1] + '2/' + str(i) + file_suffix)
		# output_file = open(file_path_refrence.question_string_nps_relevant_np_type_path + str(i) + file_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 
		input_file = open(file_path_refrence.question_string_nps_relevant_np_type_path[:-1] + '2/' + str(file_index) + file_lemma_suffix)
		output_file = open(file_path_refrence.question_string_nps_relevant_np_type_path + str(i) + file_lemma_suffix, 'w')
		for line in input_file:
			output_file.write(line) 
		
		input_file = open(file_path_refrence.np_pos_path[:-1] + '2/' + str(file_index) + file_lemma_suffix)
		output_file = open(file_path_refrence.np_pos_path + str(i) + file_lemma_suffix, 'w')
		for line in input_file:
			output_file.write(line) 

		input_file = open(file_path_refrence.np_pos_path[:-1] + '2/' + str(file_index) + file_suffix)
		output_file = open(file_path_refrence.np_pos_path + str(i) + file_suffix, 'w')
		for line in input_file:
			output_file.write(line) 

		# input_file = open(file_path_refrence.question_string_nps_relevant_np_entity_path[:-1] + '2/' + str(i) + file_suffix)
		# output_file = open(file_path_refrence.question_string_nps_relevant_np_entity_path + str(i) + file_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 
		input_file = open(file_path_refrence.question_string_nps_relevant_np_entity_path[:-1] + '2/' + str(file_index) + file_lemma_suffix)
		output_file = open(file_path_refrence.question_string_nps_relevant_np_entity_path + str(i) + file_lemma_suffix, 'w')
		for line in input_file:
			output_file.write(line) 

		input_file = open(file_path_refrence.question_string_nps_relevant_np_entity_path[:-1] + '2/' + str(file_index) + file_lemma_suffix)
		output_file = open(file_path_refrence.question_string_nps_relevant_np_entity_path + str(i) + file_lemma_suffix, 'w')
		for line in input_file:
			output_file.write(line) 

		# input_file = open(file_path_refrence.question_string_nps_relevant_np_entity_path[:-1] + '2/' + str(file_index) + file_suffix)
		# output_file = open(file_path_refrence.question_string_nps_relevant_np_entity_path + str(i) + file_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 

		try:
			input_file = open(file_path_refrence.relevant_np_entity_after_classifier[:-1] + '2/' + str(i) + file_suffix)
			output_file = open(file_path_refrence.relevant_np_entity_after_classifier + str(i) + file_suffix, 'w')
			for line in input_file:
				output_file.write(line) 
		except:
			pass
			
		try:
			input_file = open(file_path_refrence.relevant_np_entity_after_classifier[:-1] + '2/' + str(file_index) + file_lemma_suffix)
			output_file = open(file_path_refrence.relevant_np_entity_after_classifier + str(i) + file_lemma_suffix, 'w')
			for line in input_file:
				output_file.write(line) 
		except:
			pass

		# input_file = open(file_path_refrence.relevant_np_type_after_classifier[:-1] + '2/' + str(i) + file_suffix)
		# output_file = open(file_path_refrence.relevant_np_type_after_classifier + str(i) + file_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 
		try:
			input_file = open(file_path_refrence.relevant_np_type_after_classifier[:-1] + '2/' + str(file_index) + file_lemma_suffix)
			output_file = open(file_path_refrence.relevant_np_type_after_classifier + str(i) + file_lemma_suffix, 'w')
			for line in input_file:
				output_file.write(line) 
		except:
			pass

		# input_file = open(file_path_refrence.question_string_np_before_article_ommiting[:-1] + '2/' + str(file_index) + file_suffix)
		# output_file = open(file_path_refrence.question_string_np_before_article_ommiting + str(i) + file_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 
		# input_file = open(file_path_refrence.question_string_np_before_article_ommiting[:-1] + '2/' + str(file_index) + file_lemma_suffix)
		# output_file = open(file_path_refrence.question_string_np_before_article_ommiting + str(i) + file_lemma_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 

		# input_file = open(file_path_refrence.gold_subset_pair_paths[:-1] + '2/' + str(i) + file_suffix)
		# output_file = open(file_path_refrence.gold_subset_pair_paths + str(i) + file_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 
		try:
			input_file = open(file_path_refrence.gold_subset_pair_paths[:-1] + '2/' + str(file_index) + file_lemma_suffix)
			output_file = open(file_path_refrence.gold_subset_pair_paths + str(i) + file_lemma_suffix, 'w')
			for line in input_file:
				output_file.write(line) 
		except:
			pass

		# input_file = open(file_path_refrence.gold_disjoint_pair_path[:-1] + '2/' + str(i) + file_suffix)
		# output_file = open(file_path_refrence.gold_disjoint_pair_path + str(i) + file_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 
		try:
			input_file = open(file_path_refrence.gold_disjoint_pair_path[:-1] + '2/' + str(file_index) + file_lemma_suffix)
			output_file = open(file_path_refrence.gold_disjoint_pair_path + str(i) + file_lemma_suffix, 'w')
			for line in input_file:
				output_file.write(line) 
		except:
			pass

		# input_file = open(file_path_refrence.gold_equivalence_pair_path[:-1] + '2/' + str(i) + file_suffix)
		# output_file = open(file_path_refrence.gold_equivalence_pair_path + str(i) + file_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 
		try:
			input_file = open(file_path_refrence.gold_equivalence_pair_path[:-1] + '2/' + str(file_index) + file_lemma_suffix)
			output_file = open(file_path_refrence.gold_equivalence_pair_path + str(i) + file_lemma_suffix, 'w')
			for line in input_file:
				output_file.write(line) 
		except:
			pass

		# input_file = open(file_path_refrence.pos_tagging_file_path[:-1] + '2/' + str(i) + file_suffix)
		# output_file = open(file_path_refrence.pos_tagging_file_path + str(i) + file_suffix, 'w')
		# for line in input_file:
		# 	output_file.write(line) 
		input_file = open(file_path_refrence.pos_tagging_file_path[:-1] + '2/' + str(file_index) + file_lemma_suffix)
		output_file = open(file_path_refrence.pos_tagging_file_path + str(i) + file_lemma_suffix, 'w')
		for line in input_file:
			output_file.write(line) 

		input_file = open('data/stan2/' + str(file_index) + file_lemma_suffix)
		output_file = open('data/stan/' + str(i) + file_lemma_suffix, 'w')
		for line in input_file:
			output_file.write(line)

		input_file = open('data/stan2/' + str(file_index) + file_lemma_suffix_story)
		output_file = open('data/stan/' + str(i) + file_lemma_suffix_story, 'w')
		for line in input_file:
			output_file.write(line)

		input_file = open('data/stan_dep2/' + str(file_index) + file_suffix)
		output_file = open('data/stan_dep/' + str(i) + file_suffix, 'w')
		for line in input_file:
			output_file.write(line)


		input_file = open('data/stan2/' + str(file_index) + file_suffix)
		output_file = open('data/stan/' + str(i) + file_suffix, 'w')
		for line in input_file:
			output_file.write(line) 



shuffle_files(0, 400)