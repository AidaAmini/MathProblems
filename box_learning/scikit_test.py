import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

class scikit_module():
	random_forest_num_of_trees = 10
	random_forest_classifier = RandomForestClassifier(random_forest_num_of_trees)

	def __init__(self, rf_num_of_trees, min_samples_split, max_depth):
		self.random_forest_num_of_trees = rf_num_of_trees
		if min_samples_split == None and max_depth == None:
			self.random_forest_classifier = RandomForestClassifier(self.random_forest_num_of_trees)
		elif max_depth == None:
			self.random_forest_classifier = RandomForestClassifier(self.random_forest_num_of_trees, min_samples_split=min_samples_split)
		elif min_samples_split == None:
			self.random_forest_classifier = RandomForestClassifier(self.random_forest_num_of_trees, max_depth = max_depth)
		else:
			self.random_forest_classifier = RandomForestClassifier(self.random_forest_num_of_trees, min_samples_split = min_samples_split, max_depth = max_depth)

	def random_forest_train(self, X, y):
		self.random_forest_classifier.fit(X, y)

	def random_forest_get_predictions(self, X_test):
		return self.random_forest_classifier.predict(X_test)

	def random_forest_predict_by_prob(self, X_test):
		probs = self.random_forest_classifier.predict_proba(X_test)
		labels = self.random_forest_classifier.predict(X_test)
		return (labels, probs)

	def random_forest_get_feature_importrance(self):
		return self.random_forest_classifier.feature_importances_

# rng = np.random.RandomState(0)
# X = rng.rand(100, 10)
# y = rng.binomial(1, 0.5, 100)
# X_test = rng.rand(5, 10)
# clf = RandomForestClassifier(n_estimators=10)
# clf = clf.fit(X, y)
# print clf.predict_proba(X_test)
# print clf.predict(X_test)
# print clf.get_params(deep=True)
# print clf.feature_importances_

