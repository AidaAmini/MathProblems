import sys 
from file_refrence import file_refrence


start_index = int(sys.argv[1])
end_index = int(sys.argv[2])
file_path_refrence = file_refrence()
lemma_suffix = '_lemma.txt'
suffix = '.txt'
for i in range(start_index, end_index):
	input_pos_file = open(file_path_refrence.pos_tagging_file_path[:-1] + '2/' + str(i) + lemma_suffix, 'r')
	output_file = open(file_path_refrence.np_pos_path[:-1] + '_entity2/' + str(i) + suffix, 'w')
	words = []
	pos_tags = []
	#parsing input file 
	for line in input_pos_file:
		line2 = line[:-1].lower().replace(' ', '').replace('.', '').replace('?', '').replace('!', '')
		parts = line2.split('/')
		words.append(parts[0])
		pos_tags.append(parts[1])
		if '. ' in line or '? 'in line or '! ' in line:
			words.append('.')
			pos_tags.append('endOfSent')

	seen_list = []
	max_length_word = ''
	for j in range(0, len(pos_tags)):
		tag = pos_tags[j]
		if tag.startswith('nn') or tag.startswith('jj') or tag == 'pos' or tag == 'cd':
			if max_length_word == '':
				max_length_word = words[j]
			else:
				max_length_word = max_length_word + ' ' + words[j]
		else:
			if max_length_word != '' and (max_length_word not in seen_list):
				seen_list.append(max_length_word)
				output_file.write(max_length_word + '\n')
			max_length_word = ''
