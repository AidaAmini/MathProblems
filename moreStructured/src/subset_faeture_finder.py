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

	def approriate_feature_found(self, start_index, np1, np2):
		# TODO find features based on the config file
		result = ''
		result = result + (str(start_index + 1) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.question_string_substrings, np1)) + ' ')
		result = result + (str(start_index + 2) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.question_string_substrings, np2)) + ' ')
		return result, (start_index + len(self.question_prop.noun_phrase_srl_arg) + 2)

	def list_features_toString(self, start_index, np1, np2):
		result = ''
		result_str, result_index = self.approriate_feature_found(start_index, np1, np2)
		# print result_str
		return (result_str, result_index)