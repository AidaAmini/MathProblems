import math
import random

class loglinear:
	feature_label_map = []
	num_of_inputs = 0
	num_of_labels = 0
	num_of_features = 0
	learning_rate = 0.2
	labels_for_data = []
	label_map = []
	feature_vector = [[0 for x in range(0, num_of_features)] for x in range(num_of_inputs)]
	weights = []
	constant_sum_over_features = []
	# constact_prob_of_label_over_data = [] #len is equal to num of labels

	def __init__(self, num_of_features, num_of_labels, feature_file_name, learning_rate, labels, weights, feature_label_map_file_name):
		if weights == None and labels == None:
			self.num_of_labels = num_of_labels
			self.num_of_features = num_of_features
			self.learning_rate = learning_rate
			self.feature_vector = []
			self.weights = [0.0 for x in range(0, num_of_features)]
			feature_file = open(feature_file_name, 'r')
			ind = 0
			for line in feature_file:
				line = line[:-1]
				line_parts = line.split(' ')
				self.labels_for_data.append(line_parts[0])
				if line_parts[0] not in self.label_map:
					self.label_map.append(line_parts[0])
				features = []
				for i in range(1, len(line_parts)):#this should be equal to num of features
					features.append(float(line_parts[i].split(':')[1]))
				self.feature_vector.append(features)
				ind = ind + 1
			self.num_of_inputs = ind - 1
			self.calc_constant_sum_over_features()
			self.read_feature_label_map(feature_label_map_file_name)
		else:
			self.num_of_features = num_of_features
			self.num_of_labels = num_of_labels
			self.label_map = labels
			self.weights = weights
			feature_file = open(feature_file_name, 'r')
			ind = 0
			for line in feature_file:
				line_parts = line.split(' ')
				features = []
				for i in range(1, len(line_parts)):#this should be equal to num of features
					features.append(float(line_parts[i].split(':')[1]))
				self.feature_vector.append(features)
				ind = ind + 1
			self.num_of_inputs = ind
			self.read_feature_label_map(feature_label_map_file_name)
		# self.calc_constact_prob_of_label_over_data()

	def read_feature_label_map(self, feature_label_map_file_name):
		feature_label_map_file = open(feature_label_map_file_name, 'r')
		self.feature_label_map = []
		for line in feature_label_map_file:
			line = line[:-1]
			line_parts = line.split(' ')
			for i in range(int(line_parts[1]), int(line_parts[2])):
				self.feature_label_map.append(line_parts[0])

	# def __init__(self, num_of_features, num_of_labels, labels, weights, feature_file_name):
	# 	self.num_of_features = num_of_features
	# 	self.num_of_labels = num_of_labels
	# 	self.labels_for_data = labels
	# 	self.weights = weights
	# 	feature_file = open(feature_file_name, 'r')
	# 	ind = 0
	# 	for line in feature_file:
	# 		line_parts = line.split(' ')
	# 		for i in range(1, len(line_parts)):#this should be equal to num of features
	# 			self.feature_vector[ind][i] = line_parts[i]
	# 		ind = ind + 1
	# 	self.num_of_inputs = ind

	def calc_constant_sum_over_features(self):
		for i in range(0, self.num_of_features / self.num_of_labels):
			count = [0 for x in range(self.num_of_labels)]
			for j in range(0, self.num_of_inputs):
				y_ind = int (self.labels_for_data[j])
				count[y_ind] = count[y_ind] + self.feature_vector[j][i + (self.num_of_features/self.num_of_labels) * y_ind]
			self.constant_sum_over_features.append(count)
	
	def dot_product(self, inputId, label):
		res = 0.0
		flag = True
		for i in range(0, self.num_of_features):
			if label == self.feature_label_map[i]:
				res = res + self.weights[i] * self.feature_vector[inputId][i]
		return res

	def calc_py_given_xv(self, inputId, label):
		soorat = math.exp(self.dot_product(inputId, label))
		makhraj = 0.0
		for i in range(0, self.num_of_labels):
			new_label = self.label_map[i]
			makhraj = makhraj + math.exp(self.dot_product(inputId, new_label))
		return (soorat+0.0)/ (makhraj + 0.00001)


	def calc_gradient_decent_by_featureID(self, featureId):
		res = 0
		for i in range(0, self.num_of_labels):
			res = res + self.constant_sum_over_features[featureId][i]
		secont_part = 0.0
		for i in range(0, self.num_of_inputs):
			for j in range(0, self.num_of_labels):
				label = self.label_map[j]
				label_id = int(label)
				res = self.constant_sum_over_features[featureId][label_id]
				# if self.feature_vector[i][featureId + (self.num_of_features/ self.num_of_labels) * label_id] != 0:
				pi = self.calc_py_given_xv(i, label)
				if pi > 1:
					print "tooooooo large"
				elif pi < 0:
					print  "toooooo smallllllllll"
				secont_part = secont_part + self.calc_py_given_xv(i, label) * self.feature_vector[i][featureId + (self.num_of_features/ self.num_of_labels) * label_id] #self.constant_sum_over_features[featureId % self.num_of_features][label_id]
		print res
		print secont_part
		return res - secont_part

	def move_with_gradient(self):
		max_delta = 10
		num_of_iters = 0
		while(max_delta > 0.05 and num_of_iters < 1000):
			max_delta = 0
			for i in range(0, self.num_of_features/ self.num_of_labels):
				delta = self.calc_gradient_decent_by_featureID(i)
				print "delta :: " + str(delta)
				if abs(delta) > max_delta:
					max_delta = abs(delta)
				self.weights[i] = self.weights[i] + self.learning_rate * delta
			num_of_iters = num_of_iters +1
			# self.write_model('temp_models/temp_model'+str(num_of_iters)+'.txt')

	def write_model(self, model_file_name):
		model_file = open(model_file_name, 'w')
		model_file.write(str(self.num_of_labels) + '\n')
		for i in range(0, self.num_of_labels):
			model_file.write(self.label_map[i] + '\n')
		model_file.write(str(self.num_of_features) + '\n')
		for i in range(0, self.num_of_features):
			model_file.write(str(self.weights[i]) + '\n')

	def load_model(self, model_file_name):
		model_file = open(model_file_name, 'r')
		num_of_labels = int(model_file.readline()[:-1])
		labels = []
		for i in range(num_of_labels):
			labels.append(model_file.readline()[:-1])
		num_of_features = int(model_file.readline()[:-1])
		weights = []
		for i in range(0, num_of_features):
			weights.append(float(model_file.readline()[:-1]))
		return (num_of_labels, labels, num_of_features, weights)

	def get_probs_for_test_instances(self, score_file_name):
		score_file = open(score_file_name, 'w')
		output_probs = [[0.0 for x in range(self.num_of_labels)] for x in range(self.num_of_inputs)]
		output_labels = []
		for i in range(0, self.num_of_inputs):
			max_prob = 0.0
			label = 0
			for j in range(0, self.num_of_labels):
				l = int(self.label_map[j])
				prob= self.calc_py_given_xv(i, self.label_map[j])
				output_probs[i][j] = prob
				if prob > max_prob:
					max_prob = prob
					label = self.label_map[j]
			output_labels.append(label)
			score_file.write(str(label) + ' ')
			for j in range(0, self.num_of_labels - 1):
				score_file.write(str(output_probs[i][j]) + ' ')
			score_file.write(str(output_probs[i][self.num_of_labels - 1]) + '\n')
		return output_probs
















