import sys 
from file_refrence import file_refrence


start_index = int(sys.argv[1])
end_index = int(sys.argv[2])
file_path_refrence = file_refrence()
lemma_suffix = '_lemma.txt'
suffix = '.txt'
problematic_indexes = [17, 30, 33, 70, 104, 106, 132, 151, 215, 246, 200, 281, 283, 308, 312, 335, 375]
for i in range(start_index, end_index):
	# if i in problematic_indexes:
	# 	continue
	input_pos_file = open(file_path_refrence.pos_tagging_file_path + str(i) + lemma_suffix, 'r')
	output_file = open(file_path_refrence.np_pos_path[:-1] + '_entity/' + str(i) + suffix, 'w')
	words = []
	pos_tags = []
	#parsing input file 
	for line in input_pos_file:
		# print line[:-1]
		line2 = line[:-1].lower().replace(' ', '').replace('?', '').replace('!', '')
		# print line2
		parts = line2.split('/')
		if parts[0].endswith('.'):
			parts[0] = parts[0][:-1]
		print parts
		words.append(parts[0])
		pos_tags.append(parts[1])
		if '. ' in line or '? 'in line or '! ' in line:
			words.append('.')
			pos_tags.append('endOfSent')

	seen_list = []
	max_length_word = ''
	and_flag = False
	number_flag = False
	for j in range(0, len(pos_tags)):
		print j
		print words[j]
		print max_length_word
		tag = pos_tags[j]
		if (and_flag == True and number_flag == False) and (tag.startswith('nn') or tag.startswith('jj')):
			max_length_word = max_length_word + ' ' + words[j]
			print max_length_word
			continue
		else:
			if and_flag == True:
				if max_length_word != '' and (max_length_word not in seen_list):
					seen_list.append(max_length_word)
					# seen_list.append(and_word)
					print 'and_flag'
					print max_length_word
					output_file.write(max_length_word + '\n')
					# output_file.write(and_word + '\n')
				max_length_word = ''
				number_flag = False
				and_flag = False

		if tag.startswith('nn') or tag.startswith('jj') or tag == 'pos' or tag == 'cd':
			if words[j] == 'many' or words[j] == 'much' :
				continue
			# elif max_length_word == '':
			# 	max_length_word = words[j]

 			elif words[j] == 'total':
				if max_length_word != '' and (max_length_word not in seen_list):
					seen_list.append(max_length_word)
					# seen_list.append(and_word)
					print max_length_word
					output_file.write(max_length_word + '\n')
				number_flag = False
					# output_file.write(and_word + '\n')
				max_length_word = ''
				continue

			elif tag == 'cd':
				if max_length_word != '' and (max_length_word not in seen_list):
					seen_list.append(max_length_word)
					output_file.write(max_length_word + '\n')
				number_flag = True
				max_length_word = words[j]
			# elif tag.startswith('jj') and max_length_word == '':
			# 	max_length_word = words[j]
			# 	seen_nn = False
			# 	j = j + 1
			# 	while pos_tags[j].startswith('nn') or pos_tags[j].startswith('jj'):
			# 		if pos_tags[j].startswith('nn'):
			# 			seen_nn = True
			# 		max_length_word = max_length_word + ' ' + words[j]
			# 		j = j+1
			# 	j = j - 1
			# 	if seen_nn == True:
			# 		seen_list.append(max_length_word)
			# 		print max_length_word
			# 		output_file.write(max_length_word + '\n')
			# 	number_flag = False
			# 	max_length_word = ''
				
			else:
				if max_length_word != '':
					max_length_word = max_length_word + ' ' + words[j]
				else:
					max_length_word = words[j]

		elif tag == 'in' :
			print words[j]
			if max_length_word != '' and words[j] == 'of' and (pos_tags[j+1].startswith('nn') or pos_tags[j+1] == 'dt' or pos_tags[j+1].startswith('jj')):
				max_length_word = max_length_word + ' ' + words[j]
			else:
				if max_length_word != '' and (max_length_word not in seen_list):
					seen_list.append(max_length_word)
					print max_length_word
					output_file.write(max_length_word + '\n')
				number_flag = False
				max_length_word = ''

		# elif tag == 'dt':
		# 	if max_length_word != '' and (pos_tags[j + 1].startswith('nn') or pos_tags[j+1].startswith('jj')) and (j != 0) and pos_tags[j-1].startswith('in'):
		# 		continue
		elif tag == 'cc':
			if max_length_word != '' and j != 0 and words[j] == 'and' and pos_tags[j-1].startswith('nn') and (pos_tags[j+1].startswith('jj') or pos_tags[j+1].startswith('nn')):
				max_length_word = max_length_word + ' ' + words[j]
				and_flag = True

				# while(j < len(pos_tags) and (pos_tags[j+1].startswith('nn') or pos_tags[j+1].startswith('jj'))):
				# 	print 'j'
				# 	print j
				# 	max_length_word = max_length_word + ' ' + words[j]
				# 	print max_length_word
				# 	if j == len(pos_tags):
				# 		break
				# 	j = j+1
			else:
				if max_length_word != '' and (max_length_word not in seen_list):
					seen_list.append(max_length_word)
					output_file.write(max_length_word + '\n')
				number_flag = False
				max_length_word = ''
		else:
			if max_length_word != '' and (max_length_word not in seen_list):
				seen_list.append(max_length_word)
				output_file.write(max_length_word + '\n')
			number_flag = False
			max_length_word = ''




