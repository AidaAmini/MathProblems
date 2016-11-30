from basic_faeture_finder import basic_faeture_finder
from useful_np_feature_finder import useful_np_feature_finder
from entity_properties import entity_properties
from disjoint_feature_finder import disjoint_feature_finder
from subset_faeture_finder import subset_faeture_finder
from equivalence_feature_finder import equivalence_feature_finder
from class_finder import class_finder
from math_modifiers import math_modifiers
from file_refrence import file_refrence
import sys

class Feature_finder_struct_disjoint :
	data_start_index = 0
	data_end_index = 1
	feature_file_path = ""
	question_prop = entity_properties()
	non_relevant_string = ["problem: "]
	file_path_refrence = file_refrence()
	file_lemma_suffix = '_lemma.txt'
	file_lemma_suffix_story = 'story_lemma.txt'
	file_suffix = '.txt'
	entity_type_mode=1

	def __init__(self,entity_type_mode, data_end_index, data_start_index = 0, feature_file_path = "train_fv.txt"):
		self.data_start_index = data_start_index
		self.data_end_index = data_end_index
		self.feature_file_path = feature_file_path
		self.question_prop = entity_properties()
		self.entity_type_mode = entity_type_mode

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
			for np1 in self.question_prop.question_strings_np:
				if np1 in self.question_prop.pronoun_list or len(np1.split(' ')) >= 6:
					continue
				for np2 in self.question_prop.question_strings_np:
					if np2 in self.question_prop.pronoun_list or len(np2.split(' ')) >= 6:
						continue
					if np1 == np2:
						continue
					if np1.endswith(np2):
						if math_modifiers.is_word_number(np1[:np1.index(np2)-1]):
							continue
					if np2.endswith(np1):
						if math_modifiers.is_word_number(np2[:np2.index(np1)-1]):
							continue
					start_index = 0
					class_finder_obj = class_finder('str_disjoint', self.question_prop)
					output_line = class_finder_obj.check_for_label(np1, np2)
					output_file.write(output_line)
					
					
					feature_list = []
					basic_features = basic_faeture_finder(self.question_prop)
					feature_list = basic_features.appropriate_feature_finder_list(feature_list, np1)
					feature_list = basic_features.appropriate_feature_finder_list(feature_list, np2)
					useful_np_features = useful_np_feature_finder(self.question_prop)
					feature_list = useful_np_features.appropriate_feature_finder_list(feature_list, np1, np2)
					disjoint_features = disjoint_feature_finder(self.question_prop)
					feature_list = disjoint_features.appropriate_feature_finder_list(feature_list, np1, np2)
					for i in range(0, len(feature_list)):
						output_file.write(' ' + str(i) + ':' + str(feature_list[i]))
					
					output_file.write('\n')

			self.question_prop.flush()

	def read_data(self, data_index):
		print "joint"
		self.question_prop.read_pairs(self.file_path_refrence.relevant_pair_path, data_index)
		self.question_prop.read_whole_question(self.file_path_refrence.whole_question_path + str(data_index) + self.file_lemma_suffix)
		self.question_prop.read_question_strings(self.file_path_refrence.question_strings_path + str(data_index) + self.file_lemma_suffix)
		self.question_prop.read_ccg_parse(self.file_path_refrence.ccg_parse_path + str(data_index) + self.file_lemma_suffix)
		if self.entity_type_mode == 1:
			self.question_prop.read_question_np(self.file_path_refrence.question_string_nps_relevant_np_entity_path + str(data_index) + self.file_lemma_suffix)
		else:
			self.question_prop.read_question_np(self.file_path_refrence.question_string_nps_relevant_np_type_path + str(data_index) + self.file_lemma_suffix)
		# self.question_prop.read_entity_types(self.file_path_refrence.relevant_np_type_after_classifier+ str(data_index) + self.file_lemma_suffix)

		self.question_prop.read_question_strings_np_before_article_ommiting(self.file_path_refrence.question_string_np_before_article_ommiting + str(data_index) + self.file_suffix)
		self.question_prop.read_question_strings_np_before_article_ommiting_lemma(self.file_path_refrence.question_string_np_before_article_ommiting + str(data_index) + self.file_lemma_suffix)
		self.question_prop.srl_file_path = self.file_path_refrence.srl_path
		self.question_prop.read_subset_noun_phrases(self.file_path_refrence.gold_subset_pair_paths + str(data_index) + self.file_lemma_suffix)
		self.question_prop.read_disjoint_noun_phrase(self.file_path_refrence.gold_disjoint_pair_path + str(data_index) + self.file_lemma_suffix)
		self.question_prop.read_equvalence(self.file_path_refrence.gold_equivalence_pair_path + str(data_index) + self.file_lemma_suffix)
		for j in range(3):
			self.question_prop.find_srl_args(j)
		self.question_prop.find_count_noun_stanford(self.file_path_refrence.stan_parse_file_path +str(data_index)+ self.file_lemma_suffix)
		self.question_prop.find_related_words_with_conjunction(self.file_path_refrence.stan_parse_file_path+str(data_index)+ self.file_lemma_suffix_story)
		

		self.question_prop.find_list_antonyms(self.file_path_refrence.antonym_list_path)
		
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
fv_finder = Feature_finder_struct_disjoint(entity_type_mode, data_start_index = data_start, data_end_index = data_end, feature_file_path = file_name)
fv_finder.write_features()

