from entity_properties import entity_properties

class basic_faeture_finder:
	question_prop = entity_properties()
	appropriate_features = []
	feature_file_path = ''

	def __init__(self, question_prop):
		# self.feature_file_path = ""
		self.question_prop = question_prop
		# print question_prop.relevant_noun_phrases
		# self.find_demanded_features()

	def find_demanded_features(self):
		input_file = open (self.feature_file_path, 'r')
		feature_line = input_file.readline();
		parts = feature_line.split(',')
		# TODO strurctured way of defining the features

	def approriate_feature_found(self, start_index, np1):
		# TODO find features based on the config file -- add POS (if it was not found add part of speech of card)
		result  = ''
		result = result + (str(start_index + 1) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.noun_phrase_with_counts, np1)) + ' ')
		result = result + (str(start_index + 2) +':'+str(self.question_prop.has_number_before(np1)) + ' ') #merge two features TODO
		result = result + (str(start_index + 3) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.noun_phrases_in_question, np1)) + ' ')
		result = result + (str(start_index + 4) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.repeated_noun_phrases, np1))) + ' '
		result = result + (str(start_index + 5) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.noun_phrases_after_question_phrase, np1)))		
		return result, start_index + 5

	def list_features_toString(self, start_index, np1):
		return self.approriate_feature_found(start_index, np1)






















