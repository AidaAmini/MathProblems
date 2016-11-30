from math_modifiers import math_modifiers
class numeric_features:
	numeric_values_by_type = [[]]
	type_list = []
	list_of_relation_word = ['of']
	list_of_equivalence_relation_word = ['per', 'a', 'for'] 


	def find_all_numeric_values(self, type_name, whole_question):
		if type_name in self.type_list:
			return
		has_num, num = self.check_if_np_contains_number_anywhere(type_name)
		if has_num == 1:
			self.type_list.append(type_name)
			self.numeric_values_by_type.append(num)
			return 
		# print type_name
		if type_name not in whole_question:
			return
		index_type = whole_question.index(type_name)
		numeirc_values_for_this_type = []
		while index_type >= 0:
			word_count_before, beginning_of_the_word_index_before, word_list_inBetween_before = self.find_number_before(whole_question, index_type)
			word_count_after, beginning_of_the_word_index_after, word_list_inBetween_after = self.find_number_after(whole_question, index_type)
			if word_count_before <= word_count_after and word_count_before != -1:
				# print whole_question[beginning_of_the_word_index_before:whole_question.find(' ', beginning_of_the_word_index_before)]
				
				try:	
					numeric_value = float(whole_question[beginning_of_the_word_index_before:whole_question.find(' ', beginning_of_the_word_index_before)])
				# print beginning_of_the_word_index_before
				# print word_count_before
				# print type_name
				# print numeric_value
					numeirc_values_for_this_type.append(numeric_value)
				except:
					pass
			else:
				if word_count_after != -1:
					# print whole_question[beginning_of_the_word_index_after-10: beginning_of_the_word_index_after+ 10]
					try:
						numeric_value = float(whole_question[beginning_of_the_word_index_after:whole_question.find(' ', beginning_of_the_word_index_after)])
					# print beginning_of_the_word_index_after
					# print word_count_after
					# print type_name
					# print numeric_value
						numeirc_values_for_this_type.append(numeric_value)
					except:
						pass
			index_type = whole_question.find(type_name, index_type+1)
		self.type_list.append(type_name)
		self.numeric_values_by_type.append(numeirc_values_for_this_type)

	def check_if_largest_value_for_type(self, value, type_name):
		index = self.type_list.index(type_name)
		for val in self.numeric_values_by_type[index]:
			if val > value:
				return False
		return True

	def check_if_smallest_value_for_type(self, value, type_name):
		index = self.type_list.index(type_name)
		for val in self.numeric_values_by_type[index]:
			if val < value:
				return False
		return True

	def check_if_two_type_names_have_same_amount_of_counts(self, type_name1, type_name2):
		index1 = self.type_list.index(type_name1)
		index2 = self.type_list.index(type_name2)
		if len(self.numeric_values_by_type[index1]) == len(self.numeric_values_by_type[index2]):
			return True
		return False


	def find_number_after(self, whole_question, type_index):
		is_word_after_number = False
		space_index = self.find_next_space(whole_question, type_index+1)
		word_count = 0
		beginning_of_the_word_index = type_index
		word_list_inBetween = []
		while is_word_after_number == False:
			beginning_index = space_index + 1
			beginning_of_the_word_index = beginning_index

			space_index = self.find_next_space(whole_question, space_index + 1)

			end_of_the_word_index = space_index
			word_count = word_count + 1
			word_list_inBetween.append(whole_question[beginning_index:end_of_the_word_index])
			is_word_after_number = math_modifiers.is_word_number(whole_question[beginning_index:end_of_the_word_index])
			if space_index == len(whole_question):
				break
		if is_word_after_number == False:
			return (-1, -1, [])
		return (word_count, beginning_of_the_word_index, word_list_inBetween)

	def find_number_before(self, whole_question, type_index):
		is_word_before_number = False
		space_index = self.find_prev_space(whole_question, type_index)
		word_count = 0 
		beginning_of_the_word_index = 0
		word_list_inBetween = [] 
		while is_word_before_number == False:
			end_of_the_word_index = space_index
			space_index = self.find_prev_space(whole_question, space_index - 1)
			beginning_index = space_index + 1
			if space_index == 0:
				beginning_index = 0
				word_count = word_count + 1
			beginning_of_the_word_index = beginning_index
			word_count = word_count + 1
			word_list_inBetween.append(whole_question[beginning_index:end_of_the_word_index])
			is_word_before_number = math_modifiers.is_word_number(whole_question[beginning_index:end_of_the_word_index])
			if space_index == 0:
				break
		if is_word_before_number == False:
			return (-1, -1, [])
		return (word_count, beginning_of_the_word_index, word_list_inBetween)

	def find_prev_space(self, whole_question, index):
		while index > 0  and whole_question[index] != ' ':
			index = index - 1
		return index

	def find_next_space(self, whole_question, index):
		while index < len(whole_question) and whole_question[index] != ' ':
			index = index + 1
		return index

	def check_if_np_contains_number_anywhere(self, np):
		parts = np.split(' ')
#		print parts
		if len(parts) == 1:
			return (0, -1)
		for i in range(1,len(parts)):
			# print parts
			# print i
			part = parts[i]
			if math_modifiers.is_word_number(part) == True:
				return (1, part)
			if '-' in np:
				parts_dash = np.split('-')
				if math_modifiers.is_word_number(parts_dash) == True:
					return (1, parts_dash)
		return (0, -1)



