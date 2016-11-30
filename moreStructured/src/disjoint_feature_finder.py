from entity_properties import entity_properties

class disjoint_feature_finder:
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

	def approriate_feature_found(self, start_index, np1, np2):
		# TODO find features based on the config file
		result = ''
		result = result + (str(start_index + 1) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.related_words_with_conjunction, np1)) + ' ')
		result = result + (str(start_index + 2) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.related_words_with_conjunction, np2)) + ' ')
		result = result + (str(start_index + 3) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.relevant_question_string_np, np1)) + ' ')
		result = result + (str(start_index + 4) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.relevant_question_string_np, np2)) + ' ')
		if (np1 in np2) or (np2 in np1):
			result = result + (str(start_index + 5) +':1 ')
		else:
			result = result + (str(start_index + 5) +':0 ')
		if self.question_prop.have_same_head(np1, np2) == 1:
			result = result + (str(start_index + 6) +':1 ')
			result = result + (str(start_index + 7) +':'+str(self.question_prop.find_antonym_relation(self.question_prop.same_head_noun_phrases_ms[self.question_prop.same_head_noun_phrases.index(np1)], self.question_prop.same_head_noun_phrases_ms[self.question_prop.same_head_noun_phrases.index(np2)])) + ' ')
			result = result + (str(start_index + 8) +':'+str(self.question_prop.find_the_cosinge(1,self.question_prop.same_head_noun_phrases_ms[self.question_prop.same_head_noun_phrases.index(np1)], self.question_prop.same_head_noun_phrases_ms[self.question_prop.same_head_noun_phrases.index(np2)], self.question_prop.num_of_dimentions)) + ' ')
		else:
			result = result + (str(start_index + 6) +':0 ' + str(start_index + 7) +':0 ' + str(start_index + 8) +':0 ')
		result = result + (str(start_index + 9) + ':' + (str(self.question_prop.find_antonym_relation(np1, np2))+ ' '))
		result = result + (str(start_index + 10)+ ':' + (str(self.question_prop.find_the_cosinge(0,np1, np2, self.question_prop.num_of_dimentions))+ ' '))
		for i in range(0, len(self.question_prop.noun_phrase_srl_arg)):
			result = result + (str(start_index + i + 11) + ':' + (str(self.question_prop.have_similar_verbs(np1, np2, self.question_prop.noun_phrase_srl_arg[i], self. question_prop.verb_srl_related_np_arg[i])))+ ' ')
		result = result + (str(start_index + len(self.question_prop.noun_phrase_srl_arg) + 11) + ':' + (str(self.question_prop.find_sentence_proximity(np1, np2))))
		return result, (start_index + len(self.question_prop.noun_phrase_srl_arg) + 11)

	def find_the_cosinge(mode,np1, np2, num_of_dimentions):
		# print "tsrat"
		# if mode == 1:
			# print word_list.index(np1)
			# print np1
			# print np2
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
		# if mode == 1:
			# print "here"
			# print sum1
			# print sum2
			# print sum3
			# print (sum1 + 0.0) / (math.sqrt(sum2) * math.sqrt(sum3))
		return (sum1 + 0.0) / (math.sqrt(sum2) * math.sqrt(sum3))



	def list_features_toString(self, start_index, np1, np2):
		result = ''
		result_str, result_index = self.approriate_feature_found(start_index, np1, np2)
		# print result_str
		return (result_str, result_index)



