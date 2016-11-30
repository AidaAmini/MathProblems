from entity_properties import entity_properties


class useful_np_feature_finder:
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

	def approriate_feature_found(self, start_index, np1):
		result  = ''
		result = result + (str(start_index + 1) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.related_words_with_conjunction, np1)) + ' ')
#		if self.question_prop.in_noun_phrases_in_list(self.question_prop.same_head_noun_phrases, np1) == 1:
#			result = result + (str(start_index + 2) +':1 ')
#			result = result + (str(start_index + 3) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.antonym_list_inQuestion, self.question_prop.same_head_noun_phrases_ms[self.question_prop.same_head_noun_phrases.index(np1)])) + ' ')
#			result = result + (str(start_index + 4) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.antonym_list_inQuestion, self.question_prop.same_head_noun_phrases_heads[self.question_prop.same_head_noun_phrases.index(np1)])) + ' ')
#		else:
#			result = result + (str(start_index + 2) +':0 ') #+ str(start_index + 3) +':0 ' + str(start_index + 4) +':0 ')
#		result = result + (str(start_index + 5) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.antonym_list_inQuestion, np1)) + ' ')
		
		result = result + (str(start_index + 2) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.plural_used_nouns, np1)) + ' ')
		binary_string = self.question_prop.find_pos_label(np1)
		result = result +  self.convert_binary_to_fv(self.question_prop.find_pos_label(np1), start_index + 3, 11) + ' '
		res_unit = self.question_prop.find_unit_type(np1)
		if res_unit == '000':
			result = result + str(start_index + 14) + ':0 '
		else:
			result = result + str(start_index + 14) + ':1 '

#		result = result + self.convert_binary_to_fv(self.question_prop.find_unit_type(np1), start_index+7, 3) + ' '
#		result = result + self.convert_binary_to_fv(self.question_prop.find_noun_count_type(np1), start_index+14, 2) + ' '
		result = result + str(start_index + 15)  +':'+ str(self.question_prop.check_if_np_contains_number(np1)) + ' '
		result = result + str(start_index + 16)  +':'+ str(self.question_prop.check_if_np_contains_number_anywhere(np1)) + ' '
		result = result + str(start_index + 17) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.place_noun_phrases, np1)) + ' '
		result = result + str(start_index + 18) + ':'+ self.question_prop.check_for_known_word(np1) + ' '
#			result = result + str(start_index + 14) + ':' + self.question_prop.check_for_math_modifier_or_number_inside_np(np1) + ' '
		result = result + (str(start_index + 19) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.named_entity_nouns, np1)) + ' ')
		result = result + (str(start_index + 20) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.same_head_noun_phrases, np1)) + ' ')
		
#		print  str(start_index + 14) 
		result = result + str(start_index + 21) + ':'+ self.question_prop.has_percent(np1)
		
#		print result
#		if len(np1.split(' ')) > 1:
#			result = result + self.convert_binary_to_fv(self.question_prop.find_unit_type(self.question_prop.same_head_noun_phrases_heads[self.question_prop.same_head_noun_phrases.index(np1)]), start_index+11, 3)
#		else:
#			result = result + "16:0 17:0 18:0"
		
		return result, start_index + 21

	def list_features_toString(self, start_index, np1):
		return self.approriate_feature_found(start_index, np1)
		















