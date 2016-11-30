import sys
from file_refrence import file_refrence
from math_modifiers import math_modifiers

							
def find_unit_type(np1):
		return math_modifiers.check_for_unit(np1)

def find_the_pair_words_for_relevant_pair(start_index, end_index, entity_type_mode):
	file_path_refrence = file_refrence()
	output_file = open(file_path_refrence.pair_visualize_data_file, 'w')
	for i in range(start_index, end_index):
		question_strings_np = []
		if i in file_path_refrence.problematic_indexes:
			continue
		
		if entity_type_mode == 1:
			input_file = open(file_path_refrence.relevant_np_entity_after_classifier + str(i) + '.txt','r')
		elif entity_type_mode == 0:
			input_file = open(file_path_refrence.np_pos_path + str(i) + '_lemma.txt','r')
		
		for np in input_file:
			if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
				question_strings_np.append(np[:-3].lower())
			else:
				question_strings_np.append(np[:-1].lower())
		for np1 in question_strings_np:
			for np2 in question_strings_np:
				if np1 == np2:
					continue
				output_file.write(np1 + '\t' + np2 + '\n')

#####################################################

def find_the_relevant_noun_phrases(start_index, end_index, entity_type_mode):
	file_path_refrence = file_refrence()
	if entity_type_mode == 1:
		output_file = open(file_path_refrence.np_visualization_file_entity, 'w')
	else:
		output_file = open(file_path_refrence.np_visualization_file_type, 'w')

	for i in range(start_index, end_index):
		question_strings_np = []
		if i in file_path_refrence.problematic_indexes:
			continue

		if entity_type_mode == 1:
			input_file = open(file_path_refrence.question_string_nps_relevant_np_entity_path + str(i) + '_lemma.txt','r')
		elif entity_type_mode == 0:
			input_file = open(file_path_refrence.question_string_nps_relevant_np_type_path + str(i) + '_lemma.txt','r')
		
		for np in input_file:
			if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
				question_strings_np.append(np[:-3].lower())
			else:
				question_strings_np.append(np[:-1].lower())
		for np1 in question_strings_np:	
			output_file.write(np1 + '\t' + str(i) + '\n')

#####################################################
		
def calcPrecisionRecallForRelevantNP(score_file_name, test_file_name, noun_phrase_list_file, visualize_data_file_name):
	seen_list = []
	res_file = open(score_file_name, 'r')
	test_file = open(test_file_name, 'r')
	noun_phrases_list = open(noun_phrase_list_file, 'r')
	tp_array = []
	tn_array = []
	fp_array = []
	fn_array = []
	tp = 0
	tn = 0
	fp = 0
	fn = 0
	last_seen_problem = -1
	seen_word_problem_tp = []
	seen_word_problem_fp = []
	for line in res_file:
		if 'labels' in line or len(line) < 4:
			continue
		np_line = noun_phrases_list.readline()
		# if 'problem: ' in np_line:
		# 	np_line = noun_phrases_list.readline()
		parts = np_line.split('	')
		
		if len(parts) == 1:
			continue
		if (len (parts[0].split(' ')) == 1) :
			if find_unit_type(parts[0]) != '000':
				tp = tp + 1
				np_line = noun_phrases_list.readline()	
		if last_seen_problem != parts[1]:
			last_seen_problem = parts[1]
			for part_fp in seen_word_problem_fp:
				for part_tp in seen_word_problem_tp:
					if part_fp in part_tp:
						fp = fp - 1
						break

			seen_word_problem_tp = []
			seen_word_problem_fp = []

		np_line = np_line[:-1]
		test_line = test_file.readline()
		line_float = float(line[:-1])
		if line_float > 0.0:
			if test_line.startswith("1"):
				seen_word_problem_tp.append(parts[0])
				if np_line in tp_array:
					continue
				tp = tp + 1
				tp_array.append(np_line)
			else:
				seen_word_problem_fp.append(parts[0])
				if np_line in fp_array:
					continue
				fp = fp + 1
				fp_array.append(np_line)
		else: 
			if test_line.startswith("1"):
				if np_line in fn_array:
					continue
				fn = fn + 1
				fn_array.append(np_line)
			else:
				if np_line in tn_array:
					continue
				tn = tn + 1
				tn_array.append(np_line)

	# print np_line
	output_file = open(visualize_data_file_name, 'w')
	output_file.write("tp_array\n")
	for word in tp_array:
		output_file.write(word + '\n')
	output_file.write("tn_array\n")
	for word in tn_array:
		output_file.write(word + '\n')
	output_file.write("fp_array\n")
	for word in fp_array:
		output_file.write(word + '\n')
	output_file.write("fn_array\n")
	for word in fn_array:
		output_file.write(word + '\n')
	print tp
	print fn
	print tn
	print fp
	print 'accuracy::' + str((tn + tp + 0.0) / (tn + tp + fp + fn + 0.0))
	print 'precision:'+str((tp + 0.0) / (tp + fp + 0.0))
	print 'recall: '+str((tp + 0.0) / (tp + fn +0.0))




