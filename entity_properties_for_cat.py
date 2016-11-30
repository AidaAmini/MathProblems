class entity_properties_for_cat:
	list_of_cat = ['number', 'sim_eq', 'single_eq', 'base_rate', 'ratio', 'ex_knowledge']
	word_list = []
	word_list_per_cat = [[] for x in range(0, len(list_of_cat))]
	word_count_per_cat = [[] for x in range(0, len(list_of_cat))]
	problem_cat = []
	total_word_count_per_cat = [0 for x in range(0, len(list_of_cat))]
	start_index = 0
	end_index = 0

	def find_word_count_per_cat(self, dir, suffix):
		for i in range(self.start_index, self.end_index):
			input_file = open(dir+str(i) + suffix, 'r')
			problem = input_file.readline()
			words = problem.split(' ')
			for word in words:
				if word not in self.word_list:
					self.word_list.append(word)
				cat_index = self.problem_cat[i-self.start_index]
				self.total_word_count_per_cat[cat_index] = self.total_word_count_per_cat[cat_index] + 1
				if word in self.word_list_per_cat[cat_index]:
					self.word_count_per_cat[cat_index][self.word_list_per_cat[cat_index].index(word)] = self.word_count_per_cat[cat_index][self.word_list_per_cat[cat_index].index(word)]+1
				else:
					self.word_count_per_cat[cat_index].append(1)
					self.word_list_per_cat[cat_index].append(word)

	def read_problem_cat(self, dir, suffix):
		for i in range(self.start_index, self.end_index):
			cat_file = open(dir +str(i) + suffix, 'r')
			cat = cat_file.readline()
			cat = cat[:-1]
			cat_index = self.list_of_cat.index(cat)
			self.problem_cat.append(cat_index)

	def find_cat(self, problem_index):
		input_file = open('../../data/cat/' + str(problem_index) + '.cat', 'r')
		input_line = input_file.readline()
		input_line = input_line[:-1]
		return str(self.list_of_cat.index(input_line))


	def find_feature_string_for_problem(self, problem_index):
		input_file = open('../../data/problem_preprocessed/' + str(problem_index) + '_lemma.txt', 'r')
		prob = input_file.readline()
		words = prob.split(' ')
		out_string = self.find_cat(problem_index)
		out_string = out_string+ ' '
		word_problems_list = []
		out_word_list = []
		for word in words:
			for i in range(0, len(self.list_of_cat)):
				if word in self.word_list_per_cat[i]:
					if self.word_count_per_cat[i][self.word_list_per_cat[i].index(word)] > 20:
						if word in self.word_list:
							if word not in out_word_list:
								word_problems_list.append(self.word_list.index(word))
								out_word_list.append(word)

		for i in range(0, len(word_problems_list)):
			for j in range(0, len(word_problems_list)-1):
				if word_problems_list[j] >  word_problems_list[j+1]:
					tmp_ind = word_problems_list[j]
					word_problems_list[j] = word_problems_list[j+1]
					word_problems_list[j+1] = tmp_ind
					tmp_word = out_word_list[j]
					out_word_list[j] = out_word_list[j+1]
					out_word_list[j+1] = tmp_word
		list_seen = []
		for j in range(0, len(word_problems_list)):
			for i in range(0, len(self.list_of_cat)):		
				word = out_word_list[j]
				if word in self.word_list_per_cat[i]:
					print i
					out_string = out_string + str(i + len(self.list_of_cat) * word_problems_list[j]) +  ':' + str(self.word_count_per_cat[i][self.word_list_per_cat[i].index(word)] / (self.total_word_count_per_cat[i] + 0.001)) + ' '
		return out_string[:-1]

	def write_features(self):
		test_file = open('test_file.txt', 'w')
		train_file = open('train_file', 'w')
		self.start_index = 100
		self.end_index = 200
		self.read_problem_cat("../../data/cat/", '.cat')
		self.find_word_count_per_cat("../../data/problem_preprocessed/", '_lemma.txt')
		for i in range(100, 200):
			train_file.write(self.find_feature_string_for_problem(i) + '\n')
		for i in range(200, 300):
			test_file.write(self.find_feature_string_for_problem(i) + '\n')



ent_cat_prop = entity_properties_for_cat()
ent_cat_prop.write_features()


