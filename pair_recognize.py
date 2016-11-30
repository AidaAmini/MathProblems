from file_refrence import file_refrence
import sys

def rewrite_the_pairs():
	file_path_refrence = file_refrence()
	pair_file = open(file_path_refrence.all_pairs_path, 'r')
	score_file = open(file_path_refrence.score_file_name_relevant_pair, 'r')
	output_pair_file = open(file_path_refrence.relevant_pair_path, 'w')
	pair = pair_file.readline()
	for line in score_file:
		if pair.startswith('problem: '):
			output_pair_file.write(pair)
			pair = pair_file.readline()
		if line.startswith('1'):
			output_pair_file.write(pair)
		pair = pair_file.readline()

def write_all_pair_file(pair_file_name, start_index, end_index):
	file_path_refrence = file_refrence()
	for i in range(0, len(start_index)):
		sti = start_index[i]
		eni = end_index[i]
		pair_file = open(pair_file_name, 'w')
		np_list = []
		for index in range(sti, eni):
			if index == 17 or index == 30 or index == 33 or index == 70:
				continue
			np_file = open('data/entities_preprocessed/' + str(index) + '_lemma.ent')
			for np in np_file:
				if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
					np_list.append(np[:-3].lower())
				else:
					np_list.append(np[:-1].lower())

		for np1 in np_list:
			for np2 in np_list:
				if np1 == np2:
					continue
				pair_file.write(np1 + '\t' + np2 + '\n')



# write_all_pair_file(pair_file_name, [35], [50])
rewrite_the_pairs()






