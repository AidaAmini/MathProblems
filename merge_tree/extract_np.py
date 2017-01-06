import sys 
from file_refrence import file_refrence


start_index = int(sys.argv[1])
end_index = int(sys.argv[2])
file_path_refrence = file_refrence()
lemma_suffix = '_lemma.txt'
suffix = '.txt'
problematic_indexes = [17, 30, 33, 70, 104, 106, 132, 151, 215, 246, 200, 281, 283, 308, 312, 335, 375]
for i in range(start_index, end_index):
	if i in problematic_indexes:
		continue
	input_pos_file = open(file_path_refrence.pos_tagging_file_path + str(i) + lemma_suffix, 'r')
	output_file = open(file_path_refrence.np_pos_path[:-1] + '_entity/' + str(i) + suffix, 'w')
	words = []
	pos_tags = []
	#parsing input file 
	for line in input_pos_file:
		print line[:-1]
		line2 = line[:-1].lower().replace(' ', '').replace('?', '').replace('!', '')
		parts = line2.split('/')
		if parts[0].endswith('.'):
			parts[0] = parts[0][:-1]
		words.append(parts[0])
		pos_tags.append(parts[1])
		if '. ' in line or '? 'in line or '! ' in line:
			words.append('.')
			pos_tags.append('endOfSent')

	seen_list = []
	max_length_word = ''
	and_word = ''
	and_seen = False
	for j in range(0, len(pos_tags)):
		tag = pos_tags[j]
		print 'max_word is equal to ' + max_length_word
		if tag.startswith('nn') or tag.startswith('jj') or tag == 'pos' or tag == 'cd':
			print '1ss'
			if words[j] == 'many' or words[j] == 'much':
				continue
			elif max_length_word == '':
				max_length_word = words[j]
				if and_seen == True:
					and_word = and_word + ' ' + words[j]

 			elif words[j] == 'total':
				if max_length_word != '' and (max_length_word not in seen_list):
					seen_list.append(max_length_word)
					# seen_list.append(and_word)
					print max_length_word
					print and_word
					output_file.write(max_length_word + '\n')
					# output_file.write(and_word + '\n')
				if and_word != '' and (and_word not in seen_list):
					seen_list.append(and_word)
					output_file.write(and_word + '\n')
				max_length_word = ''
				and_seen = False
				and_word = ''
				continue

			elif tag == 'cd':
				if max_length_word != '' and (max_length_word not in seen_list):
					seen_list.append(max_length_word)
					output_file.write(max_length_word + '\n')
					print max_length_word
				if and_seen == True:
					and_word = and_word + ' ' + words[j]
				max_length_word = words[j]
			else:
				if and_seen == True:
					and_word = and_word + ' ' + words[j]
				max_length_word = max_length_word + ' ' + words[j]
		elif tag == 'in' :
			if words[j] ==  'of' and (pos_tags[j+1].startswith('nn') or pos_tags[j+1] == 'dt' or pos_tags[j+1].startswith('jj')):
				max_length_word = max_length_word + ' ' + words[j]
				if and_seen == True:
					and_word = and_word + ' ' + words[j]

		elif tag == 'dt':
			if (pos_tags[j + 1].startswith('nn') or pos_tags[j+1].startswith('jj')) and (j == 0 or pos_tags[j-1].startswith('in')):
				continue
			else:
				max_length_word = max_length_word + ' ' + words[j]
				if and_seen == True:
					and_word = and_word + ' ' + words[j]
		elif tag == 'cc':
			print 'aaaaaaaaaaaaaaaaaaaaannnnnnnnnnnnnnnnnnnnnnnnnnddddddddddddd' + words[j]
			if words[j] == 'and':
				print 'aaaaaaaaaaaaaaaaaaaaannnnnnnnnnnnnnnnnnnnnnnnnnddddddddddddd' + max_length_word
				output_file.write(max_length_word + '\n')
				print max_length_word
				and_seen = True
				and_word = max_length_word + ' and'
				max_length_word = ''
		else:
			if max_length_word != '' and (max_length_word not in seen_list):
				seen_list.append(max_length_word)
				print max_length_word
				print and_word
				output_file.write(max_length_word + '\n')
			if and_word != '' and (and_word not in seen_list):
				seen_list.append(and_word)
				output_file.write(and_word + '\n')
			max_length_word = ''
			and_seen = False
			and_word = ''
