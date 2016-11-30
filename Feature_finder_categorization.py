from basic_faeture_finder import basic_faeture_finder
from useful_np_feature_finder import useful_np_feature_finder
from entity_properties import entity_properties
from disjoint_feature_finder import disjoint_feature_finder
from subset_faeture_finder import subset_faeture_finder
from equivalence_feature_finder import equivalence_feature_finder
from class_finder import class_finder
from math_modifiers import math_modifiers
import sys

class Feature_finder_categorization :
	parse_file_path = ""
	data_start_index = 0
	data_end_index = 1
	feature_file_path = ""
	question_prop = entity_properties_for_cat()

	def __init__(self, data_end_index, parse_file = "parse_selection.txt", data_start_index = 0, feature_file_path = "train_fv.txt"):
		self.parse_file_path = parse_file
		self.data_start_index = data_start_index
		self.data_end_index = data_end_index
		self.feature_file_path = feature_file_path
		self.question_prop = entity_properties()

	def write_features(self):
		output_file = open(self.feature_file_path, 'w')
		self.question_prop = entity_properties()
		for i in range(self.data_start_index, self.data_end_index):
			print "i is:"
			print  i
			if i == 17 or i == 30 or i == 33 or i == 70:
				continue
			self.read_data(i)
		# 	for np1 in self.question_prop.question_strings_np:
		# 		for np2 in self.question_prop.question_strings_np:
		# 			if np1 == np2:
		# 				continue
			print self.question_prop.relevant_pairs
			for pair in self.question_prop.relevant_pairs:
				if pair.startswith('problem:'):
					continue
				parts = pair.split('\t')
				np1 = parts[0]
				np2 = parts[1]
				if np1.endswith(np2):
					if math_modifiers.is_word_number(np1[:np1.index(np2)-1]):
						continue
				if np2.endswith(np1):
					if math_modifiers.is_word_number(np2[:np2.index(np1)-1]):
						continue
				start_index = 0
				class_finder_obj = class_finder('joint', self.question_prop)
				output_line = class_finder_obj.list_features_toString(np1, np2)
				output_file.write(output_line)
				
				feature_list = []
				basic_features = basic_faeture_finder(self.question_prop)
				feature_list = basic_features.appropriate_feature_finder_list(feature_list, np1)
				feature_list = basic_features.appropriate_feature_finder_list(feature_list, np2)
				disjoint_features = disjoint_feature_finder(self.question_prop)
				feature_list = disjoint_features.appropriate_feature_finder_list(feature_list, np1, np2)
				subset_faetures = subset_faeture_finder(self.question_prop)
				feature_list = subset_faetures.appropriate_feature_finder_list(feature_list, np1, np2)
				eq_features = equivalence_feature_finder(self.question_prop)
				feature_list = eq_features.appropriate_feature_finder_list(feature_list, np1, np2)

				for i in range(0, len(feature_list)):
					output_file.write(' ' + str(i) + ':' + str(feature_list[i]))

				output_file.write('\n')
			self.question_prop.flush()

	def read_data(self, data_index):
		print "joint"
		self.question_prop.read_pairs("../../data/relevant_pair.txt", data_index)
		self.question_prop.read_whole_question("../../data/problem_preprocessed/" + str(data_index) + '_lemma.txt')
		self.question_prop.read_question_strings("../../data/spilit_preprocessed/" + str(data_index) + '_lemma.txt.ssplit')
		self.question_prop.read_ccg_parse("../../data/ccg_preprocessed/" + str(data_index) + '_lemma.txt.ssplit.ccg')
		self.question_prop.read_question_np("../../data/np_preprocessed_no_article_entity/" + str(data_index) + '_lemma.txt.ssplit.ccg.nps')
		self.question_prop.read_entity_types("../../data/np_preprocessed_no_article/"+ str(data_index) + "_lemma.txt.ssplit.ccg.nps")

		self.question_prop.read_relevant_question_string_np("../../data/np_classifier_entity/" + str(data_index) + '.txt.ssplit.ccg.nps')
		self.question_prop.read_question_strings_np_before_article_ommiting("../../data/np_preprocessed/" + str(data_index) + '.txt.ssplit.ccg.nps')
		self.question_prop.read_question_strings_np_before_article_ommiting_lemma("../../data/np_preprocessed/" + str(data_index) + '_lemma.txt.ssplit.ccg.nps')
		self.question_prop.srl_file_path = "../../data/easySrlOut.txt"
		self.question_prop.read_subset_noun_phrases("../../data/subsets/" + str(data_index) + '.lemma_subs')
		self.question_prop.read_disjoint_noun_phrase("../../data/disjoints/" + str(data_index) + '_lemma.dis')
		self.question_prop.read_equvalence("../../data/equivalence/" + str(data_index) + '_lemma.eq')
		for j in range(2):
			self.question_prop.find_srl_args(j)
		self.question_prop.find_count_noun_stanford("../../data/stan/parse_stan_corenlp"+str(data_index)+"_lemma.txt")
		self.question_prop.find_related_words_with_conjunction("../../data/stan/parse_stan_corenlp"+str(data_index)+"story.txt")
		num_of_dimentions = 300
		self.question_prop.find_list_antonyms("../../question-antonyms.dat")
		self.question_prop.find_word_list("../../we300.dat", num_of_dimentions)
		self.question_prop.find_subString_list()
		self.question_prop.find_noun_phrases_with_antonyms()
		self.question_prop.find_the_nouns_used_in_plural()
		self.question_prop.find_same_head_np()
		self.question_prop.find_noun_phrases_in_question()
		self.question_prop.find_repeated_noun_phrases()
		self.question_prop.initialize_numeric_value()
		

#from FeatureFinder_joint_learner import FeatureFinder_joint_learner
data_start = int(sys.argv[1])
data_end = int(sys.argv[2])
file_name = str(sys.argv[3])
fv_finder = FeatureFinder_joint_learner(data_start_index = data_start, data_end_index = data_end, feature_file_path = file_name)
print "hhhhilkjadlksjdaops;jd;alsdj;lajsdo;asd;akls;ldkasd"
fv_finder.write_features()

