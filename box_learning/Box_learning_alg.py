from scikit_test import scikit_module
from file_refrence import file_refrence
from box_data_structure import box_data_structure
from inference_module import inference_module

class Box_learning_alg:
	start_index = 0
	end_index = 0
	indexes = []
	file_path_refrence = file_refrence()
	box_structure = box_data_structure()
	file_lemma_suffix = '_lemma.txt'
	file_suffix = '.txt'
	test_boxes = []
	inf_module = inference_module(None)

	def __init__(self, start_index, end_index):
		self.start_index = start_index
		self.end_index = end_index

	def find_learning_indexes(self):
		self.indexes = []
		for i in range(self.start_index, self.end_index):
			try:
				input_file = open(self.file_path_refrence.new_annotation_path+ 'tables_partials_all/' + str(i) + '.txt', 'r')
				self.indexes.append(i)
			except:
				pass

	def read_data_by_problem_index(self, problem_index, box_structure):
		box_structure.read_whole_question(self.file_path_refrence.whole_question_path + str(problem_index) + self.file_lemma_suffix)
		box_structure.find_related_words_with_conjunction(self.file_path_refrence.stan_parse_file_path+str(problem_index)+ self.file_suffix)
		box_structure.read_noun_phrases(self.file_path_refrence.question_string_nps_relevant_np_entity_path + str(problem_index) + self.file_lemma_suffix)
		box_structure.read_question_strings(self.file_path_refrence.question_strings_path + str(problem_index) + self.file_lemma_suffix)
		box_structure.find_noun_phrases_in_question(self.file_path_refrence.pos_tagging_file_path + str(problem_index) + self.file_lemma_suffix)
		box_structure.find_count_noun_stanford(self.file_path_refrence.pos_tagging_file_path+str(problem_index)+ self.file_lemma_suffix)
		box_structure.read_tables(self.file_path_refrence.new_annotation_path + 'tables_partials_all/' + str(problem_index) + '.txt')
		box_structure.find_repeated_noun_phrases()
		box_structure.find_same_head_np()

	def train_procedure(self):
		self.find_learning_indexes()
		output_tarin = open('train_debug.txt', 'w')
		for i in range(0, 50):
			if self.indexes[i] == 48:
				continue
			print 'problem :  ' + str(self.indexes[i])
			prob_index = self.indexes[i]
			self.read_data_by_problem_index(prob_index, self.box_structure)
			for j in range(len(self.box_structure.true_exmples)):
				self.test_boxes.append(self.box_structure.true_exmples[j])
				output_tarin.write(str(self.box_structure.calc_box_edit_distance(self.box_structure.true_exmples[0], self.box_structure.true_exmples[j])) + ' ')
				# output_tarin.write(str(self.box_structure.calc_box_edit_distance) + ' ')
				feature_list, feature_name_list = self.box_structure.table_cell_features([], [], 6, 4, self.box_structure.true_exmples[j])
				feature_list, feature_name_list = self.box_structure.table_row_feautres(feature_list, feature_name_list, 6, 4, self.box_structure.true_exmples[j])
				feature_list, feature_name_list = self.box_structure.table_column_feautres(feature_list, feature_name_list, 6, 4, self.box_structure.true_exmples[j])
				
				for k in range(len(feature_list) - 1):
					output_tarin.write(str(k) + ':' + str(feature_list[k]) + ' ')
				output_tarin.write(str(len(feature_list)-1) + ':' + str(feature_list[len(feature_list)-1]) + '\n')
			# output_tarin.write('1 ')
			# feature_list, feature_name_list = self.box_structure.table_cell_features([], [], 6, 4, self.box_structure.true_exmple)
			# print len(feature_list)
			# feature_list, feature_name_list = self.box_structure.table_row_feautres(feature_list, feature_name_list, 6, 4, self.box_structure.true_exmple)
			# feature_list, feature_name_list = self.box_structure.table_column_feautres(feature_list, feature_name_list, 6, 4, self.box_structure.true_exmple)
			# print len(feature_list)
			# for k in range(len(feature_list) - 1):
			# 	output_tarin.write(str(k) + ':' + str(feature_list[k]) + ' ')
			# output_tarin.write(str(len(feature_list)-1) + ':' + str(feature_list[len(feature_list)-1]) + '\n')
			for j in range(len(self.box_structure.false_examples)):
				output_tarin.write(str(self.box_structure.calc_box_edit_distance(self.box_structure.true_exmples[0], self.box_structure.false_examples[j])) + ' ')
				# output_tarin.write('-1 ')
				feature_list, feature_name_list = self.box_structure.table_cell_features([], [], 6, 4, self.box_structure.false_examples[j])
				feature_list, feature_name_list = self.box_structure.table_row_feautres(feature_list, feature_name_list, 6, 4, self.box_structure.false_examples[j])
				feature_list, feature_name_list = self.box_structure.table_column_feautres(feature_list, feature_name_list, 6, 4, self.box_structure.false_examples[j])
				
				for k in range(len(feature_list) - 1):
					output_tarin.write(str(k) + ':' + str(feature_list[k]) + ' ')
				output_tarin.write(str(len(feature_list)-1) + ':' + str(feature_list[len(feature_list)-1]) + '\n')
			self.box_structure.destruct()

	def test_procedure(self):
		self.find_learning_indexes()
		output_tarin = open('test.txt', 'w')
		print len(self.indexes)
		for i in range(150, len(self.indexes) ):
			if self.indexes[i] == 422 or self.indexes[i] == 434 or self.indexes[i] == 480 or self.indexes[i] == 482 or self.indexes[i] == 487 or self.indexes[i] == 499 or self.indexes[i] == 503:
				continue
			print 'problem :  ' + str(self.indexes[i]) + '     ' + str(i)
			prob_index = self.indexes[i]
			self.read_data_by_problem_index(prob_index, self.box_structure)
			for j in range(len(self.box_structure.true_exmples)):
				self.test_boxes.append(self.box_structure.true_exmples[j])
				output_tarin.write(str(self.box_structure.calc_box_edit_distance(self.box_structure.true_exmples[0], self.box_structure.true_exmples[j])) + ' ')
				# output_tarin.write(str(self.box_structure.calc_box_edit_distance) + ' ')
				feature_list, feature_name_list = self.box_structure.table_cell_features([], [], 6, 4, self.box_structure.true_exmples[j])
				feature_list, feature_name_list = self.box_structure.table_row_feautres(feature_list, feature_name_list, 6, 4, self.box_structure.true_exmples[j])
				feature_list, feature_name_list = self.box_structure.table_column_feautres(feature_list, feature_name_list, 6, 4, self.box_structure.true_exmples[j])
				
				for k in range(len(feature_list) - 1):
					output_tarin.write(str(k) + ':' + str(feature_list[k]) + ' ')
				output_tarin.write(str(len(feature_list)-1) + ':' + str(feature_list[len(feature_list)-1]) + '\n')
			for j in range(len(self.box_structure.false_examples)):
				self.test_boxes.append(self.box_structure.false_examples[j])
				output_tarin.write(str(self.box_structure.calc_box_edit_distance(self.box_structure.true_exmples[0], self.box_structure.false_examples[j])) + ' ')
				# output_tarin.write(str(self.box_structure.calc_box_edit_distance) + ' ')
				feature_list, feature_name_list = self.box_structure.table_cell_features([], [], 6, 4, self.box_structure.false_examples[j])
				feature_list, feature_name_list = self.box_structure.table_row_feautres(feature_list, feature_name_list, 6, 4, self.box_structure.false_examples[j])
				feature_list, feature_name_list = self.box_structure.table_column_feautres(feature_list, feature_name_list, 6, 4, self.box_structure.false_examples[j])
				
				for k in range(len(feature_list) - 1):
					output_tarin.write(str(k) + ':' + str(feature_list[k]) + ' ')
				output_tarin.write(str(len(feature_list)-1) + ':' + str(feature_list[len(feature_list)-1]) + '\n')
			self.box_structure.destruct()



	def calc_precision_recal(self):
		for ths in range(0, 10):
			th = ((ths + 0.0)/10)
			print th
			tp = 0
			tn = 0
			fn = 0
			fp = 0
			res_file = open('res.txt','r')
			for line in res_file:
				line_parts = line[:-1].split('	')
				prob_positive = float(line_parts[3])
				# print prob_positive
				true_label = int(line_parts[0])
				y_label = -1
				if prob_positive >= th:
					# print 'here'
					# print prob_positive >= th + 0.0
					# print prob_positive + '  >  ' + str(th)
					y_label = 1
				if y_label == 1 and true_label == 1:
					tp = tp + 1
				elif y_label == 1 and true_label !=1:
					fp = fp + 1
				elif y_label == -1 and true_label == 1:
					fn = fn + 1
				else:
					tn = tn + 1
			print tp 
			recall = (tp + 0.0)/(tp+fn)
			percision = (tp + 0.0)/(tp+fp)
			f1_score = 2* (((percision * recall)+ 0.0)/(recall + percision + 0.0001))
			print 'recal is :' + str(recall)
			print 'precision is : ' + str(percision)
			print 'f1 score is : ' + str(f1_score)


	def train_scikit(self):
		input_train_file = open('train.txt', 'r')
		input_test_file = open('test.txt', 'r')
		self.scikit_train_module = scikit_module(30, 10, 10)
		x_train = []
		y_train = []
		x_test = []
		y_test = []
		output_res = open('res.txt','w')
		output_visualize = open('res_visual.txt','w')
		for line in input_train_file:
			parts = line[:-1].split(' ')
			x_line = []
			if parts[0].startswith('-1'):
				y_train.append(-1)
			else:
				y_train.append(1)
			for i in range(1, len(parts)):
				x_line.append(float(parts[i].split(':')[1]))
			x_train.append(x_line)

		for line in input_test_file:
			parts = line[:-1].split(' ')
			x_line = []
			if parts[0].startswith('-1'):
				y_test.append(-1)
			else:
				y_test.append(1)
			for i in range(1, len(parts)):
				x_line.append(float(parts[i].split(':')[1]))
			x_test.append(x_line)
		
		print len(x_train[0])
		print 'step1'
		self.scikit_train_module.random_forest_train(x_train, y_train)
		print 'step2'
		
		y_classified, y_probs = self.scikit_train_module.random_forest_predict_by_prob(x_test)
		print 'step3'
		
		for j in range(len(y_test)):
			output_res.write(str(y_test[j])+ '	' + str(y_classified[j]) + '	' + str(y_probs[j][0]) + '	' + str(y_probs[j][1]) + '\n')
			for jj in range(len(self.test_boxes[j])):

				output_visualize.write(str(self.test_boxes[j][jj]) + '\n')
			# print self.box_structure.true_exmple
			# for jj in range(len(self.box_structure.true_exmple)):
			# 	for jjj in range(len(self.box_structure.true_exmple[0])):
			# 		output_visualize.write(str(self.test_boxes[jj][jjj]) + '\n')
			output_visualize.write(str(y_test[j])+ '	' + str(y_classified[j]) + '	' + str(y_probs[j][0]) + '	' + str(y_probs[j][1]) + '\n\n')


	def inf_procedure(self):
		self.find_learning_indexes()
		input_train_file = open('train.txt', 'r')
		self.scikit_train_module = scikit_module(30, 10, 10)
		x_train = []
		y_train = []
		for line in input_train_file:
			parts = line[:-1].split(' ')
			x_line = []
			if parts[0].startswith('-1'):
				y_train.append(-1)
			else:
				y_train.append(1)
			for i in range(1, len(parts)):
				x_line.append(float(parts[i].split(':')[1]))
			x_train.append(x_line)
		print 'step1'
		self.scikit_train_module.random_forest_train(x_train, y_train)
		print 'step2'
		self.inf_module = inference_module(self.scikit_train_module)
		for i in range(150, len(self.indexes) ):
			self.inf_module.inference_procedure_per_problem(self.indexes[i])


box = Box_learning_alg(0,514)
box.inf_procedure()
# box.find_learning_indexes()
# box.train_procedure()
# box.test_procedure()
# box.train_scikit()
# box.calc_precision_recal()



