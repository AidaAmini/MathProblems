from entity_properties import entity_properties

class class_finder:
	mode = ''
	question_prop = entity_properties()

	def __init__(self, mode, question_prop):
		self.question_prop = question_prop
		self.mode = mode

	def check_for_label(self, np1, np2):
		result  = ''
		if self.mode == 'np_relevant':
			result = result + (str(self.question_prop.check_relevant(np1)))
		elif self.mode == 'disjoint':
			result = result + (str(self.question_prop.check_if_disjoint(np1, np2)))
		elif self.mode == 'subset':
			result = result +(str(self.question_prop.check_if_subset(np1, np2)))
		elif self.mode == 'joint':
			result = result + (str(self.question_prop.find_the_joint_label(np1, np2)))
		elif self.mode == 'eq_noRel':
			joint_label = self.question_prop.find_the_joint_label(np1, np2)
			if joint_label == 3:
				result = result + '1'
			else:
				result = result + '-1'
				
		elif self.mode == 'str_disjoint':
			joint_label = self.question_prop.find_the_joint_label(np1, np2)
			if joint_label == 1:
				result = result + '1'
			else:
				result = result + '-1'

		elif self.mode == 'pair_relevant':
			joint_label = self.question_prop.find_the_joint_label(np1, np2)
			if joint_label == 0 :
				result = result + '-1'
			else:
				result = result + '1'
		return result