def calcPrecisionRecallForRelevantPair(score_file_name, test_file_name, noun_phrase_list_file, visualize_data_file_name):
	seen_list = []
	res_file = open(score_file_name, 'r')
	test_file = open(test_file_name, 'r')
	noun_phrases_list = open(noun_phrase_list_file, 'r')
	tp_array = []
	tn_array = []
	fp_array = []
	fn_array = []
	tp = 0
	tn = 0
	fp = 0
	fn = 0
	for line in res_file:
		if line.startswith('labels') or len(line) < 4:
			continue
		np_line = noun_phrases_list.readline()
		if 'problem: ' in np_line:
			np_line = noun_phrases_list.readline()
		np_line = np_line[:-1]
		test_line = test_file.readline()
		if line.startswith('1'):
			if test_line.startswith("1"):
				tp = tp + 1
				tp_array.append(np_line)
			else:
				fp = fp + 1
				fp_array.append(np_line)
		else: 
			if test_line.startswith("1"):
				fn = fn + 1
				fn_array.append(np_line)
			else:
				tn = tn + 1
				tn_array.append(np_line)

	output_file = open(visualize_data_file_name, 'w')
	output_file.write("tp_array\n")
	for word in tp_array:
		output_file.write(word + '\n')
	output_file.write("tn_array\n")
	for word in tn_array:
		output_file.write(word + '\n')
	output_file.write("fp_array\n")
	for word in fp_array:
		output_file.write(word + '\n')
	output_file.write("fn_array\n")
	for word in fn_array:
		output_file.write(word + '\n')
	print tp
	print fn
	print tn
	print fp
	print 'accuracy::' + str((tn + tp + 0.0) / (tn + tp + fp + fn + 0.0))
	print 'precision:'+str((tp + 0.0) / (tp + fp + 0.0))
	print 'recall: '+str((tp + 0.0) / (tp + fn +0.0))


