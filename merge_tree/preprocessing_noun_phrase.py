
def omit_numbers(question_strings_np):
#	print question_strings_np
	result_list = []
	for noun_phrase in question_strings_np:
		parts = noun_phrase.split(' ')
		if len(parts) > 1:
			if noun_phrase not in result_list:
				result_list.append(noun_phrase)
		elif len(parts) == 1:
			for char in parts[0]:
				if not (char >='0' and char <= '9'):
					if noun_phrase not in result_list:
						result_list.append(noun_phrase)
	return result_list

def read_names():
	names_list = []
	names_file = open('names.txt', 'r')
	for line in names_file:
		names_list.append(line[:-1].lower())
	return names_list

def omit_names(question_strings_np, names_list):
	result_list = []
	print 'susan' in names_list
	for np in question_strings_np:
		print np
		print np not in names_list

		if np not in names_list and np not in result_list:
			result_list.append(np)
	return result_list

def add_no_opostrope_s(question_strings_np):
	result_list = []
	for np in question_strings_np:
		if '\'s' in np:
			rest_noun = ''
			parts = np.split(' ')
			for part in parts:
				if '\'s' in part:
					rest_noun = rest_noun + part[:part.index('\'s')]+ ' '
				else:
					rest_noun = rest_noun + ' '
			result_list.append(rest_noun)
		result_list.append(np)
	return result_list

def refine_articles(question_strings_np):
	result_list = []
	for noun_phrase in question_strings_np:
		if ' cost ' in noun_phrase:
			continue
		parts = noun_phrase.split(' ')
		if parts[0] == 'a' or parts[0] == 'an' or parts[0] == 'one' or parts[0] == 'the' or parts[0] == 'many':
			rest_noun = ''
			for i in range(1, len(parts)):
				rest_noun = rest_noun + parts[i]+' '
			if rest_noun[:-1] in question_strings_np:
				continue
			else:
				result_list.append(rest_noun[:-1])
		elif len(parts) >1 and parts[0] == 'and' and (parts[1] == 'a' or parts[1] == 'an' or parts[1] == 'one' or parts[1] == 'the' or parts[1] == 'many'):
			rest_noun = ''
			for i in range(2, len(parts)):
				rest_noun = rest_noun + parts[i]+' '
			if rest_noun[:-1] in question_strings_np:
				continue
			else:
				result_list.append(rest_noun[:-1])

		else:
			if noun_phrase not in result_list:
				result_list.append(noun_phrase)
	return result_list

def omit_question_strings(question_strings_np):
	result_list = []
	for noun_phrase in question_strings_np:
		noun_phrase = noun_phrase.lower()
		parts = noun_phrase.split(' ')
		if parts[0] == 'how':
			start_index = 2
			if len(parts) > 2 and (parts[2] == 'did' or parts[2] == 'does' or parts[2] == 'do' or parts[2] == 'is' or parts[2] == 'are'):
				start_index = 3
			rest_noun = ''
			for i in range(start_index, len(parts)):
				rest_noun = rest_noun + parts[i]+' '
			if rest_noun[:-1] in question_strings_np:
				continue
			else:
				result_list.append(rest_noun[:-1])
		else:
			if noun_phrase not in result_list:
				result_list.append(noun_phrase)
	return result_list

def omit_cost(question_string_np):
	result_list = []
	for noun_phrase in question_string_np:
		noun_phrase = noun_phrase.lower()
		parts = noun_phrase.split(' ')
		if parts[0] == 'cost':
			rest_noun = ''
			for i in range(1, len(parts)):
				rest_noun = rest_noun + parts[i]+' '
			if rest_noun[:-1] in question_string_np:
				continue
			else:
				result_list.append(rest_noun[:-1])
		else:
			if noun_phrase not in result_list and 'cost' not in noun_phrase:
				result_list.append(noun_phrase)
	return result_list

def omit_word_from_beginning(question_string_np, omitting_word):
	result_list = []
	for noun_phrase in question_string_np:
		noun_phrase = noun_phrase.lower()
		# print question_string_np
		parts = noun_phrase.split(" ")
		# print parts
		if parts[0] == omitting_word:
			rest_noun = ''
			for i in range(1, len(parts)):
				rest_noun = rest_noun + parts[i] + ' '
			if rest_noun[:-1] in question_string_np:
				continue
			else:
				result_list.append(rest_noun[:-1])
		else:
			if noun_phrase not in result_list:
				result_list.append(noun_phrase)
	return result_list

def omit_word_from_end(question_string_np, omitting_word):
	result_list = []
	for noun_phrase in question_string_np:
		noun_phrase = noun_phrase.lower()
		parts = noun_phrase.split(' ')
		if parts[len(parts) - 1] == omitting_word:
			rest_noun = ''
			for i in range(0, len(parts) - 1):
				rest_noun = rest_noun + parts[i] + ' '
			if rest_noun[:-1] in question_string_np:
				continue
			else:
				result_list.append(rest_noun[:-1])
		else:
			if noun_phrase not in result_list:
				result_list.append(noun_phrase)
	return result_list

