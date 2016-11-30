from math_modifiers import math_modifiers
from POSTags import POSTags
import math

class entity_properties:
	word_vector = [[]]
	word_list = []
	antonym_list = []
	ccg_parse_string = ''
	whole_question = ''
	question_strings = []
	question_strings_np = []
	relevant_question_string_np = [] # the ones that i have found with classifier
	question_strings_np_before_article_ommiting = [] #this is defined for findig plural
	question_strings_np_before_article_ommiting_lemma = [] #this is defined for finding plural 
	noun_phrase_with_counts = []
	noun_phrase_with_counts_with_count = []
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
	subset_noun_phrases = []
	plural_used_nouns = []
	question_string_substrings = []
	srl_file_path = ''
	num_of_dimentions = 300
	POS_tags = {} #This should be 2 dimentional map from one word to all the tags it gets.
	place_noun_phrases = []


	def __init__(self):
		self.find_list_antonyms("../../question-antonyms.dat")

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
#			print line
			pos = parts[1]
#			print word
			if word in  self.POS_tags:
				self.POS_tags[word] = self.POS_tags[word] + '	' + pos
			else:
				self.POS_tags[word] = pos
#			print word
#			print self.POS_tags[word]
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
		
		for np in self.question_strings_np:
			for i in range(0, len(words)):
				if words[i] == np:
					index=i-1
					if index < 0:
						continue
					while pos[index] == 'dt':
						index = index -1
							
					if pos[index] == 'in':
						if words[index] == 'at' or words[index] == 'in':
							self.place_noun_phrases.append(np)
					
#		print self.place_noun_phrases
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

	def read_relevant_question_string_np(self, file_name):
 		input_file = open(file_name, 'r')
 		for np in input_file:
			if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
				self.relevant_question_string_np.append(np[:-3].lower())
			else:
				self.relevant_question_string_np.append(np[:-1].lower())

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
			line = line[:-2]
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
		else:
			return 0
	
	def check_if_subset(self, np1, np2):
#		print "subset"
#		print self.subset_noun_phrases
		for i in range(0, len(self.subset_noun_phrases) - 1 ):
			if np1 == self.subset_noun_phrases[i] or (np1.endswith('es') and np1[:-2] == self.subset_noun_phrases[i])  or (np1.endswith('s') and  np1[:-1] == self.subset_noun_phrases[i]):
				if np2 == self.subset_noun_phrases[i + 1]  or (np2.endswith('es') and np2[:-2] == self.subset_noun_phrases[i + 1]) or (np2.endswith('s') and np2[:-1] == self.subset_noun_phrases[i + 1]) :
					return 1
			if np2 == self.subset_noun_phrases[i] or (np2.endswith('es') and np2[:-2] == self.subset_noun_phrases[i]) or (np2.endswith('s') and np2[:-1] == self.subset_noun_phrases[i]):
				if np1 == self.subset_noun_phrases[i + 1] or (np1.endswith('es') and np1[:-2] == self.subset_noun_phrases[i + 1]) or (np1 .endswith('s') and np1[:-1] == self.subset_noun_phrases[i + 1]):
					return 1
		return -1
		
	def find_pos_for_single_noun(self, np1) :
		parts = []
		if '	' not in self.POS_tags[np1]:
			parts.append(self.POS_tags[np1])
			res = POSTags.pos_tag_to_bin(parts[0])
#			print parts[0]
#			print res
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
#			print pos
			res = POSTags.pos_tag_to_bin(pos)
#			print res
			return res
			
	def find_pos_label(self, np1):
		if np1 in self.POS_tags:
			# I want to find the maximum repetition 
			return self.find_pos_for_single_noun(np1)
		else:
			head_np1, modifier_np1 = self.parse_np(np1)
#			print head_np1
			if head_np1 not in self.POS_tags:
				return "1111"
			return  self.find_pos_for_single_noun(head_np1)
			
