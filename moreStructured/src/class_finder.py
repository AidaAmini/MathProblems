from entity_properties import entity_properties

class class_finder:
	mode = ''
	question_prop = entity_properties()

	def __init__(self, mode, question_prop):
		self.question_prop = question_prop
		self.mode = mode

	def list_features_toString(self, np1, np2):
		result  = ''
		if self.mode == 'np_relevant':
			result = result + (str(self.question_prop.check_relevant(np1)))
		elif self.mode == 'disjoint':
			result = result + (str(self.question_prop.check_if_disjoint(np1, np2)))
		elif self.mode == 'subset':
			result = result +(str(self.question_prop.check_if_subset(np1, np2)))
		elif self.mode == 'joint':
			result = result + (str(self.question_prop.find_the_joint_label(np1, np2)))
		return result