from entity_properties import entity_properties
from file_refrence import file_refrence

class disjoint_feature_finder:
	question_prop = entity_properties()
	appropriate_features = []
	feature_file_path = ''
	file_path_refrence = file_refrence()

	def __init__(self, question_prop):
		# self.feature_file_path = ""
		self.question_prop = question_prop

	def find_demanded_features(self):
		input_file = open (self.feature_file_path, 'r')
		feature_line = input_file.readline();
		parts = feature_line.split(',')
		# TODO strurctured way of defining the features
	def convert_binary_to_fv(self, binary_string, starting_index, total_size):
		while len(binary_string)  < total_size:
			binary_string = '0' + binary_string
		result = ''
		for i in range(0, total_size):
			result = result + str(starting_index + i) + ':' + binary_string[i]
			if i < total_size-1:
				result = result + ' '
		return result

	def appropriate_feature_finder_list_log_linear(self, feature_list, np1, np2):
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.related_words_with_conjunction, np1))
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.related_words_with_conjunction, np2))
		feature_list.append(self.question_prop.find_the_cosinge(0,np1, np2, 300))
		if self.question_prop.have_same_head(np1, np2) == 1:
			feature_list.append(1)
			feature_list.append(self.question_prop.find_antonym_relation(self.question_prop.same_head_noun_phrases_ms[self.question_prop.same_head_noun_phrases.index(np1)], self.question_prop.same_head_noun_phrases_ms[self.question_prop.same_head_noun_phrases.index(np2)]))
			feature_list.append(self.question_prop.find_the_cosinge(1,self.question_prop.same_head_noun_phrases_ms[self.question_prop.same_head_noun_phrases.index(np1)], self.question_prop.same_head_noun_phrases_ms[self.question_prop.same_head_noun_phrases.index(np2)], 300))
		else:
			feature_list.append(0)
			feature_list.append(0)
			feature_list.append(0)
		res_np1_np2_dist = self.question_prop.find_sentence_proximity(np1, np2)
		while len(res_np1_np2_dist) < 3:
			res_np1_np2_dist = '0' + res_np1_np2_dist
		for i in range(0, len(res_np1_np2_dist)):
			feature_list.append(int(res_np1_np2_dist[i]))
		return feature_list

	def appropriate_feature_finder_list(self, feature_list, np1, np2):
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.related_words_with_conjunction, np1))
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.related_words_with_conjunction, np2))
		
		if self.question_prop.have_same_head(np1, np2) == 1:
			feature_list.append(1)
			feature_list.append(self.question_prop.find_antonym_relation(self.question_prop.same_head_noun_phrases_ms[self.question_prop.same_head_noun_phrases.index(np1)], self.question_prop.same_head_noun_phrases_ms[self.question_prop.same_head_noun_phrases.index(np2)]))
			feature_list.append(self.question_prop.find_the_cosinge(1,self.question_prop.same_head_noun_phrases_ms[self.question_prop.same_head_noun_phrases.index(np1)], self.question_prop.same_head_noun_phrases_ms[self.question_prop.same_head_noun_phrases.index(np2)], 300))
		else:
			feature_list.append(0)
			feature_list.append(0)
			feature_list.append(0)
		# feature_list.append(self.question_prop.find_antonym_relation(np1, np2))
		feature_list.append(self.question_prop.find_the_cosinge(0,np1, np2, 300))
		# feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.plural_used_nouns, np1))
		# feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.plural_used_nouns, np2))
		res_unit_np1 = self.question_prop.find_unit_type(np1)
		res_unit_np2 = self.question_prop.find_unit_type(np2)
		if res_unit_np1 == '000':
			feature_list.append(0)
		else:
			feature_list.append(1)
		if res_unit_np2 == '000':
			feature_list.append(0)
		else:
			feature_list.append(1)
		if res_unit_np1 == res_unit_np2:
			feature_list.append(1)
		else:
			feature_list.append(0)
		# feature_list.append(self.question_prop.check_if_np_contains_number_anywhere(np1))
		# feature_list.append(self.question_prop.check_if_np_contains_number_anywhere(np2))
		feature_list.append(self.question_prop.check_for_known_word(np1))
		feature_list.append(self.question_prop.check_for_known_word(np2))
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.named_entity_nouns, np1))
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.named_entity_nouns, np2))
		# feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.enitity_types, np1))
		# feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.enitity_types, np2))		
		for i in range(0, len(self.question_prop.noun_phrase_srl_arg)):
			feature_list.append(self.question_prop.have_similar_verbs(np1, np2, self.question_prop.noun_phrase_srl_arg[i], self. question_prop.verb_srl_related_np_arg[i]))
		
		res_np1_np2_dist = self.question_prop.find_sentence_proximity(np1, np2)
		while len(res_np1_np2_dist) < 3:
			res_np1_np2_dist = '0' + res_np1_np2_dist
		for i in range(0, len(res_np1_np2_dist)):
			feature_list.append(int(res_np1_np2_dist[i]))
		# feature_list.append(self.question_prop.find_sentence_proximity(np1, np2))
		return feature_list			

	def find_the_cosinge(mode,np1, np2, num_of_dimentions):
		if (np2 not in word_list) or (np1 not in word_list):
			return 0
		index_np1 = word_list.index(np1)
		index_np2 = word_list.index(np2)
		sum1 = 0
		sum2 = 0
		sum3 = 0
		for i in range(0, num_of_dimentions):
			sum1 = sum1 + word_vector[index_np1][i] * word_vector[index_np2][i]
			sum2 = sum2 + word_vector[index_np1][i] * word_vector[index_np1][i]
			sum3 = sum3 + word_vector[index_np2][i] * word_vector[index_np2][i]
		return (sum1 + 0.0) / (math.sqrt(sum2) * math.sqrt(sum3))

	

