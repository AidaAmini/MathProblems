from file_refrence import file_refrence

file_path_refrence = file_refrence()
for i in range(0, 514):
	try:
		input_file = open(file_path_refrence.new_annotation_path + str(i) + '.txt','r')
		line = input_file.readline()
		if line[0] >= '0' and line[0] <= '9':
			parts = line[:-1].split(',')
			simpl_flag = False
			if parts[len(parts) - 1].startswith('y'):
				print 'here'
				simpl_flag = True
			if simpl_flag == True:
				output_file = open(file_path_refrence.new_annotation_path + 'simpl/' + str(i) + '.txt','w')
				while line != '':
					output_file.write(line)
					line = input_file.readline()
	except:
		pass
