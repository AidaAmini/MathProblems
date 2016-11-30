from entity_properties import entity_properties

class equivalence_feature_finder:
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

	def appropriate_feature_finder_list(self, feature_list, np1, np2):
		feature_list.append(self.question_prop.find_if_both_are_in_a_same_sentence(np1, np2))
		feature_list.append(self.question_prop.find_per_equivalence_rule_value(np1, np2))
		# feature_list.append(self.question_prop.check_if_both_has_greatest_val(np1, np2))
		feature_list.append(self.question_prop.find_if_any_equivalence_word_in_between(np1, np2))
		feature_list.append(self.question_prop.check_if_both_has_lowest_val(np1, np2))
		feature_list.append(self.question_prop.check_if_both_has_same_number_of_numbers(np1, np2))
		res_np1_np2_dist = bin(self.question_prop.find_nps_min_distance(np1,np2))[2:]
		while len(res_np1_np2_dist) < 3:
			res_np1_np2_dist = '0' + res_np1_np2_dist
		for i in range(0, len(res_np1_np2_dist)):
			feature_list.append(int(res_np1_np2_dist[i]))
		return feature_list


	def approriate_feature_found(self, start_index, np1, np2):
		# TODO find features based on the config file
		result = ''
		result = result + (str(start_index + 1) +':'+str(self.question_prop.find_if_both_are_in_a_same_sentence(np1, np2)) + ' ')
		result = result + (str(start_index + 2) +':'+str(self.question_prop.find_per_equivalence_rule_value(np1, np2)) + ' ')
		# result = result + (str(start_index + 3) +':'+str(self.question_prop.check_if_both_has_greatest_val(np1, np2)) + ' ')
		result = result + (str(start_index + 4) +':'+str(self.question_prop.find_if_any_equivalence_word_in_between(np1, np2)) + ' ') # TODO
		# result = result + (str(start_index + 5) +':'+str(self.question_prop.check_if_both_has_lowest_val(np1, np2)) + ' ')
		# result = result + (str(start_index + 6) +':'+str(self.question_prop.check_if_both_has_same_number_of_numbers(np1, np2)) + ' ')
		# res_np1_np2_dist = self.question_prop.find_nps_min_distance(np1,np2)
		# result = result + self.convert_binary_to_fv(str(bin(res_np1_np2_dist)[2:]), (start_index + 7), 3)
		

		# additional here
		# res_unit_np1 = self.question_prop.find_unit_type(np1)
		# res_unit_np2 = self.question_prop.find_unit_type(np2)
		# if res_unit_np1 == '000':
		# 	result = result + str(start_index + 10) + ':0 '
		# else:
		# 	result = result + str(start_index + 10) + ':1 '

		# if res_unit_np1 == '000':
		# 	result = result + str(start_index + 11) + ':0 '
		# else:
		# 	result = result + str(start_index + 11) + ':1 '
		# if res_unit_np1 == res_unit_np2:
		# 	result = result + str(start_index + 12) + ':1 '
		# else:
		# 	result = result + str(start_index + 12) + ':0 '

		# result = result + str(start_index + 13)  +':'+ str(self.question_prop.check_if_np_contains_number_anywhere(np1)) + ' '
		# result = result + str(start_index + 14)  +':'+ str(self.question_prop.check_if_np_contains_number_anywhere(np2)) + ' '
		# result = result + str(start_index + 15) + ':'+ self.question_prop.check_for_known_word(np1) + ' '
		# result = result + str(start_index + 16) + ':'+ self.question_prop.check_for_known_word(np2) + ' '
		# result = result + (str(start_index + 17) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.named_entity_nouns, np1)) + ' ')
		# result = result + (str(start_index + 18) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.named_entity_nouns, np2)) + ' ')
		# result = result + (str(start_index + 19) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.enitity_types, np1)) + ' ')
		# result = result + (str(start_index + 20) +':'+str(self.question_prop.in_noun_phrases_in_list(self.question_prop.enitity_types, np2)) + ' ')
		# res_np1_np2_same_type = self.question_prop.check_if_same_type(np1,np2)
		# # print res_np1_np2_same_type
		# result = result + self.convert_binary_to_fv(res_np1_np2_same_type, (start_index + 21), 3)+ ' '
		# for i in range(0, len(self.question_prop.noun_phrase_srl_arg)):
		# 	result = result + (str(start_index + i + 24) + ':' + (str(self.question_prop.have_similar_verbs(np1, np2, self.question_prop.noun_phrase_srl_arg[i], self. question_prop.verb_srl_related_np_arg[i])))+ ' ')


		return result, (start_index + 24)

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




