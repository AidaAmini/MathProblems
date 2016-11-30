from math_modifiers import math_modifiers



class percenptron_data:
	noun_phrase_list = []
	unchained_np_list = []
	gold_chain_list = []
	gold_disjoint_list = []
	gold_subset_list = []
	driven_chains = []
	related_words_with_conjunction = []
	count_type_noun_phrase = []
	noun_phrase_with_counts = []
	noun_phrase_with_counts_with_count = []
	word_vector = [[]]
	word_list = []
	whole_question = ''
	equivalence_relation_word_list = ['per', 'cost', 'equals', 'be', 'costs', 'equal', 'is', 'was', 'were', 'are', 'spend', 'spent', 'spends', 'for', 'a']

	def __init(self):
		self.noun_phrase_list = []
		self.unchained_np_list = []
		self.gold_chain_list = []
		self.gold_subset_list =[]
		self.gold_disjoint_list = []
		self.driven_chains = []
		self.related_words_with_conjunction = []
		self.noun_phrase_with_counts = []
		self.noun_phrase_with_counts_with_count = []
		self.count_type_noun_phrase = []
		self.word_vector = [[]]
		self.word_list = []
		self.whole_question = ''

	def destruct(self):
		self.noun_phrase_list = []
		self.unchained_np_list = []
		self.gold_chain_list = []
		self.gold_subset_list =[]
		self.gold_disjoint_list = []
		self.driven_chains = []
		self.related_words_with_conjunction = []
		self.noun_phrase_with_counts = []
		self.noun_phrase_with_counts_with_count = []
		self.count_type_noun_phrase = []
		self.word_vector = [[]]
		self.word_list = []
		self.whole_question = ''


	def read_noun_phrases(self, file_paht):
		input_file = open(file_paht, 'r')
		for np in input_file:
			if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
				np = np[:-3]
			else:
				np = np[:-1]
			if np not in self.noun_phrase_list:
				self.noun_phrase_list.append(np)

	def read_disjoints(self, file_paht):
		input_file = open(file_paht, 'r')
		for line in input_file:
			line = line[:-1]
			if line == '':
				break
			if line[:-1] == ' ':
				line = line[:-1]
			parts = line.split('	')
			self.gold_disjoint_list.append(parts[0].lower())
			self.gold_disjoint_list.append(parts[1].lower())

	def read_subsets(self, file_paht):
		input_file = open(file_paht, 'r')
		for line in input_file:
			line = line[:-1]
			if line == '':
				break
			if line[:-1] == ' ':
				line = line[:-1]
			parts = line.split('	')
			self.gold_subset_list.append(parts[0].lower())
			self.gold_subset_list.append(parts[1].lower())

	def find_gold_chains(self):
		for i in range(0, len(self.gold_disjoint_list), 2):
			np1 = self.gold_disjoint_list[i]
			np2 = self.gold_disjoint_list[i+1]
			need_new_chain = True
			for chain in self.gold_chain_list:
				if np1 in chain:
					if np2 not in chain:
						chain.append(np2)
					need_new_chain = False
				if np2 in chain:
					if np1 not in chain:
						chain.append(np1)
					need_new_chain = False
			if need_new_chain == True:
				new_chain = []
				new_chain.append(np1)
				new_chain.append(np2)
				self.gold_chain_list.append(new_chain)
		for i in range(0, len(self.gold_subset_list), 2):
			np1 = self.gold_subset_list[i]
			np2 = self.gold_subset_list[i+1]
			need_new_chain = True
			for chain in self.gold_chain_list:
				if np1 in chain:
					if np2 not in chain:
						chain.append(np2)
					need_new_chain = False
				if np2 in chain:
					if np1 not in chain:
						chain.append(np1)
					need_new_chain = False
			if need_new_chain == True:
				new_chain = []
				new_chain.append(np1)
				new_chain.append(np2)
				self.gold_chain_list.append(new_chain)

	def find_unchained_nps(self):
		for np in self.noun_phrase_list:
			is_in_chains = False
			for chain in self.gold_chain_list:
				if np in chain:
					is_in_chains = True
					break
			if is_in_chains == False:
				self.unchained_np_list.append(np)


	def find_count_noun_stanford(self, file_name):
		noun_phrase_with_counts = []
		res_parsing_mode = []
		input_file = open(file_name, 'r')
		parse_text = input_file.readline()
		index = parse_text.find('(CD');
		while index >=0 :
			parse_result = self.find_parsing_mode(file_name, index)
			parantese_index = parse_text.find('(', index + 1)
			if parse_result == 0:
				if parse_text[parantese_index+5: parse_text.find(')', parantese_index+1)] not in self.noun_phrase_with_counts:
					self.noun_phrase_with_counts.append(parse_text[parse_text.find(' ',parantese_index+5): parse_text.find(')', parantese_index+1)].lower())
					self.count_type_noun_phrase.append(parse_result)
					self.noun_phrase_with_counts_with_count.append(parse_text[parantese_index+5: parse_text.find(')', parantese_index+1)].lower())
			elif parse_result == 1:
				if parse_text[parantese_index+4: parse_text.find(')', parantese_index+1)] not in self.noun_phrase_with_counts:
					self.noun_phrase_with_counts.append((parse_text[parse_text.find(' ',index +4): parse_text.find(')', index)]+" "+parse_text[parantese_index+4: parse_text.find(')', parantese_index+1)]).lower())
					self.count_type_noun_phrase.append(parse_result)
					self.noun_phrase_with_counts_with_count.append((parse_text[index +4: parse_text.find(')', index)]+" "+parse_text[parantese_index+4: parse_text.find(')', parantese_index+1)]).lower())
			index = parse_text.find('(CD', index+1);
		for i in range(0, len(self.noun_phrase_with_counts)):
			if self.noun_phrase_with_counts[i].startswith(' '):
				self.noun_phrase_with_counts[i] = self.noun_phrase_with_counts[i][1:]

		return (noun_phrase_with_counts, res_parsing_mode)

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


	def find_nps_min_distance(self, np1, np2):
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
		return min_distance


	def read_whole_question(self, file_name): #checked
		input_file = open(file_name, 'r')
		self.whole_question = input_file.readline().lower()


	def find_if_any_equivalence_word_in_between(self, np1, np2):
		np1_index = self.whole_question.find(np1)
		np2_index = self.whole_question.find(np2)
		while np1_index >= 0 and np2_index >= 0 and abs(np2_index - np2_index) <= 10:
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

	def calc_merge_count_feature(self, chain1, chain2):
		chain1_has_counts = False
		for np1 in chain1:
			if np1 in self.noun_phrase_with_counts:
				chain1_has_counts = True
				break
		chain2_has_counts = False
		for np2 in chain2:
			if np2 in self.noun_phrase_with_counts:
				chain2_has_counts = True
				break
		if chain1_has_counts == True and chain2_has_counts == True:
			return 1
		else:
			return 0

	def calc_merge_unit_features(self, chain1, chain2):
		chain1_has_unit = False
		for np1 in chain1:
			if math_modifiers.check_for_unit(np1) != '000':
				chain1_has_unit = True
				break
		chain2_has_unit = False
		for np2 in chain2:
			if math_modifiers.check_for_unit(np2) != '000':
				chain2_has_unit = True
				break
		if chain1_has_unit == True and chain2_has_unit == True:
			return 1
		else:
			return 0

	def calc_merge_max_cosigne(self, chain1, chain2):
		max_cosigne = 0.0
		for np1 in chain1: 
			for np2 in chain2:
				cosigne = self.find_the_cosinge(np1, np2, 300)
				if cosigne > max_cosigne:
					max_cosigne = cosigne
		return max_cosigne

	def calc_merge_ave_dist(self, chain1, chain2):
		dist_sum = 0
		count = 0
		seen_pairs = []
		for np1 in chain1:
			for np2 in chain2:
				if np1+np2 not in seen_pairs:
					seen_pairs.append(np1+np2)
					seen_pairs.append(np2+np1)
					dist_sum = dist_sum + self.find_nps_min_distance(np1, np2)
					count = count + 1

		return (dist_sum + 0.0) / count





