def add_implicit_heads(question_strings_np):
	result_list = []
	seen_heads = []
	for noun_phrase in question_strings_np:
		parts = noun_phrase.split(' ')
		if len(parts) > 1:
			head = parts[len(parts) - 1]
			if head in seen_heads:
				if head not in result_list:
					result_list.append(head)
			else:
				seen_heads.append(head)
		if noun_phrase not in result_list:
			result_list.append(noun_phrase)
	return result_list

def omit_modifiers_from_the_end(question_strings_np):
	modifier_element_list = ['total', 'combined', 'combine', 'altogather', 'only', 'each', 'sell']
	result_list = []
	for noun_phrase in question_strings_np:
		parts = noun_phrase.split(' ')
		last_index = len(parts) - 1
		if not parts[last_index] in modifier_element_list:
			if noun_phrase not in result_list:
				result_list.append(noun_phrase)
		else:
			rest_noun = ''
			for i in range(0, last_index):
				rest_noun = rest_noun + parts[i] + ' '
			if rest_noun[:-1] in question_strings_np or rest_noun == '':
				continue
			else:
				result_list.append(rest_noun)
	return result_list


def omit_math_modifiers(question_strings_np):
	modifier_element_list = [ 'triple', 'more', 'less', 'twice', 'some', 'only','any', 'many', 'number', 'total', 'time', 'much', 'amount', 'how', 'where', 'there']
	two_wrods_modifier_elements = ['as many', 'as much']
	result_list = []
	for noun_phrase in question_strings_np:
		parts = noun_phrase.split(' ')
		if not parts[0] in modifier_element_list:
			flag = True
			for modifier in two_wrods_modifier_elements:
				if modifier in noun_phrase:
					flag  = False
			if flag == True:
				result_list.append(noun_phrase)
		else:
			rest_noun = ''
			for i in range(1, len(parts)):
				rest_noun = rest_noun + parts[i]+' '
			if rest_noun[:-1] in question_strings_np or rest_noun == '':
				continue
			else:
				result_list.append(rest_noun[:-1])

	return result_list
	
def is_word_number(word):
		for char in word:
			if not((char >= '0' and char <='9') or (char == '.') or (char == ',')):
				return False
			else:
				return True

def omit_number_beginning_expect_question(question_strings_np):
	result_list = []
	for word in question_strings_np:
		parts = word.split(' ')
		if '-' in word:
			parts = word.split('-')		
		# comma_dot_flag = False
		written_number_list = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'hundered']
		if not parts[0] in written_number_list:
			for char in parts[0]:
				if not (char >='0' and char <= '9') :				
					if word not in result_list:
						if (char ==',' or char == '.'):
							# comma_dot_flag = True
							continue
						result_list.append(word)
		# if  word not in result_list:
		# 	result_list.append(word)
	return result_list

def omit_places(question_strings_np, pos_file_name, index_file):
	result_list = []
	res_not = []
	words= []
	pos = []
	input_file = open(pos_file_name, 'r')
	for line in input_file:
		line = line[:-1].lower()
		if line == "":
			break
		
		parts = line.split("/")
		words.append(parts[0])
		pos.append(parts[1])
	for np in question_strings_np:
		flag = False
		for i in range(0, len(words)):
			if words[i] == np:
				index=i-1
				if index < 0:
					continue
				while pos[index] == 'dt':
					index = index -1
				if pos[index] == 'in':
					if words[index] == 'at' or words[index] == 'in':
						res_not.append(np)
#						print np
						continue
	for np in question_strings_np:
		if np not in res_not:
			result_list.append(np)
	return result_list

def omitiing_opostrophe_s(question_string_np):
	res_list = []
	for np in question_string_np:
		while '\'s' in np:
			index = np.find('\'s')
			np = np[:index] + np[index+2:]
		while '\' s' in np:
			index = np.find('\' s')
			np = np[:index] + np[index+3:]
		res_list.append(np)
	return res_list

def omit_dot_in_between(question_strings_np):
	res_list = []
	for np in question_strings_np:
		if '.' in np:
			dot_index = np.index('.')
			if ((np[dot_index-1] >= '0' and np[dot_index - 1] <= '9') and (np[dot_index + 1] >= '0' and np[dot_index + 1] <= '9')):
				print np
			if not ((np[dot_index-1] >= '0' and np[dot_index - 1] <= '9') and (np[dot_index + 1] >= '0' and np[dot_index + 1] <= '9')):
				parts = np.split('.')
				for part in parts:
					part = part.lstrip()
					part = part.rstrip()
					res_list.append(part)
		res_list.append(np)
	return res_list

