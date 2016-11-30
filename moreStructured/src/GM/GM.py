class GM:

	enitities = [[]]
	types = [[]]

	def __init(self):
		self.enitities = [[]]
		self.types = [[]]

	def read_entities(self, file_name):
		input_file = open(file_name, 'r')
		temp_entities = []
		for line in input_file:
			temp_entities.append(line[:-1])
		self.enitities.append(temp_entities)

	def read_types(self, file_name):
		input_file = open(file_name, 'r')
		temp_types = []
		for line in input_file:
			temp_types.append(line[:-1])
			self.types.append(temp_types)

	def check_all_constraints(self):
		print //TODO
	