#			return res
			
	def find_unit_type(self, np1):
		if len(np1.split(' ')) > 1:
			head_np1, modifier_np1 = self.parse_np(np1)
			return math_modifiers.check_for_unit(head_np1)
		return math_modifiers.check_for_unit(np1)
		
	def read_disjoint_noun_phrase(self, file_name):
		input_file = open(file_name, 'r')
		for line in input_file:
			line = line[:-2]
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
					if head_np2 == head_np1:
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
		if (self.check_validity(index_parts) == False):
			return (None, None)
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
#			if np[:-1] in self.question_strings_np_before_article_ommiting_lemma:
#				print np
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

	def find_noun_phrases_in_question(self):
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
		while index >=0:
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
#		print self.count_type_noun_phrase
#		print self.noun_phrase_with_counts
#		print self.noun_phrase_with_counts_with_count
		return (noun_phrase_with_counts, res_parsing_mode)

	def find_parsing_mode(self, file_name, index):
		# this function looks for a type of the relation among the number and the noun_phrase.
		# here index is the index of founded '(CD' which is a refrence for the number
		parse_file = open(file_name, 'r')
		parse_text = parse_file.readline()
		next_open_parantese_index = parse_text.find('(', index + 1)
		# if parse_text[index-3: index-1] == 'NP':
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

	def find_related_words_with_conjunction(self, file_name):
		parse_file = open(file_name, 'r')
		parse_text = parse_file.readline()
		index = parse_text.find('[u\'conj_')
		while index > -1:
			part_text = parse_text[index:parse_text.find(']', index+1)].lower()
			parts = part_text.split(', u\'')
			for i in range(1, len(parts)):
				parts[i] = parts[i][:-1].lower()
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
#		print parts
		if math_modifiers.is_word_number(parts[0]) == True:
			return 1
		if '-' in np:
			parts = np.split('-')
			if math_modifiers.is_word_number(parts[0]) == True:
				return 1
		return 0
	def check_if_np_contains_number_anywhere(self, np):
		parts = np.split(' ')
#		print parts
		for part in parts:
			if math_modifiers.is_word_number(part) == True:
				return 1
			if '-' in np:
				parts = np.split('-')
				if math_modifiers.is_word_number(parts) == True:
					return 1
		return 0

	def check_relevant(self, np):
		if np == 'senior citizen ticket':
			print self.relevant_noun_phrases
#		print self.relevant_noun_phrases
		for i in range(0, len(self.relevant_noun_phrases)):
			if np == self.relevant_noun_phrases[i] or (np.endswith('es') and np[:-2] == self.relevant_noun_phrases[i]) or (np.endswith('s') and np[:-1] == self.relevant_noun_phrases[i]):# or np in self.relevant_noun_phrases[i]:
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
				# print 1
				return 1
		elif index_np2 % 2 == 0:
			if index_np1 == index_np2 + 1:
				# print 1
				return 1
		return 0 

	def have_same_head(self, np1, np2):
		global same_head_noun_phrases
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
#		print index_to_check
		print_flag = False
		if self.whole_question[index_to_check -7 : index_to_check  -1]  =='second':
			print self.whole_question[index_to_check  : index_to_check  +4] 
			print_flag = True 
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
				if print_flag == True:
					print "heeeeeepppppppppp"
					print flag
					print self.whole_question[prev_space_index:index_to_check]
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


	def has_number_before(self, np1):
		index = self.whole_question.find(np1)
		while index > -1:
			if self.check_for_number_before(index) == True:
				return 1
			index = self.whole_question.find(np1, index + 1)
		return 0
	

	def has_math_modifier():
		print "TODO"

	def flush(self):
		self.word_vector = [[]]
		self.word_list = []
		self.antonym_list = []
		self.ccg_parse_string = ''
		self.whole_question = ''
		self.question_strings = []
		self.question_strings_np = []
		self.relevant_question_string_np = [] # the ones that i have found with classifier
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


#entity_property = entity_properties()
#print 'here'
#entity_property.whole_question = "2000 more questions"
#print entity_property.check_for_number_before(10)





