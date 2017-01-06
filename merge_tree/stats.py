from file_refrence import file_refrence

class stat_claculator:
	file_path_refrence = file_refrence()
	start_index = 0
	end_index = 0
	file_suffix = '.txt'
	file_lemma_suffix = '_lemma.txt'

	def __init__(self, start_index, end_index):
		self.file_path_refrence = file_refrence()
		self.start_index = start_index
		self.end_index = end_index

	def find_the_num_of_disagreement_of_np_and_chain_annotations(self):
		for i in range(self.start_index, self.end_index):
			if i in self.file_path_refrence.problematic_indexes:
				continue
			print 'considering problem ' + str(i)
			np_list = []
			chain_vocab = []
			chain_input_file = open(self.file_path_refrence.gold_chian_path + str(i) + self.file_lemma_suffix)
			for line in chain_input_file:
				if '	' in line:
					parts = line[:-1].split('	')
					for part in parts:
						if part not in chain_vocab:
							chain_vocab.append(part)
			np_input_file = open(self.file_path_refrence.question_string_nps_relevant_np_entity_path + str(i) + self.file_lemma_suffix)
			for np in np_input_file:
				if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
					np = np[:-3]
				else:
					np = np[:-1]
				if np not in  np_list:
					np_list.append(np)
			count = 0
			for chain_np in chain_vocab:
				if chain_np not in np_list:
					count = count + 1
					print chain_np + 'is not extracted'
			print 'for this problem ' + str(count) + " nps are not found"





stat_clac = stat_claculator(0, 400)
stat_clac.find_the_num_of_disagreement_of_np_and_chain_annotations()
























			