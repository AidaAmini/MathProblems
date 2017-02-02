from file_refrence import file_refrence 
file_path_refrence = file_refrence()
input_file = open('world.txt','r')
founded = 0
not_found = 0
line = input_file.readline()
line = input_file.readline()
problem_index = -1
problem_annotated_nps = []
useful_index = [6,7,9]
output_annotation_file = ''
while line != '':
	if line[:-1] == ',,,,,,,,,,,':
		line = input_file.readline()
		continue
	parts = line[:-2].split(',')
	if len(parts) > 5 and parts[0] != '':
		if int(parts[0]) == problem_index:
			for index in useful_index:

				if parts[index] != '-' and parts[index] not in problem_annotated_nps:
					problem_annotated_nps.append(parts[index])
		else:
			if problem_index == -1:
				problem_index = parts[0]
				line = input_file.readline()
				continue
			input_file_words = open(file_path_refrence.np_pos_path_entity +str(problem_index) + '_lemma.txt')
			word_found_list = []
			for np in input_file_words:
				word_found_list.append(np[:-1])
			for np1 in problem_annotated_nps:
				found = False
				for np2 in word_found_list:
					if np2 == np1 or np2.startswith(np1) or np2.endswith(np1):
						found = True
						break
				if found == True:
					founded = founded + 1
				else:
					print np1
					not_found = not_found + 1
			problem_annotated_nps = []
			problem_index = int(parts[0])
			output_annotation_file = open(file_path_refrence.new_annotation_path + str(problem_index)+'.txt','w')
		print line
		output_annotation_file.write(line)
	line = input_file.readline()
print founded
print not_found