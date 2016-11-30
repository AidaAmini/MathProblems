from basic_feature_finder_revised import basic_feature_finder_revised
from useful_np_feature_finder import useful_np_feature_finder
from entity_properties import entity_properties
from disjoint_feature_finder import disjoint_feature_finder
from subset_feature_finder_revised import subset_feature_finder_revised
from equivalence_feature_finder import equivalence_feature_finder
from logLinear_Feature_finder import logLinear_Feature_finder
from class_finder import class_finder
from math_modifiers import math_modifiers
from file_refrence import file_refrence
import sys

class FeatureFinder_LogLinear_learner :
	data_start_index = 0
	data_end_index = 1
	feature_file_path = ""
	question_prop = entity_properties()
	non_relevant_string = ["problem: "]
	file_path_refrence = file_refrence()
	file_lemma_suffix = '_lemma.txt'
	file_lemma_suffix_story = 'story_lemma.txt'
	file_suffix = '.txt'
	binary_multiclass_mode = 0 # 0 for binary and 1 for multiclass
	test_train_mode = 0 #0 for train and 1 for test
	entity_type_mode = 1

	def __init__(self, test_train_mode, binary_multiclass_mode , entity_type_mode, data_end_index, data_start_index = 0, feature_file_path = "train_fv.txt"):
		self.data_start_index = data_start_index
		self.data_end_index = data_end_index
		self.feature_file_path = feature_file_path
		self.question_prop = entity_properties()
		self.entity_type_mode = entity_type_mode
		self.binary_multiclass_mode = binary_multiclass_mode
		self.test_train_mode = test_train_mode

	def write_features(self):
		output_file = open(self.feature_file_path, 'w')
		self.question_prop = entity_properties()
		self.question_prop.find_word_list(self.file_path_refrence.synonym_list_path, self.file_path_refrence.num_of_dimentions)
		
		for i in range(self.data_start_index, self.data_end_index):
			print "i is:"
			print  i
			if i in self.file_path_refrence.problematic_indexes:
				continue

			self.read_data(i)
			# for pair in self.question_prop.relevant_pairs:
			# 	parts = pair.split('\t')
			# 	np1 = parts[0]
			# 	np2 = parts[1]
			for np1 in self.question_prop.question_strings_np:
				for np2 in self.question_prop.question_strings_np:
					if np1 == np2:
						continue
					# print np1 + ' ' + np2
					if np1.endswith(np2):
						if math_modifiers.is_word_number(np1[:np1.index(np2)-1]):
							continue
					if np2.endswith(np1):
						if math_modifiers.is_word_number(np2[:np2.index(np1)-1]):
							continue
					# writing features starts from here
					# first:: checking for the label
					
					class_finder_mode = 'joint'
					if self.binary_multiclass_mode == 0:
						class_finder_mode = 'pair_relevant'
					class_finder_obj = class_finder(class_finder_mode, self.question_prop)
					output_line = class_finder_obj.check_for_label(np1, np2)
					output_file.write(output_line)
			
					features_list = []
					loglinear_features = logLinear_Feature_finder(self.question_prop)
					features_list = loglinear_features.appropriate_feature_finder_list(features_list, np1, np1, output_line, self.binary_multiclass_mode, self.test_train_mode)
					for i in range(0, len(features_list)):
						output_file.write(' ' + str(i) + ':' + str(features_list[i]))

					output_file.write('\n')
			self.question_prop.flush()

	def read_data(self, data_index):
		# self.question_prop.read_pairs(self.file_path_refrence.relevant_pair_path, data_index)
		self.question_prop.read_whole_question(self.file_path_refrence.whole_question_path + str(data_index) + self.file_lemma_suffix)
		self.question_prop.read_question_strings(self.file_path_refrence.question_strings_path + str(data_index) + self.file_lemma_suffix)
		self.question_prop.read_ccg_parse(self.file_path_refrence.ccg_parse_path + str(data_index) + self.file_lemma_suffix)
		if self.entity_type_mode == 1:
			self.question_prop.read_question_np(self.file_path_refrence.relevant_np_entity_after_classifier + str(data_index) + self.file_lemma_suffix)
		else:
			# self.question_prop.read_question_np(self.file_path_refrence.relevant_np_type_after_classifier + str(data_index) + self.file_lemma_suffix)
			self.question_prop.read_question_np(self.file_path_refrence.np_pos_path + str(data_index) + self.file_lemma_suffix)
		self.question_prop.read_entity_types(self.file_path_refrence.relevant_np_type_after_classifier+ str(data_index) + self.file_lemma_suffix)

		self.question_prop.read_question_strings_np_before_article_ommiting(self.file_path_refrence.np_pos_path + str(data_index) + self.file_suffix)
		self.question_prop.read_question_strings_np_before_article_ommiting_lemma(self.file_path_refrence.np_pos_path + str(data_index) + self.file_lemma_suffix)
		
		# self.question_prop.read_question_strings_np_before_article_ommiting(self.file_path_refrence.question_string_np_before_article_ommiting + str(data_index) + self.file_suffix)
		# self.question_prop.read_question_strings_np_before_article_ommiting_lemma(self.file_path_refrence.question_string_np_before_article_ommiting + str(data_index) + self.file_lemma_suffix)
		self.question_prop.srl_file_path = self.file_path_refrence.srl_path
		self.question_prop.read_subset_noun_phrases(self.file_path_refrence.gold_subset_pair_paths + str(data_index) + self.file_lemma_suffix)
		self.question_prop.read_disjoint_noun_phrase(self.file_path_refrence.gold_disjoint_pair_path + str(data_index) + self.file_lemma_suffix)
		self.question_prop.read_equvalence(self.file_path_refrence.gold_equivalence_pair_path + str(data_index) + self.file_lemma_suffix)
		for j in range(3):
			self.question_prop.find_srl_args(j)
		self.question_prop.find_count_noun_stanford(self.file_path_refrence.stan_parse_file_path +str(data_index)+ self.file_lemma_suffix)
		self.question_prop.find_related_words_with_conjunction(self.file_path_refrence.stan_parse_file_path+str(data_index)+ self.file_lemma_suffix_story)
		

		self.question_prop.find_list_antonyms(self.file_path_refrence.antonym_list_path)
		# self.question_prop.find_word_list(self.file_path_refrence.synonym_list_path, self.file_path_refrence.num_of_dimentions)


		# self.question_prop.read_question_np("../../data/np_preprocessed_no_article/" + str(data_index) + '_lemma.txt.ssplit.ccg.nps')
		self.question_prop.find_subString_list()
		self.question_prop.find_noun_phrases_with_antonyms()
		self.question_prop.find_the_nouns_used_in_plural()
		self.question_prop.find_same_head_np()
		self.question_prop.find_noun_phrases_in_question(self.file_path_refrence.pos_tagging_file_path + str(data_index) + self.file_lemma_suffix)
		self.question_prop.find_repeated_noun_phrases()
		self.question_prop.initialize_numeric_value()
#from FeatureFinder_joint_learner import FeatureFinder_joint_learner
data_start = int(sys.argv[1])
data_end = int(sys.argv[2])
file_name = str(sys.argv[3])
entity_type_mode = int(sys.argv[4])
binary_multiclass_mode = int(sys.argv[5])
test_train_mode = int(sys.argv[6])
fv_finder = FeatureFinder_LogLinear_learner(test_train_mode, binary_multiclass_mode, entity_type_mode, data_start_index = data_start, data_end_index = data_end, feature_file_path = file_name)
fv_finder.write_features()

