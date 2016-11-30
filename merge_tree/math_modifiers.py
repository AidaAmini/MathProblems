class math_modifiers:
	modifier_element_list = ['double', 'triple', 'more', 'less', 'twice', 'some', 'many', 'per', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
	sequential_modifier_elements = ['first', 'second', 'third', 'forth', 'fifth']
	single_digit_element_list = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
	question_string_clues = ['how many', 'how much', 'how old', 'number of', 'how much did']
	money_units = ['dollar', 'cent', 'nickel', 'dime']
	time_units = ['minute', 'hour', 'second', 'day', 'week', 'year','month']
	length_units = ['meter','centimeter', 'millimeter', 'mile', 'kilometer', 'yard', 'inch', 'feet']
	volume_units = ['milliliter', 'liter', 'gallon', 'ounce']
	unit_types = {"unkown":"000", "money": "001", "volume": "010", "time":"011", "length":"100"}
	
	@staticmethod
	def check_for_unit(word):
		global time_units
		global money_units 
		word = word.lower()
		word = word.replace(" ","")
		word = word.replace(",","")
		if word in math_modifiers.time_units:
			return math_modifiers.unit_types["time"]
		elif word in math_modifiers.money_units:
			return math_modifiers.unit_types["money"]
		elif word in math_modifiers.length_units:
			return math_modifiers.unit_types["length"]
		elif word in math_modifiers.volume_units:
			return math_modifiers.unit_types["volume"]
		else:
			return math_modifiers.unit_types["unkown"]		
		 
	@staticmethod
	def check_for_math_modifier(word):
		word = word.lower()
		word = word.replace(" ",'')
		word = word.replace(",",'')
		return word in math_modifiers.modifier_element_list
		
	@staticmethod
	def check_for_sequential_modifier(word):
		word = word.lower()
		word = word.replace(' ', '')
		word = word.replace(',', '')
		return word in math_modifiers.sequential_modifier_elements

	@staticmethod
	def check_for_single_digit_number(word):
		global single_digit_element_list
		word = word.lower()
		word = word.replace(" ",'')
		word = word.replace(",",'')
		return word in math_modifiers.single_digit_element_list
	
	@staticmethod
	def find_np_after_question_phrase(sentence, word_list):
		global question_string_clues
		qsc_in_sentence = ''
		for qsc in math_modifiers.question_string_clues:
			if qsc in sentence:
				qsc_in_sentence = qsc
				break
		if qsc_in_sentence != '':
			return []
		result = []
		index = sentence.index(qsc_in_sentence) + len(qsc_in_sentence) + 1
		for np in word_list:
			if np in sentence:
				np_index = sentence.index(np)
				while np_index < index and np_index != -1:
					np_index = sentence.find(np, index+1)
				if np_index == index:
					result.append(np)
		return result
	@staticmethod
	def is_word_number(word):
		for char in word:
			if not((char >= '0' and char <='9') or (char == '.') or (char == ',')):
				return False
		return True
	
	
	
		