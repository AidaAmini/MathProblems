from percenptron_data import percenptron_data
from file_refrence import file_refrence
from random import randint

class Merge_chain_alg:
	problem_data = percenptron_data()
	merge_weight_vector = []
	discard_weight_vector = []
	merge_th = 0.5
	discard_th = 0.8
	file_path_refrence = file_refrence()
	file_suffix = '.txt'
	file_lemma_suffix = '_lemma.txt'


	def __init__(self):
		self.problem_data = percenptron_data()


	def find_merge_feature_vector(self, chain1 , chain2):
		result = []

		print "chain1"
		print chain1
		print "chain2"
		print chain2
		print ''
		feature_list = []
		feature_names_list = []
		feature_list, feature_names_list = self.problem_data.calc_merge_count_feature(feature_list, feature_names_list, chain1, chain2)
		feature_list, feature_names_list = self.problem_data.calc_merge_unit_features(feature_list, feature_names_list, chain1, chain2)
		feature_list, feature_names_list = self.problem_data.calc_merge_max_cosigne(feature_list, feature_names_list, chain1, chain2)
		feature_list, feature_names_list = self.problem_data.calc_merge_ave_dist(feature_list, feature_names_list, chain1, chain2)
		feature_list, feature_names_list = self.problem_data.calc_merge_repeated_np(feature_list, feature_names_list, chain1, chain2)
		
		# result.append(self.problem_data.calc_merge_count_feature(chain1, chain2))
		# result.append(self.problem_data.calc_merge_unit_features(chain1, chain2))
		# result.append(self.problem_data.calc_merge_max_cosigne(chain1, chain2))
		# result.append(self.problem_data.calc_merge_ave_dist(chain1, chain2))
		# result.append(self.problem_data.calc_merge_count_feature(chain1, chain2))

		return (feature_list, feature_names_list)

	def read_data_by_problem_index(self, problem_index):
		self.problem_data.find_related_words_with_conjunction(self.file_path_refrence.stan_parse_file_path+str(problem_index)+ self.file_suffix)
		self.problem_data.read_noun_phrases(self.file_path_refrence.np_pos_path_entity + str(problem_index) + self.file_lemma_suffix)
		self.problem_data.read_subsets(self.file_path_refrence.gold_subset_pair_paths + str(problem_index) + self.file_lemma_suffix)
		self.problem_data.read_disjoints(self.file_path_refrence.gold_disjoint_pair_path + str(problem_index) + self.file_lemma_suffix)
		# self.question_prop.read_equvalence(self.file_path_refrence.gold_equivalence_pair_path + str(problem_index) + self.file_lemma_suffix)
		self.problem_data.find_gold_chains()
		self.problem_data.find_unchained_nps()
		self.problem_data.find_count_noun_stanford(self.file_path_refrence.stan_parse_file_path+str(problem_index)+ self.file_suffix)
		# self.problem_data.find_related_words_with_conjunction(self.file_path_refrence.stan_parse_file_path+str(problem_index)+ self.file_suffix)
		self.problem_data.read_whole_question(self.file_path_refrence.whole_question_path + str(problem_index) + self.file_lemma_suffix)
		print self.problem_data.gold_chain_list

	# def merge_chains(self, i, j):

	def dot_product(self, v1, v2):
		if len(v1) != len(v2):
			return -1
		sum = 0.0
		for i in range(0, len(v1)):
			sum = sum + v1[i] * v2[i]
		return sum

	def write_features_for_classification_train(self, start_index, end_index):
		output_file = open('train.txt', 'w')
		# self.problem_data.find_word_list(self.file_path_refrence.synonym_list_path, self.file_path_refrence.num_of_dimentions)

		for i in range(start_index, end_index):
			print "problem:::  " + str(i)
			self.problem_data.destruct()
			if i in self.file_path_refrence.problematic_indexes:
				continue
			self.read_data_by_problem_index(i)
			# print self.problem_data.gold_chain_list
			for chain in self.problem_data.gold_chain_list:
				print 'chaaaaaaaiiiiiiiiiiiiiiiinnnnnnnnnnnnnn'
				print chain
				for i in range(0, len(chain)):
					chain1 = []
					chain2 = []
					chain1.append(chain[i])
					for j in range(0, pow(2, len(chain)) - 1):
						chain2 = []
						str_bin_format = str(bin(j))[2:]
						for k in range(0, len(str_bin_format)):
							if str_bin_format[k] == '1' and k != i:
								chain2.append(chain[k])
						if chain1 != [] and chain2 != [] and chain1 != chain2:
							fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
							output_file.write('1')
							for p in range(0, len(fv_list)):
								output_file.write(' ' + str(p) + ':' + str(fv_list[p]))
							output_file.write('\n')

			for m in range(0, len(self.problem_data.gold_chain_list)):
				for np1 in self.problem_data.gold_chain_list[m]:
					chain1 = []
					chain2 = []
					chain1.append(np1)
					for n in range(m+1, len(self.problem_data.gold_chain_list)):
						chain2 = []
						for np2 in self.problem_data.gold_chain_list[n]:
							chain2.append(np2)
						if chain1 != [] and chain2 != [] and chain1 != chain2:
							fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
							output_file.write('0')
							for p in range(0, len(fv_list)):
								output_file.write(' ' + str(p) + ':' + str(fv_list[p]))
							output_file.write('\n')

					
					for n in range(0, len(self.problem_data.unchained_np_list)):
						chain2 = []
						chain2.append(self.problem_data.unchained_np_list[n])
					if chain1 != [] and chain2 != [] and chain1 != chain2:
						fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
						output_file.write('0')
						for p in range(0, len(fv_list)):
							output_file.write(' ' + str(p) + ':' + str(fv_list[p]))
						output_file.write('\n')

			for m in range(0, len(self.problem_data.gold_chain_list)):
				for np1 in self.problem_data.gold_chain_list[m]:
					chain1 = []
					chain2 = []
					chain1.append(np1)
					for n in range(0, len(self.problem_data.gold_chain_list)):
						num_of_random_samples = len(self.problem_data.gold_chain_list[n]) / 3 + 1
						if len(self.problem_data.gold_chain_list[n]) == 0:
							num_of_random_samples = 0
						random_samples = []
						while len(random_samples) != num_of_random_samples:
							random_number = randint(0, pow(2, len(self.problem_data.gold_chain_list[n])) - 1)
							if random_number not in random_samples:
								random_samples.append(str(bin(random_number))[2:])
						for rand_smpl in random_samples:
							chain2 = []
							for l in range(0, len(rand_smpl)):
								if rand_smpl[l] == '1':
									chain2.append(self.problem_data.gold_chain_list[n][l])
							if chain1 != [] and chain2 != [] and chain1 != chain2:
								fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
								output_file.write('0')
								for p in range(0, len(fv_list)):
									output_file.write(' ' + str(p) + ':' + str(fv_list[p]))
								output_file.write('\n')
					
					#unchained nps:
					num_of_random_samples = len(self.problem_data.unchained_np_list) / 3 + 1
					if len(self.problem_data.unchained_np_list) == 0:
						num_of_random_samples = 0
					random_samples = []
					while len(random_samples) != num_of_random_samples:
						random_number = randint(0, pow(2, len(self.problem_data.unchained_np_list)) - 1)
						if random_number not in random_samples:
							random_samples.append(str(bin(random_number))[2:])
					for rand_smpl in random_samples:
						chain2 = []
						for l in range(0, len(rand_smpl)):
							if rand_smpl[l] == '1':
								chain2.append(self.problem_data.unchained_np_list[l])
						if chain1 != [] and chain2 != [] and chain1 != chain2:
							fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
							output_file.write('0')
							for p in range(0, len(fv_list)):
								output_file.write(' ' + str(p) + ':' + str(fv_list[p]))
							output_file.write('\n')
			for np1 in self.problem_data.unchained_np_list:
				for np2 in self.problem_data.unchained_np_list:
					if np1 == np2: 
						continue
					chain1 = []
					chain2 = []
					chain1.append(np1)
					chain2.append(np2)
					if chain1 != [] and chain2 != [] and chain1 != chain2:
						fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
						output_file.write('0')
						for p in range(0, len(fv_list)):
							output_file.write(' ' + str(p) + ':' + str(fv_list[p]))
						output_file.write('\n')


	def train_procedure(self, problem_index):
		num_of_iters = 0
		self.read_data(problem_index)
		while len(self.problem_data.driven_chains) > 2 and num_of_iters < 10:
			for i in range (0, len(self.problem_data.driven_chains)):
				for j in range (i + 1, len(self.problem_data.driven_chains)):
					merge_features = self.find_merge_feature_vector()
					score = self.dot_product(merge_features, self.merge_weight_vector)
					if score >= self.merge_th:
						self.merge_chains(i, j)
			num_of_iters = num_of_iters + 1



# from Merge_chain_alg import Merge_chain_alg
Merge_chain = Merge_chain_alg()
Merge_chain.write_features_for_classification_train(0, 300)
# Merge_chain.read_data_by_problem_index(0)














