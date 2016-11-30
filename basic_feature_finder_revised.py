from entity_properties import entity_properties

class basic_feature_finder_revised:
	question_prop = entity_properties()
	appropriate_features = []
	feature_file_path = ''

	def __init__(self, question_prop):
		self.question_prop = question_prop
		# self.find_demanded_features()

	def find_demanded_features(self):
		input_file = open (self.feature_file_path, 'r')
		feature_line = input_file.readline();
		parts = feature_line.split(',')
		
	def appropriate_feature_finder_list(self, feature_list, np1, np2):
		np1_with_count = self.question_prop.in_noun_phrases_in_list(self.question_prop.noun_phrase_with_counts, np1)
		np2_with_count = self.question_prop.in_noun_phrases_in_list(self.question_prop.noun_phrase_with_counts, np2)
		np1_after_q_string = self.question_prop.in_noun_phrases_in_list(self.question_prop.noun_phrases_after_question_phrase, np1)
		np2_after_q_string = self.question_prop.in_noun_phrases_in_list(self.question_prop.noun_phrases_after_question_phrase, np2)
		if not (((np1_with_count == 1) or (np1_after_q_string == 1)) and ((np2_with_count == 1) or (np2_after_q_string == 1))):
			feature_list.append(1)
		else:
			feature_list.append(0)

		np1_repeated = self.question_prop.in_noun_phrases_in_list(self.question_prop.repeated_noun_phrases, np1)
		np2_repeated = self.question_prop.in_noun_phrases_in_list(self.question_prop.repeated_noun_phrases, np2)

		if not ((np1_repeated == 1) and (np2_repeated == 1)):
			feature_list.append(1)
		else:
			feature_list.append(0)
		if not ((np1_after_q_string == 1) and (np2_after_q_string == 1)):
			feature_list.append(1)
		else:
			feature_list.append(0)

		np1_is_place = self.question_prop.in_noun_phrases_in_list(self.question_prop.place_noun_phrases, np1)
		np2_is_place = self.question_prop.in_noun_phrases_in_list(self.question_prop.place_noun_phrases, np2)
		if ((np1_is_place == 0) or (np2_is_place == 0)):
			feature_list.append(1)
		else:
			feature_list.append(0)

		np1_is_named_entity = self.question_prop.in_noun_phrases_in_list(self.question_prop.named_entity_nouns, np1)
		np2_is_named_entity = self.question_prop.in_noun_phrases_in_list(self.question_prop.named_entity_nouns, np2)
		if ((np1_is_named_entity == 0) or (np2_is_named_entity == 0)):
			feature_list.append(1)
		else:
			feature_list.append(0)

		np1_is_type = self.question_prop.in_noun_phrases_in_list(self.question_prop.enitity_types, np1)
		np2_is_type = self.question_prop.in_noun_phrases_in_list(self.question_prop.enitity_types, np2)
		if not((np1_is_type == 1) and (np2_is_type ==1)):
			feature_list.append(1)
		else:
			feature_list.append(0)

		return feature_list





