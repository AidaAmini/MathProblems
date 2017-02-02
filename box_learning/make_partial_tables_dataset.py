from random import randint
from file_refrence import file_refrence
import copy
from math_modifiers import math_modifiers

def read_noun_phrases(file_path):
	res = []
	input_file = open(file_path, 'r')
	for np in input_file:
		if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
			np = np[:-3]
		else:
			np = np[:-1]
		# print np.split(' ')
		if np not in res and len(np.split(' '))<6:
			res.append(np)
	return res

def check_subEq(box1, box2):
	# print 'box1'
	# print box1
	for i in range(len(box1)):
		for j in range(len(box1[0])):
			if not (box1[i][j].startswith('-') or box1[i][j] == box2[i][j]):
				# print 'truuuuuuuuuueeeeee'
				return True

	return False


useful_indexes = [4,6,7,9]
change_group_one = [4,6,7,9]
change_group_two = [5,8,10]
file_path_refrence = file_refrence()
output_checking_file = open('out_check.txt','w')

for i in range(0, 514):
	row_index = []
	column_index = []
	unseen_nps = []
	seen_nps = []
	np_list = read_noun_phrases(file_path_refrence.question_string_nps_relevant_np_entity_path + str(i) + '_lemma.txt')
	true_table = []
	partial_true_tables = []
	partial_false_tables = []
	false_tables = []
	try:
		print i
		input_file=open(file_path_refrence.new_annotation_path + 'simpl/' + str(i) + '_lemma.txt', 'r')
		count = 0
		line_count = -1
		for line in input_file:
			line_count = line_count + 1
			line_parts = line[:-2].split(',')
			merges_needed = len(line_parts) - 11
			while merges_needed > 0:
				for k in range(len(line_parts)-1):
					if (line_parts[k].startswith("\"") or line_parts[k].startswith("\'\'")) and (line_parts[k+1].endswith("\"") or line_parts[k+1].endswith("\'\'")):
						line_parts[k] = line_parts[k][1:] + ',' + line_parts[k+1][:-1]
						line_parts.remove(line_parts[k+1])
				merges_needed = merges_needed - 1

			box_row = []
			for j in range(0, len(useful_indexes)):
				if not line_parts[useful_indexes[j]].startswith('-'):
					count = count + 1
					row_index.append(line_count)
					column_index.append(line_parts[useful_indexes[j]])
					seen_nps.append(line_parts[useful_indexes[j]])
				box_row.append(line_parts[useful_indexes[j]])
			if len(box_row) != 0:
				true_table.append(box_row)
		# print 'here'
		
		num_list = []
		word_list = []

		for np in np_list:
			if len(np.split(' ')) == 1 and '-' not in np:
				if math_modifiers.is_word_number(np) == True:
					num_list.append(np)
				else:
					if np not in word_list:
						word_list.append(np)
			elif '-' in np:
				parts = np.split(' ')
				if math_modifiers.is_word_number(parts[0]):
					num_list.append(parts[0])
					rest_noun = ''
					for jj in range(1, len(parts)):
						rest_noun =rest_noun + ' ' + parts[jj]
					rest_noun = rest_noun[1:]
					if rest_noun not in word_list:
						word_list.append(rest_noun)
				else:
					if np not in word_list:
						word_list.append(np)
			elif len(np.split(' ')) > 1:
				parts = np.split(' ')
				if math_modifiers.is_word_number(parts[0]):
					num_list.append(parts[0])
					rest_noun = ''
					for jj in range(1, len(parts)):
						rest_noun =rest_noun + ' ' + parts[jj]
					rest_noun = rest_noun[1:]
					if rest_noun not in word_list:
						word_list.append(rest_noun)
				else:
					if np not in word_list:
						word_list.append(np)
		for np in np_list:
			if np not in seen_nps and np in word_list:
				unseen_nps.append(np)

		output_checking_file.write(str(i)+ '\n')
		output_checking_file.write(str(true_table)+ '\n')
		output_checking_file.write(str(np_list) + '\n')
		output_checking_file.write(str(num_list) + '\n')
		output_checking_file.write(str(word_list) + '\n\n\n')

		iter_left_count = count
		last_step_generated_true_tables = []
		last_step_generated_true_tables.append(true_table)
		
		while iter_left_count>=0:

			# print 'inwhile'
			for ii in range(len(last_step_generated_true_tables)):
				new_generated_true_tables = []
				# print 'for each table'
				# print ii
				# print len(last_step_generated_true_tables)
				true_table_under_test = last_step_generated_true_tables[ii]
				for j in range(len(true_table_under_test)):
					for k in range(len(true_table_under_test[0])):
						if not true_table_under_test[j][k].startswith('-'):
							new_table = copy.deepcopy(true_table_under_test)
							new_table[j][k] = '-'
							new_generated_true_tables.append(new_table)
				# print 'new_generated_true_tables'
				# print new_generated_true_tables
				# print len(new_generated_true_tables)
				if iter_left_count != 0:
					for o in range(len(new_generated_true_tables)):
						if new_generated_true_tables[o] not in partial_true_tables:
							partial_true_tables.append(new_generated_true_tables[o])
				
				table_needed = 5
				change_needed = iter_left_count / 2
				table_count = 0
				count_of_iters = 0
				while table_count != table_needed and count_of_iters < 100:
					count_of_iters =  count_of_iters + 1
					new_table = copy.deepcopy(true_table_under_test)
					change_count = 0
					seen_changes_list = []

					src_change_row = randint(0, len(true_table) - 1)
					src_change_column = randint(0, len(useful_indexes) -1)
					dst_change_row = randint(0, len(true_table) - 1)
					dst_change_column = randint(0, len(useful_indexes) -1)
					change_iter_count = 0
					while change_count != change_needed and change_iter_count != 100:
						change_iter_count = change_iter_count + 1
						if (src_change_row == dst_change_row) and (src_change_column == dst_change_column):
							src_change_row = randint(0, len(true_table) - 1)
							src_change_column = randint(0, len(useful_indexes) -1)
							dst_change_row = randint(0, len(true_table) - 1)
							dst_change_column = randint(0, len(useful_indexes) -1)
							continue
						if (src_change_row, src_change_column, dst_change_row, dst_change_column) not in seen_changes_list:
							seen_changes_list.append((src_change_row, src_change_column, dst_change_row, dst_change_column))
							seen_changes_list.append((dst_change_row, dst_change_column, src_change_row, src_change_column))
							temp = new_table[src_change_row][src_change_column]
							change_flag = True
							for k in range(0, len(new_table[dst_change_row])):
								if new_table[dst_change_row][k] == temp:
									change_flag = False
									break
							if change_flag == True:
								new_table[dst_change_row][dst_change_column] = new_table[src_change_row][src_change_column]
								new_table[src_change_row][src_change_column] = temp
								change_count = change_count + 1
							src_change_row = randint(0, len(true_table) - 1)
							src_change_column = randint(0, len(useful_indexes) -1)
							dst_change_row = randint(0, len(true_table) - 1)
							dst_change_column = randint(0, len(useful_indexes) -1)
					
						else:
							src_change_row = randint(0, len(true_table) - 1)
							src_change_column = randint(0, len(useful_indexes) -1)
							dst_change_row = randint(0, len(true_table) - 1)
							dst_change_column = randint(0, len(useful_indexes) -1)
					adding_flag = True
					for t in false_tables:
						if new_table == t:
							adding_flag = False
							break
					if adding_flag == True and check_subEq(new_table, true_table) ==  True:
						false_tables.append(new_table)
						table_count = table_count + 1

				table_needed = 1
				change_needed = iter_left_count / 4
				table_count = 0
				count_of_iters = 0
				while table_count != table_needed and count_of_iters < 100:
					count_of_iters =  count_of_iters + 1
					new_table = copy.deepcopy(true_table_under_test)
					change_count = 0
					seen_changes_list = []

					src_change_row = randint(0, len(true_table) - 1)
					src_change_column = randint(0, len(useful_indexes) -1)
					wrod_selection_index = randint(0, len(unseen_nps)-1)
					change_iter_count = 0
					while change_count != change_needed and change_iter_count != 100:
						change_iter_count = change_iter_count + 1
						if (src_change_row, src_change_column, wrod_selection_index) not in seen_changes_list:
							seen_changes_list.append((src_change_row, src_change_column, wrod_selection_index))
							new_table[src_change_row][src_change_column] = unseen_nps[wrod_selection_index]
							change_count = change_count + 1
							src_change_row = randint(0, len(true_table) - 1)
							src_change_column = randint(0, len(useful_indexes) -1)
							wrod_selection_index = randint(0, len(unseen_nps)-1)
					
						else:
							src_change_row = randint(0, len(true_table) - 1)
							src_change_column = randint(0, len(useful_indexes) -1)
							wrod_selection_index = randint(0, len(unseen_nps)-1)

					adding_flag = True
					for t in false_tables:
						if new_table == t:
							adding_flag = False
							break
					if adding_flag == True and check_subEq(new_table, true_table) == True:
						false_tables.append(new_table)
						table_count = table_count + 1
			last_step_generated_true_tables = new_generated_true_tables
			iter_left_count = iter_left_count - 1
		# for i in range(0, 24):
		# 	word_list.append('-')
		# for i in range(18):
		# 	num_list.append('-')
		# index_complete_list = []
		# for k in range(24):
		# 	index_complete_list.append(k)
		# import itertools
		# # for k in range(len(word_list)):
		# permutations = list(itertools.permutations(word_list, 2))
		# for permute in permutations:
		# 	permute = list(permute)
		# 	list_of_chosen_indexes = list(itertools.permutations(index_complete_list, 2))
		# 	for chosen_indexes in list_of_chosen_indexes:
		# 		index1_row = chosen_indexes[0] / 4
		# 		index1_col = chosen_indexes[0] % 4
		# 		index2_row = chosen_indexes[1] / 4
		# 		index2_col = chosen_indexes[1] % 4
		# 		table_false = [['-' for x in range(4)] for x in range(6)]
		# 		table_false[index1_row][index1_col] = permute[0]
		# 		table_false[index2_row][index2_col] = permute[1]
		# 		false_tables.append(table_false)

		output_file = open(file_path_refrence.new_annotation_path + 'tables_partials_all/' + str(i) + '.txt', 'w')
		output_file.write("1\n")
		output_file.write(str(true_table)+ '\n')
		for j in range(0, len(partial_true_tables)):
			output_file.write("1\n")
			output_file.write(str(partial_true_tables[j])+ '\n')
		for j in range(0, len(false_tables)):
			output_file.write("-1\n")
			output_file.write(str(false_tables[j])+ '\n')



	except:
		print 'except'
		pass













