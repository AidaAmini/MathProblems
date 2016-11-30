from basic_faeture_finder import basic_faeture_finder
from useful_np_feature_finder import useful_np_feature_finder
from entity_properties import entity_properties
from class_finder import class_finder
from file_refrence import file_refrence
import sys

class FeatureFinder_usefull_np :
	data_start_index = 0
	data_end_index = 1
	feature_file_path = ""
	question_prop = entity_properties()
	file_path_refrence = file_refrence()
	entity_type_mode = 0 #0 is for types and 1 is for entities
	file_lemma_suffix = '_lemma.txt'
	file_lemma_suffix_story = 'story_lemma.txt'
	file_suffix = '.txt'
	file_path_refrence = file_refrence()

	def __init__(self,entity_type_mode, data_end_index, data_start_index = 0, feature_file_path = "train_fv.txt"):
		self.data_start_index = data_start_index
		self.data_end_index = data_end_index
		self.feature_file_path = feature_file_path
		question_prop = entity_properties()
		self.entity_type_mode = entity_type_mode

	def write_features(self):
		output_file = open(self.feature_file_path, 'w')
		if self.entity_type_mode == 0:
			output_file_np_visualization = open(self.file_path_refrence.np_visualization_file_type, 'w')
		else:
			output_file_np_visualization = open(self.file_path_refrence.np_visualization_file_entity, 'w')

		self.question_prop = entity_properties()
		for i in range(self.data_start_index, self.data_end_index):

			if i in self.file_path_refrence.problematic_indexes:
				continue
			self.read_data(i)
			# print self.question_prop.whole_question
			# print self.question_prop.relevant_noun_phrases
			for np1 in self.question_prop.question_strings_np:
				if np1 in self.question_prop.pronoun_list or len(np1.split(' ')) >= 6:
					continue

				if (len (np1.split(' ')) == 1) and (self.question_prop.find_unit_type(np1) != '000'):
					continue
				output_file_np_visualization.write(np1 + '\t' + str(i) + '\n')
				class_finder_obj = class_finder('np_relevant', self.question_prop)
				output_line = class_finder_obj.check_for_label(np1, np1)
				output_file.write(output_line)
				feature_list = []
				basic_features = basic_faeture_finder(self.question_prop)
				feature_list = basic_features.appropriate_feature_finder_list(feature_list, np1)
				# useful_np_features = useful_np_feature_finder(self.question_prop)
				# feature_list = useful_np_features.appropriate_feature_finder_list(feature_list, np1)
				for i in range(0, len(feature_list)):
					output_file.write(' ' + str(i) + ':' + str(feature_list[i]))

				output_file.write('\n')
			self.question_prop.flush()

	def read_data(self, data_index):
		if self.entity_type_mode == 0:
			self.question_prop.read_question_np(self.file_path_refrence.question_string_nps_relevant_np_type_path + str(data_index) + self.file_lemma_suffix)
			self.question_prop.read_gold_noun_phrase(self.file_path_refrence.gold_type_path + str(data_index) + self.file_lemma_suffix)
		else:
			self.question_prop.read_question_np(self.file_path_refrence.question_string_nps_relevant_np_entity_path + str(data_index) + self.file_lemma_suffix)
			self.question_prop.read_gold_noun_phrase(self.file_path_refrence.gold_entity_path + str(data_index) + self.file_lemma_suffix)

		self.question_prop.read_whole_question(self.file_path_refrence.whole_question_path + str(data_index) + self.file_lemma_suffix)
		self.question_prop.read_question_strings(self.file_path_refrence.question_strings_path + str(data_index) + self.file_lemma_suffix)
		self.question_prop.read_ccg_parse(self.file_path_refrence.ccg_parse_path + str(data_index) + self.file_lemma_suffix)
		self.question_prop.read_question_strings_np_before_article_ommiting(self.file_path_refrence.question_string_np_before_article_ommiting + str(data_index) + self.file_suffix)
		self.question_prop.read_question_strings_np_before_article_ommiting_lemma(self.file_path_refrence.question_string_np_before_article_ommiting + str(data_index) + self.file_lemma_suffix)
		self.question_prop.srl_file_path = self.file_path_refrence.srl_path
		

		self.question_prop.find_same_head_np()
		self.question_prop.find_noun_phrases_with_antonyms()
		for j in range(3):
			self.question_prop.find_srl_args(j)
		self.question_prop.find_noun_phrases_in_question(self.file_path_refrence.pos_tagging_file_path + str(data_index) + self.file_lemma_suffix)
		self.question_prop.find_count_noun_stanford(self.file_path_refrence.stan_parse_file_path +str(data_index)+ self.file_lemma_suffix)
		self.question_prop.check_for_person_names(self.file_path_refrence.stan_parse_file_path +str(data_index)+ self.file_lemma_suffix)
		self.question_prop.read_parse_tree(self.file_path_refrence.stan_dep_parse_tree_file_path +str(data_index) + self.file_suffix)
		self.question_prop.find_counted_noun_stan_parse_tree()
		self.question_prop.find_repeated_noun_phrases()
		self.question_prop.find_noun_phrases_after_question_phrase()
		self.question_prop.find_related_words_with_conjunction(self.file_path_refrence.stan_parse_file_path+str(data_index)+ self.file_lemma_suffix_story)
		
		self.question_prop.read_pos_taggings(self.file_path_refrence.pos_tagging_file_path + str(data_index) + self.file_lemma_suffix)
		self.question_prop.find_place_modifier(self.file_path_refrence.pos_tagging_file_path + str(data_index) + self.file_lemma_suffix)
		
		self.question_prop.find_pronouns(self.file_path_refrence.pos_tagging_file_path + str(data_index) + self.file_lemma_suffix)
		

data_start = int(sys.argv[1])
data_end = int(sys.argv[2])
file_name = str(sys.argv[3])
type_entity_mode = int(sys.argv[4])
fv_finder = FeatureFinder_usefull_np(type_entity_mode, data_start_index = data_start, data_end_index = data_end, feature_file_path = file_name)
# print 'ajshakshdlashljhl'
fv_finder.write_features()

