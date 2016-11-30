from basic_faeture_finder import basic_faeture_finder
from useful_np_feature_finder import useful_np_feature_finder
from entity_properties import entity_properties
from class_finder import class_finder
import sys

class FeatureFinder_usefull_np :
	data_start_index = 0
	data_end_index = 1
	feature_file_path = ""
	question_prop = entity_properties()

	def __init__(self, data_end_index, data_start_index = 0, feature_file_path = "train_fv.txt"):
		self.data_start_index = data_start_index
		self.data_end_index = data_end_index
		self.feature_file_path = feature_file_path
		question_prop = entity_properties()

	def write_features(self):
		output_file = open(self.feature_file_path, 'w')
		output_file_np_visualization = open("../../np_visual.txt", 'w')
		self.question_prop = entity_properties()
		for i in range(self.data_start_index, self.data_end_index):
			if i == 17 or i == 30 or i == 33 or i == 70 or i == 104 or i == 106 or i == 132:
				continue
			self.read_data(i)
			for np1 in self.question_prop.question_strings_np:
				output_file_np_visualization.write(np1 + '\n')
				class_finder_obj = class_finder('np_relevant', self.question_prop)
				output_line = class_finder_obj.list_features_toString(np1, np1)
				output_file.write(output_line)
				output_file.write(" ")
				
				start_index = 0
				basic_features = basic_faeture_finder(self.question_prop)
				output_line, start_index = basic_features.list_features_toString(start_index, np1)
				output_file.write(output_line)
				output_file.write(' ')
				useful_np_features = useful_np_feature_finder(self.question_prop)
				output_line, start_index = useful_np_features.list_features_toString(start_index, np1)
				output_file.write(output_line)
				output_file.write('\n')
			self.question_prop.flush()

	def read_data(self, data_index):
		self.question_prop.read_whole_question("../../data/problem_preprocessed/" + str(data_index) + '_lemma.txt')
		self.question_prop.read_gold_noun_phrase("../../data/ans_preprocessed/" + str(data_index) + "_lemma.ans")
		self.question_prop.read_question_strings("../../data/spilit_preprocessed/" + str(data_index) + '_lemma.txt.ssplit')
		self.question_prop.read_ccg_parse("../../data/ccg_preprocessed/" + str(data_index) + '_lemma.txt.ssplit.ccg')
		self.question_prop.read_question_np("../../data/np_preprocessed_no_article/" + str(data_index) + '_lemma.txt.ssplit.ccg.nps')
		self.question_prop.read_question_strings_np_before_article_ommiting("../../data/np_preprocessed/" + str(data_index) + '.txt.ssplit.ccg.nps')
		self.question_prop.read_question_strings_np_before_article_ommiting_lemma("../../data/np/" + str(data_index) + '_lemma.txt.ssplit.ccg.nps')
		self.question_prop.find_the_nouns_used_in_plural()
		self.question_prop.find_same_head_np()
		self.question_prop.srl_file_path = "../../data/easySrlOut.txt"
		self.question_prop.find_noun_phrases_with_antonyms()
		for j in range(2):
			self.question_prop.find_srl_args(j)
		self.question_prop.find_noun_phrases_in_question()
		self.question_prop.find_count_noun_stanford("../../data/stan/parse_stan_corenlp"+str(data_index)+"_lemma.txt")
#		self.question_prop.check_for_person_names("../../data/stan/parse_stan_corenlp"+str(data_index)+"_lemma.txt")
		self.question_prop.find_repeated_noun_phrases()
		self.question_prop.find_noun_phrases_after_question_phrase()
		self.question_prop.find_related_words_with_conjunction("../../data/stan/parse_stan_corenlp"+str(data_index)+"story.txt")
		self.question_prop.read_pos_taggings("../../data/pos/" + str(data_index) + "_lemma.pos")
		self.question_prop.find_place_modifier("../../data/pos/" + str(data_index) + "_lemma.pos")
		
		

from FeatureFinder_usefull_np import FeatureFinder_usefull_np
data_start = int(sys.argv[1])
data_end = int(sys.argv[2])
file_name = str(sys.argv[3])
fv_finder = FeatureFinder_usefull_np(data_start_index = data_start, data_end_index = data_end, feature_file_path = file_name)
fv_finder.write_features()

