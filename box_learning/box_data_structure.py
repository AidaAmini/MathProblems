from math_modifiers import math_modifiers
from nltk.corpus import wordnet as wn
from wordnet_helper import wordnet_helper
import math

class box_data_structure(object):
	"""docstring for box_data_structure"""

	noun_phrase_list = []
	related_words_with_conjunction = []
	noun_phrase_with_counts = []
	noun_phrase_with_counts_with_count = []
	word_vector = [[]]
	word_list = []
	repeated_noun_phrases = []
	noun_phrases_in_question = []
	whole_question = ''
	question_strings = []
	wn_helper = wordnet_helper()
	equivalence_relation_word_list = ['per', 'cost', 'equals', 'be', 'costs', 'equal', 'is', 'was', 'were', 'are', 'spend', 'spent', 'spends', 'sell', 'buy', 'per']
	equivalance_relation_per_like_rule_word_list = ['per', 'a']
	true_exmples = []
	same_head_noun_phrases = []
	same_head_noun_phrases_ms = []
	same_head_noun_phrases_heads = []
	false_examples = []
	num_of_features_for_cells = 7
	num_of_features_for_rows = 13
	num_of_features_for_columns = 13
	number_cells = [1,4,6]

	def __init(self):
		self.noun_phrase_list = []
		self.repeated_noun_phrases = []
		self.noun_phrases_in_question = []
		self.related_words_with_conjunction = []
		self.noun_phrase_with_counts = []
		self.noun_phrase_with_counts_with_count = []
		self.whole_question = ''
		self.question_strings = []
		self.true_exmples = []
		self.false_examples = []
		self.same_head_noun_phrases = []
		self.same_head_noun_phrases_heads = []
		self.same_head_noun_phrases_ms = []

	def destruct(self):
		self.noun_phrase_list = []
		self.repeated_noun_phrases = []
		self.noun_phrases_in_question = []
		self.related_words_with_conjunction = []
		self.noun_phrase_with_counts = []
		self.noun_phrase_with_counts_with_count = []
		self.whole_question = ''
		self.question_strings = []
		self.true_exmples = []
		self.false_examples = []
		self.same_head_noun_phrases = []
		self.same_head_noun_phrases_ms = []
		self.same_head_noun_phrases_heads = []


	def read_noun_phrases(self, file_path):
		input_file = open(file_path, 'r')
		for np in input_file:
			if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
				np = np[:-3]
			else:
				np = np[:-1]
			if np not in self.noun_phrase_list:
				self.noun_phrase_list.append(np)

	def read_tables(self, file_path):
		input_file = open(file_path, 'r')
		line = input_file.readline()
		while line != '':
			true_flag = True
			if line.startswith('-1'):
				true_flag = False
			line  = input_file.readline()
			line = line[1:-2]
			line.replace('\"', '')
			parts = line.split('], [')
			parts[0] = parts[0][1:]
			parts[len(parts) - 1] = parts[len(parts) - 1][:-1]
			table = []
			for row_input in parts:
				row = []
				row_parts = row_input.split(',')
				for item in row_parts:
					item = item.lstrip()
					item = item.replace('\'', '')
					row.append(item)
				table.append(row)

			if true_flag == True:
				self.true_exmples.append(table)
			else:
				self.false_examples.append(table)
			line = input_file.readline()

	def find_if_any_equivalence_word_in_between(self, np1, np2):
		np1_index = self.whole_question.find(np1)
		np2_index = self.whole_question.find(np2)
		while np1_index >= 0 and np2_index >= 0 and abs(np2_index - np1_index) <= 20:
			if np1_index > np2_index:
				part_words = self.whole_question[np2_index: np1_index].split(' ')
				for word in part_words:
					if word in self.equivalence_relation_word_list:
						return 1
				np2_index = self.whole_question.find(np2, np2_index + 1)
			else:
				part_words = self.whole_question[np1_index: np2_index].split(' ')
				for word in part_words:
					if word in self.equivalence_relation_word_list:
						return 1
				np1_index = self.whole_question.find(np1, np1_index + 1)
		return 0

	def find_per_equivalence_rule_value(self, np1, np2):
		np1_index = self.whole_question.find(np1)
		np2_index = self.whole_question.find(np2)
		while np1_index >= 0 and np2_index >= 0:
			if np1_index > np2_index:
				part_words = self.whole_question[np2_index: np1_index].split(' ')
				for word in self.equivalance_relation_per_like_rule_word_list:
					if np2 + ' ' + word + ' ' + np1 in self.whole_question:
						return 1
				np2_index = self.whole_question.find(np2, np2_index + 1)
			else:
				part_words = self.whole_question[np1_index: np2_index]
				for word in self.equivalance_relation_per_like_rule_word_list:
					if np1 + ' ' + word + ' ' + np2 in self.whole_question:
						return 1
				np1_index = self.whole_question.find(np1, np1_index + 1)
		return 0

	def find_repeated_noun_phrases(self):
		for noun_phrase in self.noun_phrase_list:
			found_index = self.whole_question.find(noun_phrase) + 1
			if self.whole_question.find(noun_phrase, found_index) > -1:
				if noun_phrase not in self.repeated_noun_phrases:
					self.repeated_noun_phrases.append(noun_phrase)


	def find_noun_phrases_in_question(self, pos_file_name):
		pos_file = open(pos_file_name, 'r')
		pos_list = []
		word_list = []
		for line in pos_file:
			parts = line[:-1].split('/')
			pos_list.append(parts[1].lower())
			word_list.append(parts[0].lower())
		index = -1
		if 'wrb' in pos_list:
			index = pos_list.index('wrb')
		while index > -1:
			word_index = index + 1
			new_word = ''
			while word_index < len(pos_list) and pos_list[word_index] != 'nns':
				if pos_list[word_index].startswith('nn'):
					new_word = new_word + word_list[word_index] + ' '
				word_index = word_index + 1
			if word_index != len(pos_list):
				new_word = new_word + word_list[word_index]
			if new_word.endswith(' '):
				new_word = new_word[:-1]
			self.noun_phrases_in_question.append(new_word)
			if 'wrb' in pos_list[index+1:]:
				index = pos_list.index('wrb', index+1)
			else:
				index = -1

		if len(self.noun_phrases_in_question) > 0:
			return 	
		for i in range (0, len(self.question_strings)):
			sentence = self.question_strings[i].lower()
			if '?' in sentence or (i == len(self.question_strings) -1):
				for noun_phrase in self.noun_phrase_list:
					if sentence.find(noun_phrase) > -1:
						if noun_phrase not in self.noun_phrases_in_question:
							self.noun_phrases_in_question.append(noun_phrase.lower())

	def calc_box_edit_distance(self, box1, box2):
		dist = 0
		# print box1
		# print box2
		seen_rows_in_box2 = []
		seen_rows_in_box1 = []
		for i in range(len(box2)):
			seen_rows_in_box2.append(False)
			seen_rows_in_box1.append(False)
		for i in range(len(box2)):
			seen_rows_in_box2[i] = True
			max_count = 0
			index_matched = -1
			for j in range(len(box1)):
				count = 0
				if seen_rows_in_box1[j]== True:
					continue
				for k in range(len(box2[j])):
					# print 'checking'
					# print box1[j][k]
					# print box2[i][k]
					if box1[j][k] == box2[i][k] or box2[i][k].startswith('-'):
						# print 'cunt increase'
						count = count + 1
				# print 'after count '
				# print count
				# print seen_rows_in_box1
				if count > max_count and seen_rows_in_box1[j] == False:
					max_count = count
					index_matched = j
			if index_matched >= 0:
				seen_rows_in_box1[index_matched] = True
			# print 'index_matched'
			# print str(index_matched) + '     ' + str(i)
			for k in range(len(box2[i])):
				if box2[i][k].startswith('-') and not box1[index_matched][k].startswith('-'):
					dist = dist + 1
				elif not box2[i][k].startswith('-') and box1[index_matched][k].startswith('-'):
					return -1
				elif not box2[i][k].startswith('-') and not box1[index_matched][k].startswith('-') and box2[i][k] != box1[index_matched][k]:
					return -1

		for i in range(len(seen_rows_in_box1)):
			if seen_rows_in_box1 == False:
				for k in range(len(box1[0])):
					dist = dist + 1
			if seen_rows_in_box2 == False:
				for k in range(len(box1[0])):
					dist = dist + 1
		max_heigth = len(box1)
		if len(box2) > max_heigth:
			max_heigth = len(box2)

		# print 'return 1'
		return 1#(dist + 0.0)/(max_heigth * len(box[0]))

	def find_count_noun_stanford(self, file_name):
		input_file = open(file_name, 'r')
		words = []
		pos_tags = []
		#parsing input file 
		for line in input_file:
			line2 = line[:-1].lower().replace(' ', '').replace('?', '').replace('!', '')
			parts = line2.split('/')
			if parts[0].endswith('.'):
				parts[0] = parts[0][:-1]
			words.append(parts[0])
			pos_tags.append(parts[1])
			if '. ' in line or '? 'in line or '! ' in line:
				words.append('.')
				pos_tags.append('endOfSent')

		for i in range(0, len(pos_tags)):
			if pos_tags[i] == 'cd':
				rest_noun = ''
				i = i+1
				while pos_tags[i].startswith('nn') or pos_tags[i].startswith('jj') or pos_tags[i] == 'pos' or pos_tags[i] == 'cd' or pos_tags[i] == 'cc' or words[i] in math_modifiers.modifier_element_list:
					if words[i] not in math_modifiers.modifier_element_list:
						rest_noun = words[i] + " "
					i = i+ 1
				rest_noun = rest_noun[:-1]
				if rest_noun != '' and rest_noun not in self.noun_phrase_with_counts:
					self.noun_phrase_with_counts.append(rest_noun)


	def find_parsing_mode(self, file_name, index):
		parse_file = open(file_name, 'r')
		parse_text = parse_file.readline()
		next_open_parantese_index = parse_text.find('(', index + 1)
		if parse_text[next_open_parantese_index + 1: next_open_parantese_index + 4] =='NNS':
			return 0
		elif parse_text[next_open_parantese_index + 1: next_open_parantese_index + 4] =='NN ':
			return 1
		elif parse_text[next_open_parantese_index + 1: next_open_parantese_index + 4] =='JJS': # for sit like 4 more then ...
			return 2
		elif parse_text[next_open_parantese_index + 1: next_open_parantese_index + 4] =='TO ':
			return 3
		else:
			return -1

	def find_unit_type(self, np1):
		if len(np1.split(' ')) > 1:
			parts = np1.split(' ')
			return math_modifiers.check_for_unit(parts[len(parts)-1])
		return math_modifiers.check_for_unit(np1)

	def find_related_words_with_conjunction(self, file_name):
		parse_file = open(file_name, 'r')
		parse_text = parse_file.readline()
		index = parse_text.find('[u\'conj_')
		while index > -1:
			part_text = parse_text[index:parse_text.find(']', index+1)].lower()
			part_text_before = parse_text[parse_text.find('u\'',index - 30):parse_text.find('],', index - 20)]
			parts = part_text.split(', u\'')
			parts_before = part_text_before.split(', u\'')
			for i in range(1, len(parts)):
				parts[i] = parts[i][:-1].lower()
			main_part_before = parts_before[len(parts_before)-1][:-1].lower()
			main_part = parts[len(parts)-1]
			for np in self.noun_phrase_list:
				if np.startswith(main_part_before) or np.endswith(main_part_before) or np == main_part_before:
					self.related_words_with_conjunction.append(main_part)

			for i in range(1, len(parts)):
				for np in self.noun_phrase_list:
					if np.startswith(parts[i]) or np.endswith(parts[i]):
						for j in range(1, len(parts)):
							if j == i:
								continue 
							if parts[j] not in np:
								self.related_words_with_conjunction.append(np[:np.find(parts[i])] + parts[j] + np[np.find(parts[i]) + len(parts[i]):])
								others_important = self.find_related_np_to_conjucated_np(parts[i], parts[j])
								for noun_phrase in others_important:
									self.related_words_with_conjunction.append(noun_phrase)

			index = parse_text.find('[u\'conj_', index+1)

	def find_same_head_np(self):
		for np1 in self.noun_phrase_list:
			for np2 in self.noun_phrase_list:
				if (np1 in np2) or (np2 in np1):
					continue
				if ' ' in np1 and ' ' in np2:
					head_np1, modifier_np1 = self.parse_np(np1)
					head_np2, modifier_np2 = self.parse_np(np2)
					if head_np2 == head_np1 and head_np1 != '':
						if modifier_np1 in self.same_head_noun_phrases and modifier_np2 in self.same_head_noun_phrases:
							continue
						self.same_head_noun_phrases_ms.append(modifier_np1)
						self.same_head_noun_phrases_ms.append(modifier_np2)
						self.same_head_noun_phrases_heads.append(head_np1)
						self.same_head_noun_phrases_heads.append(head_np2)
						self.same_head_noun_phrases.append(np1)
						self.same_head_noun_phrases.append(np2)

	def find_related_np_to_conjucated_np(self, np1, np2):
		res_list = []
		for i in range(0, len(self.noun_phrase_list)):
			if self.noun_phrase_list[i].startswith(np1):
				ending_part = self.noun_phrase_list[i][len(np1) + 1:]
				for j in range(0, len(self.noun_phrase_list)):
					if j==i:
						continue
					if self.noun_phrase_list[j].startswith(np2) and self.noun_phrase_list[j].endswith(ending_part):
						if self.noun_phrase_list[j] not in res_list:
							res_list.append(self.noun_phrase_list[j])
							break
			elif self.noun_phrase_list[i].startswith(np2):
				ending_part = self.noun_phrase_list[i][len(np2) + 1:]
				for j in range(0, len(self.noun_phrase_list)):
					if j==i:
						continue
					if self.noun_phrase_list[j].startswith(np1) and self.noun_phrase_list[j].endswith(ending_part):
						if self.noun_phrase_list[j] not in res_list:
							res_list.append(self.noun_phrase_list[j])
						break
			elif self.noun_phrase_list[i].endswith(np1):
				starting_part = self.noun_phrase_list[i][:-1*len(np1) -1]
				for j in range(0, len(self.noun_phrase_list)):
					if j==i:
						continue
					if self.noun_phrase_list[j].endswith(np2) and self.noun_phrase_list[j].startswith(starting_part):
						if self.noun_phrase_list[j] not in res_list:
							res_list.append(self.noun_phrase_list[j])
						break
			elif self.noun_phrase_list[i].endswith(np2):
				starting_part = self.noun_phrase_list[i][:-1*len(np2) -1]
				for j in range(0, len(self.noun_phrase_list)):
					if j==i:
						continue
					if self.noun_phrase_list[j].endswith(np1) and self.noun_phrase_list[j].startswith(starting_part):
						if self.noun_phrase_list[j] not in res_list:
							res_list.append(self.noun_phrase_list[j])
						break
		return res_list

	def have_same_head(self, np1, np2):
		parts_np1 = np1.split(' ')
		parts_np2 = np2.split(' ')
		if (len(parts_np1) < 2) or (len(parts_np2) < 2):
			return 0
		if (np1 in self.same_head_noun_phrases) and (np2 in self.same_head_noun_phrases) and (((self.same_head_noun_phrases.index(np1) - self.same_head_noun_phrases.index(np2)) == 1) or((self.same_head_noun_phrases.index(np2) - self.same_head_noun_phrases.index(np1)) == 1)):
			return 1
		return 0

	def find_the_cosinge(self, np1, np2, num_of_dimentions):
		if (np2 not in self.word_list) or (np1 not in self.word_list):
			return 0
		index_np1 = self.word_list.index(np1)
		index_np2 = self.word_list.index(np2)
		sum1 = 0
		sum2 = 0
		sum3 = 0
		for i in range(0, num_of_dimentions):
			sum1 = sum1 + self.word_vector[index_np1][i] * self.word_vector[index_np2][i]
			sum2 = sum2 + self.word_vector[index_np1][i] * self.word_vector[index_np1][i]
			sum3 = sum3 + self.word_vector[index_np2][i] * self.word_vector[index_np2][i]
		return (sum1 + 0.0) / (math.sqrt(sum2) * math.sqrt(sum3))

	def find_word_list(self, file_name, num_of_dimentions):
		embedding_file = open(file_name, 'r')
		for line in embedding_file:
			parts = line.split(' ')
			self.word_list.append(parts[0])
		self.word_vector = [[0.0]*num_of_dimentions for x in range(len(self.word_list))]
		embedding_file = open(file_name, 'r')
		index = 0
		for line in embedding_file:
			parts = line.split(' ')
			for i in range(1, num_of_dimentions + 1):
				self.word_vector[index][i-1] = float(parts[i])
			index = index + 1

	def find_nps_min_distance(self, np1, np2): # Should I do this for the heads as well
		np1_index = self.whole_question.find(np1)
		np2_index = self.whole_question.find(np2)
		min_distance = 999999
		while np1_index >= 0 and np2_index >= 0:
			if np1_index > np2_index:
				if np1_index - np2_index < min_distance:
					min_distance = np1_index - np2_index
				np2_index = self.whole_question.find(np2, np2_index + 1)
			else:
				if np2_index - np1_index < min_distance:
					min_distance = np2_index - np1_index
				np1_index = self.whole_question.find(np1, np1_index + 1)
		if min_distance > 7:
			min_distance = 7
		return (min_distance +0.0) / 7


	def read_whole_question(self, file_name): #checked
		input_file = open(file_name, 'r')
		self.whole_question = input_file.readline().lower()

	def read_question_strings(self, file_name): #checked
		input_file = open(file_name, 'r')
		for line in input_file:
				self.question_strings.append(line.lower())

	def parse_np(self, noun_phrase):
		parts = noun_phrase.split(' ')
		rest_parts = ''
		head = parts[len(parts) - 1]
		for i in range(0, len(parts)-1):
			rest_parts = rest_parts + parts[i] + ' '
		return (head, rest_parts[:-1])


	def table_cell_features(self, feature_list, feature_name_list, num_of_row, num_of_columns, table_under_test):
		for i in range(num_of_row):
			if i >= len(table_under_test):
				for j in range(num_of_columns):
					for k in range(self.num_of_features_for_cells):
						feature_list.append(0)

			else:
				for j in range(num_of_columns):
					if j >= len(table_under_test[0]):
						for k in range(self.num_of_features_for_cells):
							feature_list.append(0)
					else:
						if table_under_test[i][j] == '-':
							for k in range(self.num_of_features_for_cells):
								feature_list.append(0)
						else:
							feature_list, feature_name_list = self.find_feature_for_cell(feature_list,feature_name_list, i, j, table_under_test[i][j])

		return (feature_list, feature_name_list)


	def find_feature_for_cell(self, feature_list, feature_name_list, x, y, word_in_cell):
		if word_in_cell in self.repeated_noun_phrases:
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("cell feature: if np in cell is repeated")
		if word_in_cell in self.noun_phrase_with_counts:
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("cell feature: if np in cell has count")
		if math_modifiers.check_for_unit(word_in_cell) != '000':
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("cell feature: if np in cell is unit")
		if '%' in word_in_cell:
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("cell feature: if percent is in np")
		if '-' in word_in_cell:
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("cell feature: if np in cell has - in it")
		if y in self.number_cells:
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("cell feature: if the cell is a number cell")
		if word_in_cell in self.noun_phrases_in_question:
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("cell feature: if np in cell is a np questioned about")
		return (feature_list, feature_name_list)

	def table_row_feautres(self, feature_list, feature_name_list, num_of_row, num_of_columns, table_under_test):
		for i in range(num_of_row):
			# print len(feature_list)
			if i >= len(table_under_test):
				for j in range(num_of_columns):
					for jj in range(j+ 1, num_of_columns):
						for k in range(self.num_of_features_for_rows):
							feature_list.append(0)
			else:
				for j in range(num_of_columns):
					for jj in range(j+1, num_of_columns):
						if j >=len(table_under_test[0]) or jj>= len(table_under_test[0]):
							for k in range(self.num_of_features_for_rows):
								feature_list.append(0)
						else:
							if table_under_test[i][j].startswith('-') or table_under_test[i][jj].startswith('-'):
								for k in range(self.num_of_features_for_rows):
									feature_list.append(0)
							else:
								feature_list, feature_name_list = self.find_feature_for_row(feature_list,feature_name_list, i, j,jj, table_under_test[i][j], table_under_test[i][jj])
		return (feature_list, feature_name_list)

	def table_column_feautres(self, feature_list, feature_name_list, num_of_row, num_of_columns, table_under_test):
		for i in range(num_of_columns):
			# print len(feature_list)
			if i >= len(table_under_test[0]) :
				for j in range(num_of_row):
					for jj in range(j+ 1, num_of_row):
						for k in range(self.num_of_features_for_columns):
							feature_list.append(0)
			else:
				for j in range(num_of_row):
					for jj in range(j+1, num_of_row):
						if j >=len(table_under_test) or jj >= len(table_under_test):
							for k in range(self.num_of_features_for_columns):
								feature_list.append(0)
						else:
							if table_under_test[j][i].startswith('-') or table_under_test[jj][i].startswith('-'):
								for k in range(self.num_of_features_for_columns):
									feature_list.append(0)
							else:
								feature_list, feature_name_list = self.find_feature_for_column(feature_list,feature_name_list, i, j,jj, table_under_test[j][i], table_under_test[jj][i])
		return (feature_list, feature_name_list)


	def calc_wordsim_feature(self, feature_list, feature_name_list, np1, np2):
		max_similarity = 0
		ave_similarity = 0
		count = 0
		parts_np1 = np1.split(' ')
		parts_np2 = np2.split(' ')
		if len(parts_np1) >1 and len(parts_np2) > 1:
			sim = self.wn_helper.word_similarity(parts_np1[0], parts_np2[0])
			count = count + 1
			ave_similarity = ave_similarity + sim
			if sim> max_similarity:
				max_similarity = sim
		elif len(parts_np1) > 1:
			sim = self.wn_helper.word_similarity(parts_np1[len(parts_np1)-1], np2)
			count = count + 1
			ave_similarity = ave_similarity + sim
			if sim> max_similarity:
				max_similarity = sim
		elif len(parts_np2) > 1:
			sim = self.wn_helper.word_similarity(np1, parts_np2[len(parts_np2) - 1])
			count = count + 1
			ave_similarity = ave_similarity + sim
			if sim> max_similarity:
				max_similarity = sim
		feature_name_list.append('max word_net similarity between 2 chains')
		feature_list.append(max_similarity)
		feature_name_list.append('ave word_net similarity between 2 chains')
		feature_list.append((ave_similarity + 0.0) / (count + 0.00001))
		return (feature_list, feature_name_list)

	def find_feature_for_row(self, feature_list, feature_name_list, x, y, yy, np1, np2):
		np1_parts = np1.split(' ')
		if np1 == np2:
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("row feature: if the nps are the same")
		if np2.startswith(np1_parts[0]) or np2.endswith(np1_parts[len(np1_parts) - 1]):
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("row feature: if np has the same begging or head")
		if math_modifiers.check_for_unit(np1) != '000' and math_modifiers.check_for_unit(np2) != '000':
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("row feature: if both nps are units")
		if math_modifiers.check_for_unit(np1) != '000' or math_modifiers.check_for_unit(np2) != '000':
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("row feature: if one of the nps is unit")
		if math_modifiers.check_for_unit(np1) != math_modifiers.check_for_unit(np2) and math_modifiers.check_for_unit(np2) != '000':
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("row feature: if both nps are same units")
		self.calc_wordsim_feature(feature_list, feature_name_list, np1, np2)
		cosigne = self.find_the_cosinge(np1, np2, 300)
		feature_list.append(cosigne)
		feature_name_list.append("row feature: cosigne of nps")
		if y in self.number_cells and yy in self.number_cells:
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("row feature: both index are number cells.")
		if y in self.number_cells or yy in self.number_cells:
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("row feature: one index are number cells.")
		if (y in self.number_cells and yy  not in self.number_cells) or (yy in self.number_cells and y not in self.number_cells):
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("row feature: exactly one index are number cells.")
		if self.have_same_head(np1, np2) == 1:
			feature_list.append(1)
			feature_list.append(self.find_the_cosinge(self.same_head_noun_phrases_ms[self.same_head_noun_phrases.index(np1)], self.same_head_noun_phrases_ms[self.same_head_noun_phrases.index(np2)], 300))
		else:
			feature_list.append(-1)
			feature_list.append(0)
		feature_name_list.append("row feature: the nps have same head")
		feature_name_list.append("row feature: the cosigne between the adj")
		return (feature_list, feature_name_list)


	def find_feature_for_column(self, feature_list, feature_name_list, y, x, xx, np1, np2):
		np1_parts = np1.split(' ')
		if np1 == np2:
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("column feature: if the nps are the same")
		if np2.startswith(np1_parts[0]) or np2.endswith(np1_parts[len(np1_parts) - 1]):
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("column feature: if np has the same begging or head")
		if math_modifiers.check_for_unit(np1) != '000' and math_modifiers.check_for_unit(np2) != '000':
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("column feature: if both nps are units")
		if math_modifiers.check_for_unit(np1) != '000' or math_modifiers.check_for_unit(np2) != '000':
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("column feature: if one of the nps is unit")
		if math_modifiers.check_for_unit(np1) != math_modifiers.check_for_unit(np2) and math_modifiers.check_for_unit(np2) != '000':
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("column feature: if both nps are same units")
		self.calc_wordsim_feature(feature_list, feature_name_list, np1, np2)
		cosigne = self.find_the_cosinge(np1, np2, 300)
		feature_list.append(cosigne)
		feature_name_list.append("column feature: cosigne of nps")
		if y in self.number_cells:
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append("column feature: both index are number cells.")
		if ('x1' in np1 or 'x2' in np1) or ('x1' in np2 or 'x2' in np2):
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append('column feature: one of elements is variable')
		if ('x1' in np1 or 'x2' in np1) and ('x1' in np2 or 'x2' in np2):
			feature_list.append(1)
		else:
			feature_list.append(-1)
		feature_name_list.append('column feature: both elements are variable')
		if self.have_same_head(np1, np2) == 1:
			feature_list.append(1)
			feature_list.append(self.find_the_cosinge(self.same_head_noun_phrases_ms[self.same_head_noun_phrases.index(np1)], self.same_head_noun_phrases_ms[self.same_head_noun_phrases.index(np2)], 300))
		else:
			feature_list.append(-1)
			feature_list.append(0)
		feature_name_list.append("row feature: the nps have same head")
		feature_name_list.append("row feature: the cosigne between the adj")
		return (feature_list, feature_name_list)














































		