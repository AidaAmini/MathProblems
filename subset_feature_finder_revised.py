from entity_properties import entity_properties

class subset_feature_finder_revised:
	question_prop = entity_properties()
	appropriate_features = []
	feature_file_path = ''

	def __init__(self, question_prop):
		# self.feature_file_path = ""
		self.question_prop = question_prop

	def find_demanded_features(self):
		input_file = open (self.feature_file_path, 'r')
		feature_line = input_file.readline();
		parts = feature_line.split(',')


	def appropriate_feature_finder_list(self, feature_list, np1, np2):

		np1_np2_same_head = self.question_prop.have_same_head(np1, np2)

		if np1_np2_same_head == 1:
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
		np1_q_subString = self.question_prop.in_noun_phrases_in_list(self.question_prop.question_string_substrings, np1)
		np2_q_substring = self.question_prop.in_noun_phrases_in_list(self.question_prop.question_string_substrings, np2)
		if np1_q_subString == 1 or np2_q_substring == 1:
			feature_list.append(1)
		else:
			feature_list.append(0)
		# feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.question_string_substrings, np1))
		# feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.question_string_substrings, np2))
		if ((np1 in np2) or (np2 in np1)) and (np1 != np2):
			feature_list.append(1)
		else:
			feature_list.append(0)
		return feature_list