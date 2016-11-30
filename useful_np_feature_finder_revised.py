from entity_properties import entity_properties


class useful_np_feature_finder_revised:
	question_prop = entity_properties()
	appropriate_features = []
	feature_file_path = ''

	def __init__(self, question_prop):
		self.question_prop = question_prop

	def find_demanded_features(self):
		input_file = open (self.feature_file_path, 'r')
		feature_line = input_file.readline();
		parts = feature_line.split(',')
	
	def convert_binary_to_fv(self, binary_string, starting_index, total_size):
		while len(binary_string)  < total_size:
			binary_string = '0' + binary_string
		result = ''
		for i in range(0, total_size):
			result = result + str(starting_index + i) + ':' + binary_string[i]
			if i < total_size-1:
				result = result + ' '
		return result

	def appropriate_feature_finder_list(self, feature_list, np1, np2):
		# feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.related_words_with_conjunction, np1))
		# feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.place_noun_phrases, np1))
		# feature_list.append(self.question_prop.check_if_np_contains_number(np1))
		# feature_list.append(self.question_prop.check_for_known_word(np1))
		# feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.named_entity_nouns, np1))
		# feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.same_head_noun_phrases, np1))
		np1_has_percent = self.question_prop.has_percent(np1)
		np2_has_percent = self.question_prop.has_percent(np2)
		if np1_has_percent == 1 or np2_has_percent == 1:
			feature_list.append(1)
		else:
			feature_list.append(0)

		if np1_has_percent == 1 and np2_has_percent == 1:
			feature_list.append(1)
		else:
			feature_list.append(0)

		# feature_list.append(self.question_prop.has_percent(np1))
		# feature_list.append(self.question_prop.check_if_np_contains_number_anywhere(np1))
		np1_dash = 0
		if '-' in np1:
			np1_dash = 1
		np2_dash = 0
		if '-' in np2:
			np2_dash = 1
		if np1_dash == 1 and np2_dash == 1:
			feature_list.append(1)
		else:
			feature_list.append(0)

		if np1_dash == 1 or np2_dash == 1:
			feature_list.append(1)
		else:
			feature_list.append(0)

		np1_len = 0
		if len(np1.split(' ')) > 4:
			np1_len = 1
		np2_len = 0
		if len(np2.split(' ')) > 4:
			np2_len = 1

		if np1_len == 1 or np2_len == 1:
			feature_list.append(1)
		else:
			feature_list.append(0)
		return feature_list


	def approriate_feature_found(self, start_index, np1):
		result  = ''
		# print self.question_prop.related_words_with_conjunction
		result = result + (str(start_index + 1) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.related_words_with_conjunction, np1)) + ' ')
		result = result + (str(start_index + 2) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.plural_used_nouns, np1)) + ' ')
		binary_string = self.question_prop.find_pos_label(np1)
		result = result +  self.convert_binary_to_fv(self.question_prop.find_pos_label(np1), start_index + 3, 2) + ' '
		res_unit = self.question_prop.find_unit_type(np1)
		if res_unit == '000':
			result = result + str(start_index + 5) + ':0 '
		else:
			result = result + str(start_index + 5) + ':1 '
		# result = result + str(start_index + 15)  +':'+ str(self.question_prop.check_if_np_contains_number(np1)) + ' '
		result = result + str(start_index + 6) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.place_noun_phrases, np1)) + ' '
		result = result + str(start_index + 7) + ':'+ self.question_prop.check_for_known_word(np1) + ' '
		result = result + (str(start_index + 8) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.named_entity_nouns, np1)) + ' ')
		# print self.question_prop.same_head_noun_phrases
		result = result + (str(start_index + 9) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.same_head_noun_phrases, np1)) + ' ')
		result = result + str(start_index + 10) + ':'+ self.question_prop.has_percent(np1) + ' '
		result = result + str(start_index + 11)  +':'+ str(self.question_prop.check_if_np_contains_number_anywhere(np1)) + ' '
		
		if '-' in np1:
			result = result + str(start_index + 12) + ':1 '
		else:
			result = result + str(start_index + 12) + ':0 '

		if len(np1.split(' ')) > 4:
			result = result + str(start_index + 13) + ':1'
		else:
			result = result + str(start_index + 13) + ':0'
				
		return result, start_index + 14

	def list_features_toString(self, start_index, np1):
		return self.approriate_feature_found(start_index, np1)
		


