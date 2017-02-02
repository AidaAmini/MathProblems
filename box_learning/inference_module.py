from scikit_test import scikit_module
from file_refrence import file_refrence
from box_data_structure import box_data_structure
from math_modifiers import math_modifiers
import copy

class inference_module:
	file_path_refrence = file_refrence()
	box_structure = box_data_structure()
	word_list = []
	np_list = []
	num_list = []
	num_of_row = 6
	num_of_column = 4
	true_table = []
	head_list = []
	counted_more_than_once = []
	scikit_train_module = scikit_module(30, 10, 10)
	beam_size = 20

	def __init__(self, scikit_module):
		self.word_list = []
		self.np_list = []
		self.num_list = []
		self.true_table = []
		self.scikit_train_module = scikit_module
		self.head_list = []
		self.counted_more_than_once = []

	def flush_data(self):
		self.word_list = []
		self.np_list = []
		self.num_list = []
		self.true_table = []
		self.head_list = []
		self.counted_more_than_once = []

	def find_same_head_np(self):
		self.head_list = []
		for np1 in self.np_list:
			for np2 in self.np_list:
				if (np1 in np2) or (np2 in np1):
					continue
				if ' ' in np1 and ' ' in np2:
					np1_parts = np1.split(' ')
					np1_head = np1_parts[len(np1_parts) - 1]
					np2_parts = np2.split(' ')
					np2_head = np2_parts[len(np2_parts) - 1]
					if np1_head == np2_head:
						self.head_list.append(np1_head)
					if np1_parts[0] == np2_parts[0]:
						self.head_list.append(np1_parts[0])
				elif ' ' in np1 and ' ' not in np2:
					np1_parts = np1.split(' ')
					np1_head = np1_parts[len(np1_parts) - 1]
					if np1_head == np2:
						self.head_list.append(np1_head)
					if np1_parts[0] == np2:
						self.head_list.append(np2)
				elif ' ' not in np1 and ' ' in np2:
					np2_parts = np2.split(' ')
					np2_head = np2_parts[len(np2_parts) - 1]
					if np2_head == np1:
						self.head_list.append(np2_head)
					if np2_parts[0] == np1:
						self.head_list.append(np1)

	def read_true_table(self, problem_index):
		self.true_table = []
		useful_indexes = [4,6,7,9]
		input_file=open(self.file_path_refrence.new_annotation_path + 'simpl/' + str(problem_index) + '_lemma.txt', 'r')
		for line in input_file:
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
				box_row.append(line_parts[useful_indexes[j]])
			if len(box_row) != 0:
				self.true_table.append(box_row)


	def table_equality_check(self, table1, table2):
		dist = 0
		seen_rows_in_table2 = []
		seen_rows_in_table1 = []
		for i in range(len(table2)):
			seen_rows_in_table2.append(False)
			seen_rows_in_table1.append(False)
		for i in range(len(table2)):
			seen_rows_in_table2[i] = True
			equal_row_found = False
			for j in range(len(table1)):
				if seen_rows_in_table1[j] == True:
					continue 
				row_EQ = True
				for k in range(len(table2[0])):
					if table1[j][k] != table2[i][k]:
						row_EQ = False
						break
				if row_EQ == True:
					seen_rows_in_table1[j] = True
					equal_row_found = True
					break
			if equal_row_found == False:
				return False
		return True
			

	def modify_check(self, new_table, new_table_list, new_word_added):
		for table in new_table_list:
			if self.table_equality_check(table, new_table) == True:
				return False
			if new_word_added in self.head_list or math_modifiers.check_for_unit(new_word_added) != '000':
				return True
			count = 0
			for i in range(len(new_table)):
				for j in range(len(new_table[i])):
					if new_table[i][j] == new_word_added:
						count = count + 1
			if count > 1:
				return False
		return True

	def inference_procedure_per_problem(self, problem_index):
		print 'problem' + str(problem_index)
		self.initialize_num_word_lists(problem_index)
		first_sample = []
		for i in range(self.num_of_row):
			new_row = []
			for ii in range(self.num_of_column):
				new_row.append('-')
			first_sample.append(new_row)
		list_of_considerations = []
		list_of_considerations.append((first_sample, 1))
		stop_flag = False
		output_tarin = open('inf/test_inf' + str(problem_index) +'.txt', 'w')
		while stop_flag != True:
			print 'in while'
			new_table_list = []
			for element in list_of_considerations:
				cur_table = list(element)[0]
				for j in range(self.num_of_row):
					for k in range(self.num_of_column):
						if cur_table[j][k].startswith('-'):
							for i in range(len(self.word_list)):
								new_table = copy.deepcopy(cur_table)
								new_table[j][k] = self.word_list[i]
								if self.modify_check(new_table, new_table_list, self.word_list[i]) == True:
									new_table_list.append(new_table)
			y_test = []
			x_test = []
			table_test_list = []
			print len(new_table_list)
			for table in new_table_list:
				table_test_list.append(table)
				y_label = self.box_structure.calc_box_edit_distance(self.true_table, table)
				# output_tarin.write(str(y_label) + ' ')
				y_test.append(y_label)
				# output_tarin.write(str(self.box_structure.calc_box_edit_distance) + ' ')
				feature_list, feature_name_list = self.box_structure.table_cell_features([], [], 6, 4, table)
				feature_list, feature_name_list = self.box_structure.table_row_feautres(feature_list, feature_name_list, 6, 4, table)
				feature_list, feature_name_list = self.box_structure.table_column_feautres(feature_list, feature_name_list, 6, 4, table)
				x_test.append(feature_list)
				# for k in range(len(feature_list) - 1):
				# 	output_tarin.write(str(k) + ':' + str(feature_list[k]) + ' ')
				# output_tarin.write(str(len(feature_list)-1) + ':' + str(feature_list[len(feature_list)-1]) + '\n')
			y_classified, y_probs = self.scikit_train_module.random_forest_predict_by_prob(x_test)
			sorted_list = []
			for i in range(len(table_test_list)):
				if y_probs[i][1] > 0.6:
					sorted_list.append( (table_test_list[i], y_probs[i][1]))
			if len(sorted_list) < 5:
				stop_flag = True
			if stop_flag == True:
				break
			sorted_list.sort(key=lambda tup: tup[1])
			new_list_of_considerations = []
			for i in range(self.beam_size):
				new_list_of_considerations.append(sorted_list[i])
			stop_flag = self.check_for_stop_conditions(new_list_of_considerations)
			if stop_flag == True:
				break
			list_of_considerations = new_list_of_considerations
			#TODO: implement the function and save th last successful state	

		for res in list_of_considerations:
			prob = list(res)[1]
			table = list(res)[0]
			output_tarin.write(str(prob) + '\n')
			for i in range(len(table)):
				output_tarin.write(str(table[i]) + '\n')

		self.flush_data()
			
	def check_for_stop_conditions(self, table_list):
		for item in table_list:
			# print table
			table = list(item)[0]
			count_of_num_needed = 0 
			for i in range(self.num_of_row):
				if not table[i][0].startswith('-') or not table[i][1].startswith('-'):
					count_of_num_needed = count_of_num_needed + 1
				if not table[i][2].startswith('-'):
					count_of_num_needed = count_of_num_needed + 1
				if not table[i][3].startswith('-'):
					count_of_num_needed = count_of_num_needed + 1
			if count_of_num_needed == len(self.num_list):
				return True
		return False

	def read_noun_phrases(self, file_path):
		input_file = open(file_path, 'r')
		for np in input_file:
			if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
				np = np[:-3]
			else:
				np = np[:-1]
			# print np.split(' ')
			if np not in self.np_list and len(np.split(' '))<6:
				self.np_list.append(np)


	def initialize_num_word_lists(self, problem_index):
		self.read_noun_phrases(self.file_path_refrence.question_string_nps_relevant_np_entity_path + str(problem_index) + '_lemma.txt')
		self.read_true_table(problem_index)
		self.find_same_head_np()
		self.num_list.append('x1')
		self.num_list.append('x2')
		for np in self.np_list:
			if len(np.split(' ')) == 1 and '-' not in np:
				if math_modifiers.is_word_number(np) == True:
					self.num_list.append(np)
				else:
					if np not in self.word_list:
						self.word_list.append(np)
			elif '-' in np:
				parts = np.split(' ')
				if math_modifiers.is_word_number(parts[0]):
					self.num_list.append(parts[0])
					rest_noun = ''
					for jj in range(1, len(parts)):
						rest_noun =rest_noun + ' ' + parts[jj]
					rest_noun = rest_noun[1:]
					if rest_noun not in self.word_list:
						self.word_list.append(rest_noun)
				else:
					if np not in self.word_list:
						self.word_list.append(np)
			elif len(np.split(' ')) > 1:
				parts = np.split(' ')
				if math_modifiers.is_word_number(parts[0]):
					self.num_list.append(parts[0])
					rest_noun = ''
					for jj in range(1, len(parts)):
						rest_noun =rest_noun + ' ' + parts[jj]
					rest_noun = rest_noun[1:]
					if rest_noun not in self.word_list:
						self.word_list.append(rest_noun)
				else:
					if np not in self.word_list:
						self.word_list.append(np)





# inf_test = inference_module(scikit_module(30, 10, 10))
# inf_test.initialize_num_word_lists(353)
# print inf_test.num_list
# print inf_test.np_list
# print inf_test.word_list



































