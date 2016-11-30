from loglinear import loglinear

class loglinear_procedure:

	def train_data(self, train_file_name, model_file_name, num_of_features, num_of_labels, learning_rate = 0.2):
		loglin = loglinear(num_of_features, num_of_labels, train_file_name, learning_rate, None, None, 'fv_label_map.txt')
		loglin.move_with_gradient()
		loglin.write_model(model_file_name)

	def test_data(self, test_file_name, model_file_name, score_file_name):
		num_of_labels, labels, num_of_features, weights = self.load_model(model_file_name)
		loglin = loglinear(num_of_features, num_of_labels, test_file_name, None, labels, weights, 'fv_label_map.txt')
		loglin.get_probs_for_test_instances(score_file_name)



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

loglin_procedure = loglinear_procedure()
loglin_procedure.train_data("trainl.txt", 'model.txt', 116, 4)
loglin_procedure.test_data("testl.txt", "model.txt", "score.txt")