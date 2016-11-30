from math_modifiers import math_modifiers
from numeric_features import numeric_features
from POSTags import POSTags
from file_refrence import file_refrence
import math

class entity_properties:
	numeric_feature_helper = numeric_features()
	file_path_refrence = file_refrence()
	word_vector = [[]]
	word_list = []
	antonym_list = []
	ccg_parse_string = ''
	whole_question = ''
	question_strings = []
	question_strings_np = []
	question_strings_np_before_article_ommiting = [] #this is defined for finding plural
	question_strings_np_before_article_ommiting_lemma = [] #this is defined for finding plural 
	noun_phrase_with_counts = []
	noun_phrase_with_counts_with_count = []
	named_entity_nouns = []
	noun_phrases_in_question = []
	noun_phrases_after_question_phrase = []
	repeated_noun_phrases = []
	related_words_with_conjunction = []
	noun_phrase_srl_arg = [[] for x in range(3)] # Since we want to define arg0 to arg2
	verb_srl_related_np_arg = [[] for x in range(3)]
	same_head_noun_phrases_heads = []
	same_head_noun_phrases_ms = []
	same_head_noun_phrases = []
	antonym_list_inQuestion = []
	count_type_noun_phrase = []
	relevant_noun_phrases = []
	disjoint_noun_phrases = []
	equivalence_noun_phrases = []
	subset_noun_phrases = []
	plural_used_nouns = []
	question_string_substrings = []
	srl_file_path = ''
	POS_tags = {} #This should be 2 dimensional map from one word to all the tags it gets.
	place_noun_phrases = []
	enitity_types = []
	relevant_pairs = []
	pronoun_list = []
	parse_tree_sentences = []
	parse_tree_levels = []
	equivalence_relation_word_list = ['per', 'cost', 'equals', 'be', 'costs', 'equal', 'is', 'was', 'were', 'are', 'spend', 'spent', 'spends', 'for', 'a']
	equivalance_relation_per_like_rule_word_list = ['per', 'a']

	
	def __init__(self):
		self.srl_file_path = self.file_path_refrence.srl_path

	def initialize_numeric_value(self):
		for type_name in self.enitity_types:
			self.numeric_feature_helper.find_all_numeric_values(type_name, self.whole_question)

	def read_pairs(self, file_name, problem_index):
		pair_file = open(file_name, 'r')
		line = pair_file.readline()
		while line != '':
			if line[:-1] == 'problem: ' + str(problem_index):
				line = pair_file.readline()
				while not 'problem: ' in line:
					self.relevant_pairs.append(line[:-1])
					line = pair_file.readline()
				break
			line = pair_file.readline()

	def read_equvalence(self, file_name):
		input_file = open(file_name, 'r')
		for line in input_file:
			line = line[:-1]
			if line == '':
				break
			parts = line.split('	')
			self.equivalence_noun_phrases.append(parts[0].lower())
			self.equivalence_noun_phrases.append(parts[1].lower())


	def find_subString_list(self):  # TODO add this functionality
		for noun_phrase in self.question_strings_np:
			for np1 in self.noun_phrases_in_question:
				if noun_phrase in np1 and noun_phrase != np1:
					self.question_string_substrings.append(noun_phrase)
			for np2 in self.repeated_noun_phrases:
				if noun_phrase in np2 and noun_phrase != np2:
					self.question_string_substrings.append(noun_phrase)
			for np3 in self.same_head_noun_phrases:
				if noun_phrase in np3 and noun_phrase != np3:
					self.question_string_substrings.append(noun_phrase)

	def find_list_antonyms(self, file_name):
		antonym_file = open(file_name, 'r')
		for line in antonym_file:
			parts = line.split(' ')
			for i in range(0, len(parts)):
				if parts[i].endswith('\n'):
					self.antonym_list.append(parts[i][:-1])
				else:
					self.antonym_list.append(parts[i])

	def read_whole_question(self, file_name):
		input_file = open(file_name, 'r')
		self.whole_question = input_file.readline().lower()

	def read_gold_noun_phrase(self, file_name):
		input_file = open(file_name, 'r')
		for line in input_file:
			line = line[:-1]
			if line == '':
				break
			self.relevant_noun_phrases.append(line.lower())
			
	def read_pos_taggings(self, file_name):
		input_file = open(file_name, 'r')
		for line in input_file:
			line = line[:-1].lower()
			if line == "":
				break
			
			parts = line.split("/")
			word = parts[0]
			if word.endswith('.') or word.endswith(',') or word.endswith('!') or word.endswith('?'): #TODO check format
				word = word[:-1]
			pos = parts[1]
			if word in  self.POS_tags:
				self.POS_tags[word] = self.POS_tags[word] + '	' + pos
			else:
				self.POS_tags[word] = pos
	
	def read_entity_types(self, file_name):
		input_file = open(file_name, 'r')
		for line in input_file:
			line = line[:-1]
			self.enitity_types.append(line)

	def find_place_modifier(self, pos_file_name):
		words= []
		pos = []
		input_file = open(pos_file_name, 'r')
		for line in input_file:
			line = line[:-1].lower()
			if line == "":
				break			
			parts = line.split("/")
			words.append(parts[0])
			pos.append(parts[1])

		for i in range(0, len(words)):
			if not (pos[i] == 'nn' or pos[i] == 'nnp'):
				continue
			index=i-1
			if index < 0:
				continue
			while pos[index] == 'dt':
				index = index -1
					
			if pos[index] == 'in':
				if words[index] == 'at' or words[index] == 'in':
					self.place_noun_phrases.append(words[i])

	def find_pronouns(self, pos_file_name):
		words= []
		pos = []
		input_file = open(pos_file_name, 'r')
		for line in input_file:
			line = line[:-1].lower()
			if line == "":
				break			
			parts = line.split("/")
			words.append(parts[0])
			pos.append(parts[1])
		for i in range(0, len(words)):
			if pos[i] == 'prp':
				self.pronoun_list.append(words[i])


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

	def find_if_both_are_in_a_same_sentence(self, np1, np2):
		for sentence in self.question_strings:
			if sentence.find(np1) >=0 and sentence.find(np2) >=0:
				return 1
		return 0

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

	def find_per_equivalence_rule_value(self, np1, np2):
		np1_index = self.whole_question.find(np1)
		np2_index = self.whole_question.find(np2)
		while np1_index >= 0 and np2_index >= 0:
			if np1_index > np2_index:
				part_words = self.whole_question[np2_index: np1_index].split(' ')
				for word in self.equivalance_relation_per_like_rule_word_list:
					if np2 + ' ' + word + ' ' + np1 in part_words:
						return 1
				np2_index = self.whole_question.find(np2, np2_index + 1)
			else:
				part_words = self.whole_question[np1_index: np2_index]
				for word in self.equivalance_relation_per_like_rule_word_list:
					if np1 + ' ' + word + ' ' + np2 in part_words:
						return 1
				np1_index = self.whole_question.find(np1, np1_index + 1)
		return 0

	def check_if_both_has_greatest_val(self, np1, np2):

		np1_number_part, np1_type_part = self.seperate_type_and_number(np1)
		np2_number_part, np2_type_part = self.seperate_type_and_number(np2)
		if np1_type_part == '' or np2_type_part == '' or np1_number_part == -1 or np2_number_part == -1:
			return 0

		np1_flag = self.numeric_feature_helper.check_if_largest_value_for_type(np1_number_part, np1_type_part)
		np2_flag = self.numeric_feature_helper.check_if_largest_value_for_type(np2_number_part, np2_type_part)
		if np1_flag == True and np2_flag == True:
			return 1
		return 0

	def check_if_both_has_lowest_val(self, np1, np2):

		np1_number_part, np1_type_part = self.seperate_type_and_number(np1)
		np2_number_part, np2_type_part = self.seperate_type_and_number(np2)
		if np1_type_part == '' or np2_type_part == '' or np1_number_part == -1 or np2_number_part == -1:
			return 0
		np1_flag = self.numeric_feature_helper.check_if_smallest_value_for_type(np1_number_part, np1_type_part)
		np2_flag = self.numeric_feature_helper.check_if_smallest_value_for_type(np2_number_part, np2_type_part)
		if np1_flag == True and np2_flag == True:
			return 1
		return 0

	def check_if_both_has_same_number_of_numbers(self, np1, np2):
		np1_number_part, np1_type_part = self.seperate_type_and_number(np1)
		np2_number_part, np2_type_part = self.seperate_type_and_number(np2)
		if np1_type_part == '' or np2_type_part == '' or np1_number_part == -1 or np2_number_part == -1:
			return 0
		if self.numeric_feature_helper.check_if_two_type_names_have_same_amount_of_counts(np1_type_part, np2_type_part) == True:
			return 1
		return 0
					
	def seperate_type_and_number(self, np): # it finds the largest type_name
		words_in_np = np.split(' ')
		res_type = ''
		res_number = -1
		for word in words_in_np:
			if math_modifiers.is_word_number(word) == True:
				try:
					res_number = float(word)
				except:
					pass
		for type_name in self.enitity_types:
			if type_name in np and len(type_name) > len(res_type):
				res_type = type_name
		return (res_number, res_type)

	def has_percent(self, np):
		if '%' in np and (np.index('%') < len(np) - 2):
			return '1'
		return '0'
	
	def read_question_strings(self, file_name):
		input_file = open(file_name, 'r')
		for line in input_file:
				self.question_strings.append(line.lower())

	def read_ccg_parse(self, file_name):
		self.ccg_parse_string = ''
		input_file = open(file_name, 'r')
		for line in input_file:
			self.ccg_parse_string = self.ccg_parse_string + line
		self.ccg_parse_string = self.ccg_parse_string.lower()

 	def read_question_np(self, file_name):
 		input_file = open(file_name, 'r')
 		for np in input_file:
			if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
				self.question_strings_np.append(np[:-3].lower())
			else:
				self.question_strings_np.append(np[:-1].lower())

	def read_question_strings_np_before_article_ommiting(self, file_name):
		input_file = open(file_name, 'r')
		for np in input_file:
			if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
				self.question_strings_np_before_article_ommiting.append(np[:-3].lower())
			else:
				self.question_strings_np_before_article_ommiting.append(np[:-1].lower())
			
	def read_question_strings_np_before_article_ommiting_lemma(self, file_name):
		input_file = open(file_name, 'r')
		for np in input_file:
			if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
				self.question_strings_np_before_article_ommiting_lemma.append(np[:-3].lower())
			else:
				self.question_strings_np_before_article_ommiting_lemma.append(np[:-1].lower())
				
	def read_subset_noun_phrases(self,  file_name):
		input_file = open(file_name,  'r')
		for line in input_file:
			line = line[:-1]
			if line=='':
				break
			parts = line.split('	')
			self.subset_noun_phrases.append(parts[0].lower())
			self.subset_noun_phrases.append(parts[1].lower())
			
	def find_the_joint_label(self, np1, np2):
		if self.check_if_disjoint(np1, np2) == 1:
			return 1
		elif self.check_if_subset(np1, np2) == 1:
			return 2
		elif self.check_if_equivalence(np1, np2) == 1:
			return 3
		else:
			return 0
	
	def check_if_subset(self, np1, np2):
		for i in range(0, len(self.subset_noun_phrases) - 1 ):
			if np1 == self.subset_noun_phrases[i] or (np1.endswith('es') and np1[:-2] == self.subset_noun_phrases[i])  or (np1.endswith('s') and  np1[:-1] == self.subset_noun_phrases[i]):
				if np2 == self.subset_noun_phrases[i + 1]  or (np2.endswith('es') and np2[:-2] == self.subset_noun_phrases[i + 1]) or (np2.endswith('s') and np2[:-1] == self.subset_noun_phrases[i + 1]) :
					return 1
			if np2 == self.subset_noun_phrases[i] or (np2.endswith('es') and np2[:-2] == self.subset_noun_phrases[i]) or (np2.endswith('s') and np2[:-1] == self.subset_noun_phrases[i]):
				if np1 == self.subset_noun_phrases[i + 1] or (np1.endswith('es') and np1[:-2] == self.subset_noun_phrases[i + 1]) or (np1 .endswith('s') and np1[:-1] == self.subset_noun_phrases[i + 1]):
					return 1
		return -1

	def check_if_equivalence(self, np1, np2):

		for i in range(0, len(self.equivalence_noun_phrases) - 1 ):
			if np1 == self.equivalence_noun_phrases[i] or (np1.endswith('es') and np1[:-2] == self.equivalence_noun_phrases[i])  or (np1.endswith('s') and  np1[:-1] == self.equivalence_noun_phrases[i]):
				if np2 == self.equivalence_noun_phrases[i + 1]  or (np2.endswith('es') and np2[:-2] == self.equivalence_noun_phrases[i + 1]) or (np2.endswith('s') and np2[:-1] == self.equivalence_noun_phrases[i + 1]) :
					return 1
			if np2 == self.equivalence_noun_phrases[i] or (np2.endswith('es') and np2[:-2] == self.equivalence_noun_phrases[i]) or (np2.endswith('s') and np2[:-1] == self.equivalence_noun_phrases[i]):
				if np1 == self.equivalence_noun_phrases[i + 1] or (np1.endswith('es') and np1[:-2] == self.equivalence_noun_phrases[i + 1]) or (np1 .endswith('s') and np1[:-1] == self.equivalence_noun_phrases[i + 1]):
					return 1
		return -1
		
	def find_pos_for_single_noun(self, np1) :
		parts = []
		if '	' not in self.POS_tags[np1]:
			parts.append(self.POS_tags[np1])
			res = POSTags.pos_tag_to_bin(parts[0])
			return res
		else :
			parts = self.POS_tags[np1].split('	')
			count_dict = {}
			for part in parts:
				if part in count_dict:
					count_dict[part] = count_dict[part] + 1
				else:
					count_dict[part] = 1
			max_pos = ''
			max_count = 0
			for pos in count_dict:
				if count_dict[pos] > max_count:
					max_count = count_dict[pos]
					max_pos = pos
			res = POSTags.pos_tag_to_bin(pos)
			return res
			
	def find_pos_label(self, np1):
		if np1 in self.POS_tags:
			# I want to find the maximum repetition 
			return self.find_pos_for_single_noun(np1)
		else:
			head_np1, modifier_np1 = self.parse_np(np1)
			if head_np1 not in self.POS_tags:
				return "11"
			return  self.find_pos_for_single_noun(head_np1)
			
			
	def find_unit_type(self, np1):
		if len(np1.split(' ')) > 1:
			head_np1, modifier_np1 = self.parse_np(np1)
			return math_modifiers.check_for_unit(head_np1)
		return math_modifiers.check_for_unit(np1)
		
	def read_disjoint_noun_phrase(self, file_name):
		input_file = open(file_name, 'r')
		for line in input_file:
			line = line[:-1]
			if line == '':
				break
			parts = line.split('	')
			self.disjoint_noun_phrases.append(parts[0].lower())
			self.disjoint_noun_phrases.append(parts[1].lower())

	def check_if_disjoint(self, np1, np2):
		for i in range(0, len(self.disjoint_noun_phrases) - 1):
			if np1 == self.disjoint_noun_phrases[i] or (np1.endswith('es') and np1[:-2] == self.disjoint_noun_phrases[i]) or (np1.endswith('s') and np1[:-1] == self.disjoint_noun_phrases[i]):
				if np2 == self.disjoint_noun_phrases[i + 1] or (np2.endswith('es') and np2[:-2] ==self. disjoint_noun_phrases[i + 1]) or (np2.endswith('s') and np2[:-1] == self.disjoint_noun_phrases[i + 1]):
					return 1

			if np2 == self.disjoint_noun_phrases[i] or (np2.endswith('es') and np2[:-2] == self.disjoint_noun_phrases[i]) or (np2.endswith('s') and np2[:-1] == self.disjoint_noun_phrases[i]):
				if np1 == self.disjoint_noun_phrases[i + 1] or (np1.endswith('es') and np1[:-2] == self.disjoint_noun_phrases[i + 1]) or (np1.endswith('s') and np1[:-1] == self.disjoint_noun_phrases[i + 1]):
					return 1
		return -1

	def find_same_head_np(self):
		for np1 in self.question_strings_np:
			for np2 in self.question_strings_np:
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

	def parse_np(self, noun_phrase):
		parts = noun_phrase.split(' ')
		index_parts = self.find_part_indexes(noun_phrase)
		rest_parts = ''
		head = ''
		for i in range(0, len(index_parts)):
			# finding the index of the previous paranteses
			index = index_parts[i] - 1
			while (index >= 0) and (self.ccg_parse_string[index] != '<'):
				index = index - 1
			index_np = index_parts[i]
			if self.ccg_parse_string[index + 4] == '/':
				rest_parts = rest_parts + self.ccg_parse_string[index_np:self.ccg_parse_string.find(" n/n>)" , index_np)] + ' '
			elif self.ccg_parse_string[index + 4] == ' ':
				head = head + self.ccg_parse_string[index_np:self.ccg_parse_string.find(" n>)" , index_np)] + ' '
				return (head[:-1], rest_parts[:-1])
		return (head[:-1], rest_parts[:-1])

	def check_validity(self, index_parts):
		return True
	
	def find_part_indexes(self, noun_phrase):
		parts = noun_phrase.split(' ')
		index_parts = []
		for i in range(0, len(parts)):
			index_parts.append(-1)
		index_parts[0] = self.ccg_parse_string.find(parts[0])
		for i in range(1, len(parts)):
			index_parts[i] = self.ccg_parse_string.find(parts[i])
			while (self.ccg_parse_string.find(parts[i - 1], index_parts[i - 1] + 1)  != -1) and (self.ccg_parse_string.find(parts[i - 1],  index_parts[i - 1] + 1)  <  index_parts[i]):
				index_parts[i - 1] = self.ccg_parse_string.find(parts[i - 1], index_parts[i - 1] + 1)
		return index_parts

	def find_noun_phrases_with_antonyms(self):
		for np1 in self.question_strings_np:
			if np1 not in self.antonym_list:
				continue
			for np2 in self.question_strings_np:
				if np2 not in self.antonym_list:
					continue
				index_np1 = self.antonym_list.index(np1)
				index_np2 = self.antonym_list.index(np2)
				if index_np1 % 2 == 0:
					if index_np2 == index_np1 + 1:
						if np1 not in self.antonym_list_inQuestion:
							self.antonym_list_inQuestion.append(np1)
							self.antonym_list_inQuestion.append(np2)
				elif index_np2 % 2 == 0:
					if index_np1 == index_np2 + 1:
						if np1 not in self.antonym_list_inQuestion:
							self.antonym_list_inQuestion.append(np1)

	def find_the_nouns_used_in_plural(self):
		for np in self.question_strings_np_before_article_ommiting:
			if (np.endswith('es') and np[:-2] in self.question_strings_np_before_article_ommiting_lemma) or (np.endswith('s') and np[:-1] in self.question_strings_np_before_article_ommiting_lemma):
				self.plural_used_nouns.append(np)


	def find_srl_args(self, demanded_arg):
		input_file  = open(self.srl_file_path, 'r')
		for line in input_file:
			line = line.lower()
			line = line[:-1]
			if line == "":
				continue
			parts = line.split(' ')
			if 'arg' + str(demanded_arg) == parts[1]:
				rest_noun = ''
				for j in range(2, len(parts)-1):
					rest_noun = rest_noun + parts[j]  + ' '
				rest_noun = rest_noun + parts[len(parts)-1]
				if rest_noun not in self.noun_phrase_srl_arg[demanded_arg]:
					self.noun_phrase_srl_arg[demanded_arg].append(rest_noun)
					self.verb_srl_related_np_arg[demanded_arg].append(parts[0])

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
				for noun_phrase in self.question_strings_np:
					if sentence.find(noun_phrase) > -1:
						if noun_phrase not in self.noun_phrases_in_question:
							self.noun_phrases_in_question.append(noun_phrase.lower())

	def find_noun_count_type(self, np):
		if np in self.noun_phrase_with_counts_with_count:
			return str(self.count_type_noun_phrase[self.noun_phrase_with_counts_with_count.index(np)])
		else:
			return '11'

	def find_count_noun_stanford(self, file_name):
		noun_phrase_with_counts = []
		res_parsing_mode = []
		input_file = open(file_name, 'r')
		parse_text = input_file.readline()
		index = parse_text.find('(CD');
		while index >=0 :
			# print index
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
		# print "noun_phrase_with_counts" 
		# print self.noun_phrase_with_counts_with_count
		return (noun_phrase_with_counts, res_parsing_mode)

	def read_parse_tree(self, file_name):
		input_file = open(file_name, 'r')
		for line in input_file:
			len_while_space = 0
			while line[len_while_space] == ' ':
				len_while_space = len_while_space + 1
			self.parse_tree_levels.append(len_while_space)
			self.parse_tree_sentences.append(line[len_while_space:-1].lower())

	def extract_phrase_parse_tree(self, index):
		parse_phrase = self.parse_tree_sentences[index]
		if ')' not in parse_phrase:
			return ''
		if '(np' not in parse_phrase:
			return ''
		result_np = ''
		parse_index = parse_phrase.find('(np') + 3
		opened_par = 1
		last_space_seen = 0
		last_par_close_seen = 0
		parse_chars = ''
		while opened_par != 0:
			if parse_phrase[parse_index] == ')':
				last_par_close_seen = parse_index
				opened_par = opened_par - 1
				if opened_par == 0:
					break
				if parse_chars == '(nn' or parse_chars == '(jj' or parse_chars == '(nns' or parse_chars == '(nnp':
					result_np = result_np + parse_phrase[last_space_seen+1:last_par_close_seen]+' '
				
			if parse_phrase[parse_index] == '(':
				opened_par = opened_par + 1
				parse_chars = ''
				while parse_phrase[parse_index] != ' ':
					parse_chars = parse_chars + parse_phrase[parse_index]
					parse_index = parse_index + 1
			if parse_phrase[parse_index] == ' ':
				last_space_seen = parse_index


			parse_index = parse_index + 1
		return result_np[:-1]

	def find_counted_noun_stan_parse_tree(self):
		for i in range(0, len(self.parse_tree_sentences)):
			parse_sent = self.parse_tree_sentences[i]
			if parse_sent.startswith('(vp ') and ('(cd ' in parse_sent):
				vp_level = self.parse_tree_levels[i]
				ind = i - 1
				while self.parse_tree_levels[ind] >= vp_level:
					np = self.extract_phrase_parse_tree(ind)
					if np != '':
						self.noun_phrase_with_counts.append(np)
					ind = ind -1

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

	def find_count_parsing_mode(self, noun_phrase):
		parsing_mode = -1
		if noun_phrase in self.noun_phrase_with_counts:
			index = self.noun_phrase_with_counts.index(noun_phrase)
			parsing_mode = self.count_type_noun_phrase[index]
		elif noun_phrase.endswith('es'):
			if noun_phrase[:-2] in self.noun_phrase_with_counts:
				index = self.noun_phrase_with_counts.index(noun_phrase[:-2])
				parsing_mode = self.count_type_noun_phrase[index]
		elif noun_phrase.endswith('s'):
			if noun_phrase[:-1] in self.noun_phrase_with_counts:
				index = self.noun_phrase_with_counts.index(noun_phrase[:-1])
				parsing_mode = self.count_type_noun_phrase[index]

		if parsing_mode == 0:
			return 1
		else:
			return 0

	def find_repeated_noun_phrases(self):
		repeated_noun_phrases = []
		for noun_phrase in self.question_strings_np:
			found_index = self.whole_question.find(noun_phrase) + 1
			if self.whole_question.find(noun_phrase, found_index) > -1:
				if noun_phrase not in self.repeated_noun_phrases:
					self.repeated_noun_phrases.append(noun_phrase)

	def check_for_person_names(self, file_name):
		parse_file = open(file_name, 'r')
		parse = ''
		for line in parse_file:
			parse = parse + line

		index_of_person_parse = parse.find('\', {u\'NamedEntityTag\': u\'PERSON')
		while index_of_person_parse > 0:
			prev_comma_index = index_of_person_parse - 1
			while(parse[prev_comma_index] != '\''):
				prev_comma_index = prev_comma_index - 1
			name = parse[prev_comma_index+1:index_of_person_parse]
			self.named_entity_nouns.append(name.lower())
			index_of_person_parse = parse.find('\', {u\'NamedEntityTag\': u\'PERSON', index_of_person_parse + 2)

		

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
			for np in self.noun_phrases_in_question:
				if np.startswith(main_part_before) or np.endswith(main_part_before) or np == main_part_before:
					self.related_words_with_conjunction.append(main_part)

			for i in range(1, len(parts)):
				for np in self.noun_phrases_in_question:
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
		for i in range(0, len(self.question_strings_np)):
			if self.question_strings_np[i].startswith(np1):
				ending_part = self.question_strings_np[i][len(np1) + 1:]
				for j in range(0, len(self.question_strings_np)):
					if j==i:
						continue
					if self.question_strings_np[j].startswith(np2) and self.question_strings_np[j].endswith(ending_part):
						if self.question_strings_np[j] not in res_list:
							res_list.append(self.question_strings_np[j])
							break
			elif self.question_strings_np[i].startswith(np2):
				ending_part = self.question_strings_np[i][len(np2) + 1:]
				for j in range(0, len(self.question_strings_np)):
					if j==i:
						continue
					if self.question_strings_np[j].startswith(np1) and self.question_strings_np[j].endswith(ending_part):
						if self.question_strings_np[j] not in res_list:
							res_list.append(self.question_strings_np[j])
						break
			elif self.question_strings_np[i].endswith(np1):
				starting_part = self.question_strings_np[i][:-1*len(np1) -1]
				for j in range(0, len(self.question_strings_np)):
					if j==i:
						continue
					if self.question_strings_np[j].endswith(np2) and self.question_strings_np[j].startswith(starting_part):
						if self.question_strings_np[j] not in res_list:
							res_list.append(self.question_strings_np[j])
						break
			elif self.question_strings_np[i].endswith(np2):
				starting_part = self.question_strings_np[i][:-1*len(np2) -1]
				for j in range(0, len(self.question_strings_np)):
					if j==i:
						continue
					if self.question_strings_np[j].endswith(np1) and self.question_strings_np[j].startswith(starting_part):
						if self.question_strings_np[j] not in res_list:
							res_list.append(self.question_strings_np[j])
						break
		return res_list

	def check_if_np_contains_number(self, np):
		parts = np.split(' ')
		if math_modifiers.is_word_number(parts[0]) == True:
			return 1
		if '-' in np:
			parts = np.split('-')
			if math_modifiers.is_word_number(parts[0]) == True:
				return 1
		return 0
	def check_if_np_contains_number_anywhere(self, np):
		parts = np.split(' ')
		if len(parts) == 1:
			return 0
		for i in range(0,len(parts)):
			part = parts[i]
			if math_modifiers.is_word_number(part) == True:
				return 1
			if '-' in part:
				parts_dash = np.split('-')
				if math_modifiers.is_word_number(parts_dash) == True:
					return 1
		return 0

	def check_relevant(self, np):
		for i in range(0, len(self.relevant_noun_phrases)):
			if np == self.relevant_noun_phrases[i] or (np.endswith('es') and np[:-2] == self.relevant_noun_phrases[i]) or (np.endswith('s') and np[:-1] == self.relevant_noun_phrases[i]):
				return 1
		return -1

	def in_noun_phrases_in_list(self, list, noun_phrase):
		if noun_phrase in list:
			return 1;
		elif noun_phrase.endswith('es'):
			if noun_phrase[:-2] in list:
				return 1
		elif noun_phrase.endswith('s'):
			if noun_phrase[:-1] in list:
				return 1
		return 0

	def find_antonym_relation(self, np1, np2):
		if (np1 not in self.antonym_list) or (np2 not in self.antonym_list):
			return 0
		index_np1 = self.antonym_list.index(np1)
		index_np2 = self.antonym_list.index(np2)
		if index_np1 % 2 == 0:
			if index_np2 == index_np1 + 1:
				return 1
		elif index_np2 % 2 == 0:
			if index_np1 == index_np2 + 1:
				return 1
		return 0 

	def have_same_head(self, np1, np2):
		parts_np1 = np1.split(' ')
		parts_np2 = np2.split(' ')
		if (len(parts_np1) < 2) or (len(parts_np2) < 2):
			return 0
		if (np1 in self.same_head_noun_phrases) and (np2 in self.same_head_noun_phrases) and (((self.same_head_noun_phrases.index(np1) - self.same_head_noun_phrases.index(np2)) == 1) or((self.same_head_noun_phrases.index(np2) - self.same_head_noun_phrases.index(np1)) == 1)):
			return 1
		return 0

	def find_sentence_proximity(self, np1, np2):
		index_np1 = -1
		index_np2 = -1
		max_distance = 20
		for i in range (0, len(self.question_strings)):
			if np1 in self.question_strings[i]:
				if i - index_np2 < max_distance:
					max_distance = i - index_np2
					index_np1 = i
			if np2 in self.question_strings[i]:
				if i - index_np1 <  max_distance:
					max_distance = i - index_np1
					index_np2 = i
		if max_distance > 7:
			max_distance = 7
		return str(bin(max_distance))[2:]

	def have_similar_verbs(self, np1, np2, demanded_arg, related_verbs):
		if (np1 not in demanded_arg) or (np2 not in demanded_arg):
			return 0
		if related_verbs[demanded_arg.index(np1)] ==  related_verbs[demanded_arg.index(np2)]:
			return 1
		return 0

	def find_edit_distance(self, np1, np2):
		num_of_edits = 0
		index_np1 = 0
		index_np2
		while index_np1 < len(np1):
			if np1[index_np1] == np2[index_np2]:
				index_np1 = index_np1 + 1
				index_np2 = index_np2 + 1
				
		
	def find_noun_phrases_after_question_phrase(self):
		for i in range (0, len(self.question_strings)):
			sentence = self.question_strings[i].lower()
			if '?' in sentence or (i == len(self.question_strings) -1):
				res_np = math_modifiers.find_np_after_question_phrase(sentence, self.question_strings_np)
				for np in res_np:
					if np not in self.noun_phrases_after_question_phrase:
						self.noun_phrases_after_question_phrase.append(np)
	
	def check_for_number_before(self, index_to_check):
		if self.whole_question[index_to_check - 1] == ' ':
			index_to_check = index_to_check - 1
			if (self.whole_question[index_to_check - 1] >= '0' and self.whole_question[index_to_check - 1] <= '9'):
				flag = True
				index_back = index_to_check - 1
				while (self.whole_question[index_back] != ' ' and index_back != 0):
					if not (self.whole_question[index_back] >= '0' and self.whole_question[index_to_check] <= '9'):
						flag = False
					index_back = index_back - 1
				return flag
			else:
				prev_space_index = index_to_check - 1
				while (self.whole_question[prev_space_index - 1] != ' ' and prev_space_index > 0):
					prev_space_index = prev_space_index - 1
				flag = math_modifiers.check_for_math_modifier(self.whole_question[prev_space_index:index_to_check])
				if flag == True :
					return True#self.check_for_number_before(prev_space_index)
				else: 
					return False

	def check_for_known_word(self, np):
		if math_modifiers.check_for_math_modifier(np) == True:
			return '1'
		else:
			return '0'

	def check_for_math_modifier_or_number_inside_np(self, np):
		parts = np.split(' ')
		part = parts[0]
		if self.check_for_known_word(part) == '1':
			return '1'
		elif math_modifiers.is_word_number(part) == True:
			return '1'
		if '-' in np:
			parts = np.split('-')
			part = parts[0]
			if self.check_for_known_word(part) == '1':
				return '1'
			elif math_modifiers.is_word_number(part) == True:
				return '1'
		return '0'
					
	def find_the_cosinge(self, mode,np1, np2, num_of_dimentions):
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
		
	def find_antonym_relation(self, np1, np2):
		if (np1 not in self.antonym_list) or (np2 not in self.antonym_list):
			return 0
		index_np1 = self.antonym_list.index(np1)
		index_np2 = self.antonym_list.index(np2)
		if index_np1 % 2 == 0:
			if index_np2 == index_np1 + 1:
				return 1
		elif index_np2 % 2 == 0:
			if index_np1 == index_np2 + 1:
				return 1
		return 0 
		
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

	def check_if_same_type(self, np1, np2):
		np1_contains_number = False
		np2_contains_number = False
		parts_np1 = np1.split(' ')
		parts_np2 = np2.split(' ')
		rest_part_np1 = ''
		rest_part_np2 = ''
		for part in parts_np1:
			if math_modifiers.is_word_number(part) == True and np1_contains_number != True:
				np1_contains_number = True
				continue
			elif '-' in part:
				temp_parts = part.split('-')
				for temp_part in temp_parts:
					if math_modifiers.is_word_number(temp_part) == True and np1_contains_number != True:
						np1_contains_number = True
						continue
					if np1_contains_number == True:
						rest_part_np1 = rest_part_np1 + temp_part

			if np1_contains_number==True:
						rest_part_np1 = rest_part_np1 + part

		for part in parts_np2:
			if math_modifiers.is_word_number(part) == True and np2_contains_number != True:
				np2_contains_number = True
				continue
			elif '-' in part:
				temp_parts = part.split('-')
				for temp_part in temp_parts:
					if math_modifiers.is_word_number(temp_part) == True and np2_contains_number != True:
						np2_contains_number = True
						continue
					if np2_contains_number==True:
						rest_part_np2 = rest_part_np2 + temp_part

			if np2_contains_number==True:
						rest_part_np2 = rest_part_np2 + part
		if rest_part_np1 == '':
			rest_part_np1 = np1
		if rest_part_np2 == '':
			rest_part_np2 = np2
		
		type_np1 = ''
		type_np2 = ''
		for np_type in self.enitity_types:
			if rest_part_np1 in np_type and len(np_type) > len(type_np1):
				type_np1 = np_type
			if rest_part_np2 in np_type and len(np_type) > len(type_np2):
				type_np2 = np_type

		if type_np1 == '' and type_np2 == '':
			return '000'
		if type_np1 == type_np2:
			return '100'
		if type_np1 in type_np2:
			return '010'
		if type_np2 in type_np1:
			return '001'
		else:
			return '000'

	def has_number_before(self, np1):
		index = self.whole_question.find(np1)
		while index > -1:
			if self.check_for_number_before(index) == True:
				return 1
			index = self.whole_question.find(np1, index + 1)
		return 0

	def flush(self):
		self.numeric_feature_helper = numeric_features()
		# self.word_vector = [[]]
		# self.word_list = []
		self.antonym_list = []
		self.ccg_parse_string = ''
		self.whole_question = ''
		self.question_strings = []
		self.question_strings_np = []
		self.question_strings_np_before_article_ommiting = [] #this is defined for findig plural
		self.question_strings_np_before_article_ommiting_lemma = [] #this is defined for finding plural 
		self.noun_phrase_with_counts = []
		self.noun_phrase_with_counts_with_count = []
		self.noun_phrases_in_question = []
		self.repeated_noun_phrases = []
		self.related_words_with_conjunction = []
		self.noun_phrase_srl_arg = [[] for x in range(3)] # Since we want to define arg0 to arg2
		self.verb_srl_related_np_arg = [[] for x in range(3)]
		self.same_head_noun_phrases_heads = []
		self.same_head_noun_phrases_ms = []
		self.same_head_noun_phrases = []
		self.antonym_list_inQuestion = []
		self.count_type_noun_phrase = []
		self.relevant_noun_phrases = []
		self.disjoint_noun_phrases = []
		self.subset_noun_phrases = []
		self.plural_used_nouns = []
		self.noun_phrases_after_question_phrase = []
		self.question_string_substrings = []
		self.POS_tags = {}
		self.place_noun_phrases = []
		self.named_entity_nouns = []
		self.enitity_types = []
		self.relevant_pairs = []
		self.equivalence_noun_phrases = []
		self.pronoun_list = []
		self.parse_tree_sentences = []
		self.parse_tree_levels = []