def calcPrecisionRecallForJointLearner(score_file_name, test_file_name, visualize_data_file_name):
	file_path_refrence = file_refrence()
	res_file = open(score_file_name, 'r')
	test_file = open(test_file_name, 'r')
	noun_phrases_list = open(file_path_refrence.pair_visualize_data_file, 'r')

	tp_array_disjoint = []
	fp_array_disjoint = []
	fn_array_disjoint = []
	tp_array_subset = []
	tn_array = []
	fp_array_subset = []
	fn_array_subset = []
	tp_array_eq = []
	fp_array_eq = []
	fn_array_eq = []
	tp_disjoint = 0
	tn_total = 0
	fp_disjoint = 0
	fn_disjoint = 0
	tp_subset = 0
	fp_subset = 0
	fn_subset = 0
	tp_eq = 0
	fp_eq = 0
	fn_eq = 0
	for line in res_file:
		if line.startswith('labels'):
			continue
		while 1==1:
			np_line = noun_phrases_list.readline()
			# while 'problem: ' in np_line:
			# 	np_line = noun_phrases_list.readline()
			np_line = np_line[:-1]
			# parts = np_line.split('\t')
			np1 = ''
			np2 = ''

			# if np1.endswith(np2):
			# 	if math_modifiers.is_word_number(np1[:np1.index(np2)-1]):
			# 		tp_array_subset.append(np_line)
			# 		tp_subset = tp_subset + 1
			# 	else:
			# 		break
			# elif np2.endswith(np1):
			# 	if math_modifiers.is_word_number(np2[:np2.index(np1)-1]):
			# 		tp_array_subset.append(np_line)
			# 		tp_subset = tp_subset + 1
			# 	else:
			# 		break
			# else:
			# 	break
		
		test_line = test_file.readline()
		# print test_line
		# print line
		# if not test_line.startswith('0'):
		# 	if not line.startswith('0'):
				# print line[:-1]
				# print test_line[:-1]
				# print ''
		if line.startswith("1"):
			if test_line.startswith("1"):
				tp_subset = tp_subset + 1
				tp_array_subset.append(np_line)
			else:
				fp_subset = fp_subset + 1
				fp_array_subset.append(np_line)
				if test_line.startswith('3'):
					fn_array_eq.append(np_line)
					fn_eq = fn_eq + 1
				elif test_line.startswith('2'):
					fn_array_disjoint.append(np_line)
					fn_disjoint = fn_disjoint + 1

		elif line.startswith("2"):
			if test_line.startswith("2"):
				tp_array_disjoint.append(np_line)
				tp_disjoint = tp_disjoint +1
			else:
				fp_array_disjoint.append(np_line)
				fp_disjoint = fp_disjoint + 1
				if test_line.startswith('3'):
					fn_array_eq.append(np_line)
					fn_eq = fn_eq + 1
				elif test_line.startswith('1'):
					fn_array_subset.append(np_line)
					fn_subset = fn_subset + 1

		elif line.startswith("3"):
			if test_line.startswith("3"):
				tp_array_eq.append(np_line)
				tp_eq = tp_eq +1
			else:
				fp_array_eq.append(np_line)
				fp_eq = fp_eq + 1
				if test_line.startswith('2'):
					fn_array_disjoint.append(np_line)
					fn_disjoint = fn_disjoint + 1
				elif test_line.startswith('1'):
					fn_array_subset.append(np_line)
					fn_subset = fn_subset + 1
		else: 
			if test_line.startswith("1"):
				fn_subset = fn_subset + 1
				fn_array_subset.append(np_line)
			elif test_line.startswith('2'):
				fn_array_disjoint.append(np_line)
				fn_disjoint = fn_disjoint + 1
			elif test_line.startswith('3'):
				fn_array_eq.append(np_line)
				fn_eq = fn_eq + 1
			else:
				tn_total = tn_total + 1
				tn_array.append(np_line)
		

	output_file = open(visualize_data_file_name, 'w')
	output_file.write("tp_array_disjoint\n")
	for word in tp_array_disjoint:
		output_file.write(word + '\n')

	output_file.write("fp_array_disjoint\n")
	for word in fp_array_disjoint:
		output_file.write(word + '\n')
	output_file.write("fn_array_disjoint\n")
	for word in fn_array_disjoint:
		output_file.write(word + '\n')

	output_file.write("tp_array_subset\n")
	for word in tp_array_subset:
		output_file.write(word + '\n')

	output_file.write("fp_array_subset\n")
	for word in fp_array_subset:
		output_file.write(word + '\n')
	output_file.write("fn_array_subset\n")
	for word in fn_array_subset:
		output_file.write(word + '\n')

	output_file.write("tn_array\n")
	for word in tn_array:
		output_file.write(word + '\n')
	print 'for disjoint'
	tp = tp_disjoint
	tn = tn_total + tp_subset + fn_subset + tp_eq + fn_eq
	fp = fp_disjoint
	fn = fn_disjoint
	print 'accuracy::' + str((tn + tp + 0.0) / (tn + tp + fp + fn + 0.0))
	print 'precision:'+str((tp + 0.0) / (tp + fp + 0.0))
	print 'recall: '+str((tp + 0.0) / (tp + fn +0.0))

	print 'for subset'
	tp = tp_subset
	tn = tn_total + tp_disjoint + fn_disjoint + tp_eq + fn_eq
	fp = fp_subset
	fn = fn_disjoint + fp_disjoint
	print 'accuracy::' + str((tn + tp + 0.0) / (tn + tp + fp + fn + 0.0))
	print 'precision:'+str((tp + 0.0) / (tp + fp + 0.0))
	print 'recall: '+str((tp + 0.0) / (tp + fn +0.0))

	print 'for equivalence'
	tp = tp_eq
	tn = tn_total + tp_disjoint + fn_disjoint + tp_subset + fn_subset
	fp = fp_eq
	fn = fn_eq
	print 'accuracy::' + str((tn + tp + 0.0) / (tn + tp + fp + fn + 0.0))
	print 'precision:'+str((tp + 0.0) / (tp + fp + 0.0))
	print 'recall: '+str((tp + 0.0) / (tp + fn +0.0))

	print 'for disjoint/subset'
	tp = tp_disjoint + tp_subset + tp_eq
	tn = tn_total
	fp = fp_disjoint + fp_subset + fp_eq
	fn = fn_disjoint + fn_subset + fn_eq
	print 'accuracy::' + str((tn + tp + 0.0) / (tn + tp + fp + fn + 0.0))
	print 'precision:'+str((tp + 0.0) / (tp + fp + 0.0))
	print 'recall: '+str((tp + 0.0) / (tp + fn +0.0))



file_path_refrence = file_refrence()
seen_list = []
score_file_name = str(sys.argv[1])
test_file_name = str(sys.argv[2])
mode = int(sys.argv[3]) #0 : np_relevant -- 1: pair relevant --2: noRel, eq-- 3:joint
entity_type_mode = int(sys.argv[4]) # 1 for entity and 0 for type
start_index = int(sys.argv[5])
end_index = int(sys.argv[6])

if mode == 0:
	# find_the_relevant_noun_phrases(start_index, end_index, entity_type_mode)
	if entity_type_mode == 1:
		calcPrecisionRecallForRelevantNP(score_file_name, test_file_name, file_path_refrence.np_visualization_file_entity, 'visualize_data_np_entity.txt')
	elif entity_type_mode == 0:
		calcPrecisionRecallForRelevantNP(score_file_name, test_file_name, file_path_refrence.np_visualization_file_type, 'visualize_data_np_type.txt')

elif mode == 1:
	# find_the_pair_words_for_relevant_pair(start_index, end_index, entity_type_mode)
	calcPrecisionRecallForRelevantPair(score_file_name, test_file_name, file_path_refrence.all_pairs_path, 'visualize_data_pair.txt')
elif mode == 2:
	find_the_pair_words_for_relevant_pair(start_index, end_index, entity_type_mode)
	calcPrecisionRecallForRelevantPair(score_file_name, test_file_name, file_path_refrence.all_pairs_path, 'visualize_data_releq.txt')
elif mode == 3:
	# find_the_pair_words_for_relevant_pair(start_index, end_index, entity_type_mode)
	calcPrecisionRecallForJointLearner(score_file_name, test_file_name, "visualize_data_joint.txt")

