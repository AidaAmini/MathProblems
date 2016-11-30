class log_linear_np_relevant:
	labels = [] # list of labels in sequential order
	data = [] # list of np to be considered in seqeuential order
	feature_vectors = [[]]
	vocab_list = []
	vocab_dict = {}
	true_count_dict = {}
	train_start_index = 50
	train_end_index = 90
	test_start_index = 0
	test_end_index = 50
	steo_size = 0.2
	lamb = 0.4

	def read_data(self, file_name):
		input_file = open(file_name, 'r')
		for line in input_file:
			fv = []
			label = line[:1]
			feature_vector = line[2:-1]
			if line.startswith('-'):
				label = line[:2]
				feature_vector = line[3:-1]
			features = feature_vector.split(' ')
			for feature in features:
				parts = feature.split(':')
				fv.append(float(parts[1]))
			self.labels.append(label)
			self.feature_vectors.append(fv)

	# def fill_in_data(self, start_index, end_index):
	# 	for i in range(start_index, end_index):
	# 		input_file = open("../../data/np_no_article/" + str(file_index) + '_lemma.txt.ssplit.ccg.nps', 'r')
	# 		for line in input_file:
	# 			if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
	# 				self.data.append(np[:-3].lower())
	# 			else:
	# 				self.data.append(np[:-1].lower())


	def finding_counts(self, file_index):
		noun_phrase_file = open("../../data/np_no_article/" + str(file_index) + '_lemma.txt.ssplit.ccg.nps', 'r')
		for np in noun_phrase_file:
			noun_phrase = ''
			if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
				noun_phrase = np[:-3].lower()
			else:
				noun_phrase = np[:-1].lower()
			self.vocab_list.append(noun_phrase)
			if noun_phrase in self.vocab_dict:
				self.vocab_dict[noun_phrase] = self.vocab_dict[noun_phrase] + 1
			else:
				self.vocab_dict[noun_phrase] = 1
		ans_noun_phrase_file = opne("../../data/ans/" + str(file_index) + "_lemma.ans", 'r')
		for np in ans_noun_phrase_file:
			noun_phrase = ''
			if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
				noun_phrase = np[:-3].lower()
			else:
				noun_phrase = np[:-1].lower()
			if noun_phrase in self.true_count_dict:
				self.true_count_dict[noun_phrase] = self.true_count_dict[noun_phrase] + 1
			else:
				self.true_count_dict[noun_phrase] = 1

	def initialize_weights(self):
	    self.wieghts = np.zeros(len(ngram_dict))

	def find_the_gradient(self, j):
		part1_sum = 0.0
		part2_sum = 0.0
		for i in range(0, len(self.feature_vector[j])):
			part1_sum = part1_sum + self.feature_vector[j][i]
		for i in range(0, len(self.feature_vector[j])):
			noun_phrase = self.vocab_list[i]
			if self.label[i] == 1:
				part2_sum = part2_sum + self.feature_vector[j][i] * (self.true_count_dict[noun_phrase] / (self.vocab_dict[noun_phrase] + 0.0))
			else:
				part2_sum = part2_sum + self.feature_vector[j][i] * ((self.vocab_dict[noun_phrase]  - (self.true_count_dict[noun_phrase])) / (self.vocab_dict[noun_phrase] + 0.0))

		return part1_sum - part2_sum

	def move_with_gradient(self):
		self.initialize_weights()
		for i in range(0, 10):
			for j in range(0, len(self.feature_vector)):
				self.wieghts[j] = self.wieghts[j] - self.steo_size * find_the_gradient(j)
			self.wieghts = self.wieghts - self.lamb * linalg.norm(self.wieghts.T, 1)
		output_file = open("weights.txt", 'w')
		for weight in self.weights:
			output_file.write(self.weights[i])


	def initialize(self, train_test_mode):
		start_index = 0
		end_index = 0
		if train_test_mode == 'train':
			start_index = self.train_start_index
			end_index = self.train_end_index
		elif train_test_mode == 'test':
			start_index = self.test_start_index
			end_index = self.test_end_index
		# self.fill_in_data(start_index, end_index)
		self.vocab_dict = {}
		self.true_count_dict = {}
		for i in range(start_index, end_index):
			finding_counts(i) 


if __name__ == "__main__":
	from log_linear_np_relevant import log_linear_np_relevant
	log_linear = log_linear_np_relevant()
	log_linear.initialize('train')
	log_linear.move_with_gradient()
