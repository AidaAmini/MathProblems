class math_modifiers:
	modifier_element_list = ['double', 'triple', 'more', 'less', 'twice', ]
	single_digit_element_list = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'single']
	question_string_clues = ['how many', 'how much', 'how old', 'number of']

	@staticmethod
	def check_for_math_modifier(word):
		word = word.lower()
		word = word.replace(" ",'')
		word = word.replace(",",'')
		return word in self.modifier_element_list

	@staticmethod
	def check_for_single_digit_number(word):
		word = word.lower()
		word = word.replace(" ",'')
		word = word.replace(",",'')
		return word in self.single_digit_element_list