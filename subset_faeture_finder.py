from entity_properties import entity_properties

class subset_faeture_finder:
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
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.question_string_substrings, np1))
		feature_list.append(self.question_prop.in_noun_phrases_in_list(self.question_prop.question_string_substrings, np2))
		if ((np1 in np2) or (np2 in np1)) and (np1 != np2):
			feature_list.append(1)
		else:
			feature_list.append(0)
		return feature_list