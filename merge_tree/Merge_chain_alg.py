from percenptron_data import percenptron_data
from file_refrence import file_refrence
from random import randint
from scikit_test import scikit_module

class Merge_chain_alg:
	train_problem_data = percenptron_data()
	test_problem_data = percenptron_data()
	merge_weight_vector = []
	discard_weight_vector = []
	merge_th = 0.5
	discard_th = 0.8
	file_path_refrence = file_refrence()
	file_suffix = '.txt'
	file_lemma_suffix = '_lemma.txt'
	feature_names_list = []
	scikit_train_module = scikit_module(10)
	neg_th = 0.8
	pos_th = 0.6
	log_file = open("run_log.txt",'w')

	def __init__(self):
		self.train_problem_data = percenptron_data()
		self.test_problem_data = percenptron_data()
		self.scikit_train_module = scikit_module(10)
		self.train_problem_data.find_word_list(self.file_path_refrence.synonym_list_path, self.file_path_refrence.num_of_dimentions)
		self.test_problem_data.word_vector = self.train_problem_data.word_vector
		self.test_problem_data.word_list = self.test_problem_data.word_list

	def find_merge_feature_vector(self, chain1 , chain2):
		result = []

		# #print "chain1"
		# #print chain1
		# #print "chain2"
		# #print chain2
		# #print ''
		feature_list = []
		feature_names_list = []
		feature_list, feature_names_list = self.train_problem_data.calc_merge_count_feature(feature_list, feature_names_list, chain1, chain2)
		feature_list, feature_names_list = self.train_problem_data.calc_merge_unit_features(feature_list, feature_names_list, chain1, chain2)
		feature_list, feature_names_list = self.train_problem_data.calc_merge_max_cosigne(feature_list, feature_names_list, chain1, chain2)
		feature_list, feature_names_list = self.train_problem_data.calc_merge_ave_dist(feature_list, feature_names_list, chain1, chain2)
		feature_list, feature_names_list = self.train_problem_data.calc_merge_repeated_np(feature_list, feature_names_list, chain1, chain2)
		
		# result.append(self.train_problem_data.calc_merge_count_feature(chain1, chain2))
		# result.append(self.train_problem_data.calc_merge_unit_features(chain1, chain2))
		# result.append(self.train_problem_data.calc_merge_max_cosigne(chain1, chain2))
		# result.append(self.train_problem_data.calc_merge_ave_dist(chain1, chain2))
		# result.append(self.train_problem_data.calc_merge_count_feature(chain1, chain2))

		return (feature_list, feature_names_list)

	def read_data_by_problem_index(self, problem_index, percenptron_data_structure):
		percenptron_data_structure.find_related_words_with_conjunction(self.file_path_refrence.stan_parse_file_path+str(problem_index)+ self.file_suffix)
		percenptron_data_structure.read_noun_phrases(self.file_path_refrence.np_pos_path_entity + str(problem_index) + self.file_lemma_suffix)
		percenptron_data_structure.read_question_strings(self.file_path_refrence.question_strings_path + str(problem_index) + self.file_lemma_suffix)
		percenptron_data_structure.read_subsets(self.file_path_refrence.gold_subset_pair_paths + str(problem_index) + self.file_lemma_suffix)
		percenptron_data_structure.read_disjoints(self.file_path_refrence.gold_disjoint_pair_path + str(problem_index) + self.file_lemma_suffix)
		# self.question_prop.read_equvalence(self.file_path_refrence.gold_equivalence_pair_path + str(problem_index) + self.file_lemma_suffix)
		percenptron_data_structure.find_gold_chains()
		percenptron_data_structure.find_unchained_nps()
		percenptron_data_structure.find_count_noun_stanford(self.file_path_refrence.stan_parse_file_path+str(problem_index)+ self.file_suffix)
		# self.train_problem_data.find_related_words_with_conjunction(self.file_path_refrence.stan_parse_file_path+str(problem_index)+ self.file_suffix)
		percenptron_data_structure.read_whole_question(self.file_path_refrence.whole_question_path + str(problem_index) + self.file_lemma_suffix)
		percenptron_data_structure.find_repeated_noun_phrases()
		percenptron_data_structure.find_noun_phrases_in_question(self.file_path_refrence.pos_tagging_file_path + str(problem_index) + self.file_lemma_suffix)
		
	# def do_the_inferences(self, problem_index, percenptron_data_structure):

	# def merge_chains(self, i, j):

	def dot_product(self, v1, v2):
		if len(v1) != len(v2):
			return -1
		sum = 0.0
		for i in range(0, len(v1)):
			sum = sum + v1[i] * v2[i]
		return sum

	def write_features_for_classification_train(self, start_index, end_index, additional_train_pair, additional_train_pair_indexes):
		x_train = []
		y_train = []
		train_chain_pairs = []
		train_chain_pair_prob_index = []
		output_file = open('train.txt', 'w')
		for i in range(start_index, end_index):
			addidional_pairs_for_prob_index = []
			for k in range(0, len(additional_train_pair_indexes)):
				if additional_train_pair_indexes[k] == i:
					addidional_pairs_for_prob_index.append(additional_train_pair[k])
			self.train_problem_data.destruct()
			if i in self.file_path_refrence.problematic_indexes:
				continue
			self.read_data_by_problem_index(i, self.train_problem_data)
			for i in range(0 , len(addidional_pairs_for_prob_index), 2):
				chain1 = addidional_pairs_for_prob_index[i]
				chain2 = addidional_pairs_for_prob_index[i+ 1]
				fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
				train_chain_pairs.append(chain1)
				train_chain_pairs.append(chain2)
				train_chain_pair_prob_index.append(i)
				train_chain_pair_prob_index.append(i)
				x_train.append(fv_list)
				label = self.find_label(self.train_problem_data, chain1, chain2)
				y_train.append(label)
				output_file.write(str(label))
				for p in range(0, len(fv_list)):
					output_file.write(' ' + str(p) + ':' + str(fv_list[p]))
				output_file.write('\n')
			for chain in self.train_problem_data.gold_chain_list:
				for m in range(0, len(chain)):
					chain1 = []
					chain2 = []
					chain1.append(chain[m])
					for j in range(0, pow(2, len(chain)) - 1):
						chain2 = []
						str_bin_format = str(bin(j))[2:]
						for k in range(0, len(str_bin_format)):
							if str_bin_format[k] == '1' and k != i:
								chain2.append(chain[k])
						if chain1 != [] and chain2 != [] and chain1 != chain2:
							fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
							train_chain_pairs.append(chain1)
							train_chain_pairs.append(chain2)
							train_chain_pair_prob_index.append(i)
							train_chain_pair_prob_index.append(i)
							x_train.append(fv_list)
							y_train.append(1)
							output_file.write('1')
							for p in range(0, len(fv_list)):
								output_file.write(' ' + str(p) + ':' + str(fv_list[p]))
							output_file.write('\n')

			for m in range(0, len(self.train_problem_data.gold_chain_list)):
				for np1 in self.train_problem_data.gold_chain_list[m]:
					chain1 = []
					chain2 = []
					chain1.append(np1)
					for n in range(m+1, len(self.train_problem_data.gold_chain_list)):
						chain2 = []
						for np2 in self.train_problem_data.gold_chain_list[n]:
							chain2.append(np2)
						if chain1 != [] and chain2 != [] and chain1 != chain2:
							fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
							train_chain_pairs.append(chain1)
							train_chain_pairs.append(chain2)
							train_chain_pair_prob_index.append(i)
							train_chain_pair_prob_index.append(i)
							x_train.append(fv_list)
							y_train.append(0)
							output_file.write('0')
							for p in range(0, len(fv_list)):
								output_file.write(' ' + str(p) + ':' + str(fv_list[p]))
							output_file.write('\n')

					
					for n in range(0, len(self.train_problem_data.unchained_np_list)):
						chain2 = []
						chain2.append(self.train_problem_data.unchained_np_list[n])
					if chain1 != [] and chain2 != [] and chain1 != chain2:
						fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
						self.feature_names_list = fv_name_list
						train_chain_pairs.append(chain1)
						train_chain_pairs.append(chain2)
						train_chain_pair_prob_index.append(i)
						train_chain_pair_prob_index.append(i)
						x_train.append(fv_list)
						y_train.append(0)
						output_file.write('0')
						for p in range(0, len(fv_list)):
							output_file.write(' ' + str(p) + ':' + str(fv_list[p]))
						output_file.write('\n')

			for m in range(0, len(self.train_problem_data.gold_chain_list)):
				for np1 in self.train_problem_data.gold_chain_list[m]:
					chain1 = []
					chain2 = []
					chain1.append(np1)
					for n in range(0, len(self.train_problem_data.gold_chain_list)):
						num_of_random_samples = len(self.train_problem_data.gold_chain_list[n]) / 3 + 1
						if len(self.train_problem_data.gold_chain_list[n]) == 0:
							num_of_random_samples = 0
						random_samples = []
						while len(random_samples) != num_of_random_samples:
							random_number = randint(0, pow(2, len(self.train_problem_data.gold_chain_list[n])) - 1)
							if random_number not in random_samples:
								random_samples.append(str(bin(random_number))[2:])
						for rand_smpl in random_samples:
							chain2 = []
							for l in range(0, len(rand_smpl)):
								if rand_smpl[l] == '1':
									chain2.append(self.train_problem_data.gold_chain_list[n][l])
							if chain1 != [] and chain2 != [] and chain1 != chain2:
								fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
								train_chain_pairs.append(chain1)
								train_chain_pairs.append(chain2)
								train_chain_pair_prob_index.append(i)
								train_chain_pair_prob_index.append(i)
								x_train.append(fv_list)
								y_train.append(0)
								output_file.write('0')
								for p in range(0, len(fv_list)):
									output_file.write(' ' + str(p) + ':' + str(fv_list[p]))
								output_file.write('\n')
					
					#unchained nps:
					num_of_random_samples = len(self.train_problem_data.unchained_np_list) / 3 + 1
					if len(self.train_problem_data.unchained_np_list) == 0:
						num_of_random_samples = 0
					random_samples = []
					while len(random_samples) != num_of_random_samples:
						random_number = randint(0, pow(2, len(self.train_problem_data.unchained_np_list)) - 1)
						if random_number not in random_samples:
							random_samples.append(str(bin(random_number))[2:])
					for rand_smpl in random_samples:
						chain2 = []
						for l in range(0, len(rand_smpl)):
							if rand_smpl[l] == '1':
								chain2.append(self.train_problem_data.unchained_np_list[l])
						if chain1 != [] and chain2 != [] and chain1 != chain2:
							fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
							train_chain_pairs.append(chain1)
							train_chain_pairs.append(chain2)
							train_chain_pair_prob_index.append(i)
							train_chain_pair_prob_index.append(i)
							x_train.append(fv_list)
							y_train.append(0)
							output_file.write('0')
							for p in range(0, len(fv_list)):
								output_file.write(' ' + str(p) + ':' + str(fv_list[p]))
							output_file.write('\n')
			for np1 in self.train_problem_data.unchained_np_list:
				for np2 in self.train_problem_data.unchained_np_list:
					if np1 == np2: 
						continue
					chain1 = []
					chain2 = []
					chain1.append(np1)
					chain2.append(np2)
					if chain1 != [] and chain2 != [] and chain1 != chain2:
						fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
						train_chain_pairs.append(chain1)
						train_chain_pairs.append(chain2)
						train_chain_pair_prob_index.append(i)
						train_chain_pair_prob_index.append(i)
						x_train.append(fv_list)
						y_train.append(0)
						output_file.write('0')
						for p in range(0, len(fv_list)):
							output_file.write(' ' + str(p) + ':' + str(fv_list[p]))
						output_file.write('\n')
		for j in range(0, len(self.feature_names_list)):
			self.log_file.write(str(j) + '  ' + self.feature_names_list[j] + '\n')	
		for l in range(0, len(y_train)):
			self.log_file.write(str(y_train[l]) + ' ')
		self.log_file.write(' end \n')		
		return (x_train, y_train, train_chain_pairs, train_chain_pair_prob_index)

	def train_procedure(self, problem_index):
		num_of_iters = 0
		self.read_data(problem_index)
		while len(self.train_problem_data.driven_chains) > 2 and num_of_iters < 10:
			for i in range (0, len(self.train_problem_data.driven_chains)):
				for j in range (i + 1, len(self.train_problem_data.driven_chains)):
					merge_features = self.find_merge_feature_vector()
					score = self.dot_product(merge_features, self.merge_weight_vector)
					if score >= self.merge_th:
						self.merge_chains(i, j)
			num_of_iters = num_of_iters + 1

	def find_label(self, problem_data, chain1, chain2):
		merged_chain = []
		for np1 in chain1:
			merged_chain.append(np1)
		for np2 in chain2:
			merged_chain.append(np2)
		for chain in problem_data.gold_chain_list:
			flag = True
			for element_in_chain in merged_chain:
				if element_in_chain not in chain:
					flag = False
					break
			if flag == True:
				return 1
		return 0

	def choose_hard_pos_neg(self, y_classified, y_test, y_probs, chain_pair_list):
		additional_train_pair = []
		for i in range(0, len(y_test)):
			if y_test[i] == 1 and y_classified[i] == 0:
				if y_probs[i][0] > self.pos_th:
					additional_train_pair.append(chain_pair_list[2*i])
					additional_train_pair.append(chain_pair_list[2*i + 1])
			if y_test[i] == 0 and y_classified[i] == 1:
				if y_probs[i][1] > self.neg_th:
					additional_train_pair.append(chain_pair_list[2*i])
					additional_train_pair.append(chain_pair_list[2*i + 1])
		return additional_train_pair

	def merge_two_chains(self, problem_data, chain1, chain2):
		if len(chain1) == 1:
			if chain1[0] in problem_data.driven_unchained_np_list:
				problem_data.driven_unchained_np_list.remove(chain1[0])
		if len(chain2) == 1:
			if chain2[0] in problem_data.driven_unchained_np_list:
				problem_data.driven_unchained_np_list.remove(chain2[0])
		if len(chain1) == 1 and len(chain2) == 1:
			new_chain = []
			new_chain.append(chain1[0])
			new_chain.append(chain2[0])
			problem_data.driven_chains.append(new_chain)
		elif len(chain1) != 1:
			chain1_index = problem_data.driven_chains.index(chain1)
			for i in range(0, len(chain2)):
				problem_data.driven_chains[chain1_index].append(chain2[i])
			if len(chain2) > 1:
				chain2_index = problem_data.driven_chains.index(chain2)
				problem_data.driven_chains.remove(chain2)
		else:  # len(chain 1 == 1 and len chain2 > 1)
			chain2_index = problem_data.driven_chains.index(chain2)
			problem_data.driven_chains[chain2_index].append(chain1[0])

	def update_stats(self, y_test,y_classified ,tp, fp, tn, fn):
		print y_test
		print y_classified
		for i in range(0, len(y_test)):
			if y_test[i] == 0:
				if y_classified[i] == 0:
					tn = tn + 1
				else:
					fp = fp + 1
			else:
				if y_classified[i] == 1:
					tp = tp + 1
				else:
					fn = fn + 1
		return (tp, fp, tn, fn)

	def update_status_calc_measurements(self, problem_data, chain_pair_list, y_test, y_classified, y_probs, tp, fp, tn, fn):
		additional_pairs = []
		num_of_changes = 0
		no_change_needed = True
		for i in range(0, len(y_test)):
			if y_test[i] == 1:
				no_change_needed = False
				break
		if no_change_needed == True:
			return (tp, fp, tn, fn, num_of_changes, [])
		# no_change_detected = True
		# for i in range(0, len(y_classified)):
		# 	if y_classified[i] == 1:
		# 		no_change_detected = False
		# 		break
		# if no_change_needed == True:
		merge_probs = []
		seen_max = []
		for l in range(0, len(y_probs)):
			seen_max.append(False)
		for l in range(0, len(y_probs)):
			merge_probs.append(y_probs[l][1])
		max_index = merge_probs.index(max(merge_probs))
		while(y_test[max_index] != 1):
			#print 'while'
			#print max_index
			additional_pairs.append(chain_pair_list[2*max_index])
			additional_pairs.append(chain_pair_list[2*max_index + 1])
			seen_max[max_index] = True
			max_index = -1
			max_prob = 0.0
			#print merge_probs
			for l in range(0, len(merge_probs)):
				if merge_probs[l] > max_prob:
					if seen_max[l] != True:
						max_index = l
						max_prob = merge_probs[l]
			if max_index == -1:
				break
		if max_index == -1:
			return (tp, fp, tn, fn, num_of_changes, [])
		if y_classified[max_index] != 1:
			additional_pairs.append(chain_pair_list[2*max_index])
			additional_pairs.append(chain_pair_list[2*max_index + 1])
		self.merge_two_chains(problem_data, chain_pair_list[2*max_index], chain_pair_list[2*max_index +1])
		num_of_changes = num_of_changes + 1
		# else:
		# 	for i in range(0, len(y_classified)):
		# 		if y_classified[i] == 1:
		# 			self.merge_two_chains(problem_data, chain_pair_list[2*i], chain_pair_list[2*i +1])
		# 			num_of_changes = num_of_changes + 1
		tp, fp, tn, fn = self.update_stats(y_test,y_classified ,tp, fp, tn, fn)
		return (tp, fp, tn, fn, num_of_changes, additional_pairs)

	def test_procedure_for_one_problem(self, problem_index, tp, tn, fp, fn):
		self.test_problem_data.destruct()
		if problem_index in self.file_path_refrence.problematic_indexes:
			return (tp, fp, tn, fn, [])
		self.read_data_by_problem_index(problem_index, self.test_problem_data)
		#print "aaaaaaaaaaaa"
		# #print 'akjhakhskajdlaksldkajlksjdaklhsfkjabvjb,alknlcamlkamnflajl'
		# #print self.test_problem_data.noun_phrase_list
		# #print self.test_problem_data.driven_unchained_np_list
		num_of_changes = -1
		while num_of_changes != 0:
			#print "num_of_changes"
			#print num_of_changes
			#print self.test_problem_data.driven_chains
			#print self.test_problem_data.driven_unchained_np_list
			num_of_changes = 0
			y_test = []
			x_test = []
			chain_pair_list = []
			for chain1 in self.test_problem_data.driven_chains:
				for chain2 in self.test_problem_data.driven_chains:
					if chain1 != [] and chain2 != [] and chain1 != chain2:
						fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
						x_test.append(fv_list)
						chain_pair_list.append(chain1)
						chain_pair_list.append(chain2)
						y_test.append(self.find_label(self.test_problem_data ,chain1 , chain2))
			#print "aaaaaaaaaaaaa1111"
			for l in range(0, len(y_test)):
				self.log_file.write(str(y_test[l]) + ' ')
			self.log_file.write(' end \n')
			#print "aaaaaaaaaaaaa2222"
			
			for chain1 in self.test_problem_data.driven_chains:
				for np in self.test_problem_data.driven_unchained_np_list:
					chain2 = []
					chain2.append(np)
					if chain1 != [] and chain2 != [] and chain1 != chain2:
						fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
						x_test.append(fv_list)
						chain_pair_list.append(chain1)
						chain_pair_list.append(chain2)
						y_test.append(self.find_label(self.test_problem_data ,chain1 , chain2))
			#print "aaaaaaaaaaaaa3333"

			for np1 in self.test_problem_data.driven_unchained_np_list:
				for np2 in self.test_problem_data.driven_unchained_np_list:
					chain1 = []
					chain1.append(np1)
					chain2 = []
					chain2.append(np2)
					if chain1 != [] and chain2 != [] and chain1 != chain2:
						fv_list, fv_name_list = self.find_merge_feature_vector(chain1, chain2)
						x_test.append(fv_list)
						chain_pair_list.append(chain1)
						chain_pair_list.append(chain2)
						y_test.append(self.find_label(self.test_problem_data ,chain1 , chain2))
			#print "aaaaaaaaaaaaa44444"
			y_classified, y_probs = self.scikit_train_module.random_forest_predict_by_prob(x_test)
			#print "aaaaaaaaaaaaa5555"
			# additional_train_pair = self.choose_hard_pos_neg(y_classified, y_test, y_probs, chain_pair_list)     
			#print "aaaaaaaaaaaaa6666"
			tp, fp, tn, fn, num_of_changes, additional_train_pair = self.update_status_calc_measurements(self.test_problem_data, chain_pair_list, y_test, y_classified, y_probs, tp, fp, tn, fn)
			#print "aaaaaaaaaaaaa777777"
			
		return (tp, fp, tn, fn, additional_train_pair)

	def report_measurements(self, tp, tn, fp, fn, iteration_num):
		recall = (tp + 0.0)/(tp+fn)
		percision = (tp + 0.0)/(tp+fp)
		f1_score = 2* (((percision * recall)+ 0.0)/(recall + percision))
		print "Recal for iteration number " + str(iteration_num) + " is: " + str(recall)
		print "precision for iteration number " + str(iteration_num) + " is: " + str(percision)
		print "F1 Score for iteration number " + str(iteration_num) + " is: " + str(f1_score)


	def iterative_train_procedure(self):
		additional_train_pair = []
		additional_train_pair_indexes = []
		for i in range(0, 10):
			print i
			self.log_file.write('iteration number ' + str(i) + '\n')
			tp = 0
			fp = 0
			tn = 0
			fn = 0
			start_index_train = 0
			end_index_train = 0
			start_index_test = 0
			end_index_test = 0
			if i%2 == 0:
				start_index_train = 0
				end_index_train = 200
				start_index_test = 200
				end_index_test = 400
			else:
				start_index_train = 200
				end_index_train = 400
				start_index_test = 0
				end_index_test = 200

			self.scikit_train_module = scikit_module(100)
			print 'step1'
			x_train, y_train, pair_list_train, prob_indexes_train = self.write_features_for_classification_train(start_index_train, end_index_train, additional_train_pair, additional_train_pair_indexes)
			print 'step2'
			self.scikit_train_module.random_forest_train(x_train, y_train)
			print 'step3'
			for k in range(start_index_test, end_index_test):
				#print 'k' + str(k)
				tp, fp, tn, fn, adding_pairs = self.test_procedure_for_one_problem(k, tp, fp, tn, fn)
				#print "11111"
				self.log_file.write("After Test procedure" + str(k) + '\n')
				self.log_file.write("tp" + str(tp) + '\n')
				self.log_file.write("fp" + str(fp) + '\n')
				self.log_file.write("tn" + str(tn) + '\n')
				self.log_file.write("fn" + str(fn) + '\n')
				for pair in adding_pairs:
					#print "22222"
					additional_train_pair.append(pair)
					additional_train_pair_indexes.append(k)

			self.report_measurements(tp, tn, fp, fn, i)



			# x_test, y_test, pair_list_test, prob_indexes_test = self.write_features_for_classification_test(start_index_test, end_index_test)
			# y_classified, y_probs = self.scikit_train_module.random_forest_predict_by_prob(x_test)
			# additional_train_pair, additional_train_pair_indexes = choose_hard_pos_neg(y_classified, y_test, y_probs, pair_list_test, prob_indexes_test)

# from Merge_chain_alg import Merge_chain_alg
Merge_chain = Merge_chain_alg()
Merge_chain.iterative_train_procedure()
# Merge_chain.read_data_by_problem_index(0)