def find_question_strings(file_index):
	question_st = []
	input_file = open("data/spilit_preprocessed/" + str(file_index) + '_lemma.txt','r')
	for line in input_file:
		if '?' in line:
			question_st.append(line.lower())
	return question_st

def omit_short_np(whole_question, question_strings_np):
	whole_question_parts = whole_question.split(' ')
	res = []
	for np in question_strings_np:
		print np
		np_parts = np.split(' ')
		if np_parts[0] not in whole_question_parts:
			if np not in res:
				res.append(np)
				continue
		ind = whole_question_parts.index(np_parts[0])
		while ind > -1:
			cur_str = ''
			checking_flag = True
			for ii in range(0, len(np_parts)):
				if ind + ii == len(whole_question_parts):
					if np not in res:
						res.append(np)
				else:
					if whole_question_parts[ind + ii] != np_parts[ii]:
						checking_flag = False
						break
					cur_str = cur_str + whole_question_parts[ind + ii] + ' '
			if checking_flag == False:
				if np_parts[0] in whole_question_parts[ind + 1:]:
					ind = whole_question_parts.index(np_parts[0], ind + 1)
				else:
					break
				continue

			if ind + len(np_parts) == len(whole_question_parts):
				if np not in res:
					res.append(np)
			else:
				print ind + len(np_parts)
				print len(whole_question_parts)
				cur_str = cur_str + whole_question_parts[ind + len(np_parts)]
			
			adding_flag = True
			for temp_np in question_strings_np:
				if cur_str in temp_np:
					adding_flag = False
			if adding_flag == True:
				if np not in res:
					res.append(np)
			if np_parts[0] in whole_question_parts[ind + 1:]:
				ind = whole_question_parts.index(np_parts[0], ind + 1)
			else:
				break
	return res

def omit_ban_np(question_strings_np):
	bad_word_list = ['together', 'triple', 'more', 'less', 'twice', 'some', 'only','any', 'many', 'number', 'total', 'time', 'much', 'amount', 'how', 'where', 'there', 'all', 'weighted', 'combined']
	res_list = []
	for np in question_strings_np:
		if np not in bad_word_list and np not in res_list:
			res_list.append(np)
	return res_list

word_list_not_in_beginning = ['many', 'much', 'cost', 'combined', 'remainder', 'other']
word_list_not_in_end = ['conbined', 'altogether', 'cost', 'total', 'selling']

if __name__ =="__main__":
	# question_strings_nps = ['0.75 dollar', 'dollar.dolar', '250 tivkry', '18.00 pins']
	# print omit_dot_in_between(question_strings_nps)
	question_strings = []
	names_list = read_names()
	for i in range(0, 400):
		print i
		
		question_strings_nps = []
		if i == 17 or i == 30 or i == 33 or i == 70 or i == 104 or i == 106 or i ==132 or i == 151 or i == 215 or i == 246 or i == 200 or i == 281 or i == 283 or i == 308 or i == 312 or  i == 335 or i == 375:
			continue
		question_strings = find_question_strings(i)
		input_file = open("data/np_pos_entity/" + str(i) + '.txt','r')
		for np in input_file:
			np = np.lstrip()
			if np == '':
				continue
			if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
				question_strings_nps.append(np[:-3].lower())
			else:
				question_strings_nps.append(np[:-1].lower())


		input_whole_question = open('data/problem_preprocessed/' + str(i) + '_lemma.txt', 'r')
		whole_question = input_whole_question.readline().lower()
		output_file = open("data/np_preprocessed_no_article_entity/" + str(i) + '.txt','w')
		res_article = refine_articles(question_strings_nps)
		res_no_opostrophe = omitiing_opostrophe_s(res_article)
		res_no_dot = omit_dot_in_between(res_no_opostrophe)
		res_q_string = omit_question_strings(res_no_dot)
		res_no_ban_word = res_q_string
		res_no_ban_word = omit_ban_np(res_no_ban_word)
		print res_no_ban_word
		for word in word_list_not_in_beginning:
			res_no_ban_word = omit_word_from_beginning(res_no_ban_word, word)
		
		for word in word_list_not_in_end:
			res_no_ban_word = omit_word_from_end(res_no_ban_word, word)

		# res_cost_omitted = omit_cost(res_q_string)
		res_no_names = omit_names(res_no_ban_word, names_list)
		print res_no_names
		res_no_math_modifier = omit_math_modifiers(res_no_names)
		res_no_modifier_in_end = omit_modifiers_from_the_end(res_no_math_modifier)
		# res_no_number_in_beginning = omit_number_beginning_expect_question(res_no_modifier_in_end)
		res_no_place = omit_places(res_no_modifier_in_end, "data/pos/" + str(i) + "_lemma.txt", i)
		res_added_implicit_head = add_implicit_heads(res_no_place)
		# res_no_short_np = omit_short_np(whole_question, res_no_place)
		res = omit_numbers(res_added_implicit_head)

		for res_np in res:
			output_file.write(res_np+'\n')
	
