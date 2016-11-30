from entity_properties import entity_properties

class basic_faeture_finder:
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
		
	def appropriate_feature_finder_list(self, feature_list, np1):
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.noun_phrase_with_counts, np1))
		feature_list.append(self.question_prop.has_number_before(np1))
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.noun_phrases_in_question, np1))
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.repeated_noun_phrases, np1))
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.noun_phrases_after_question_phrase, np1))
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.place_noun_phrases, np1))
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.named_entity_nouns, np1))
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.enitity_types, np1))
		return feature_list


















