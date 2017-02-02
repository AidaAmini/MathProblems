from file_refrence import file_refrence

file_path_refrence = file_refrence()
input_file = open('annotations.csv','r')
seen_problem = -1
opened_output_file = ''
for line in input_file:
	if line[0] >= '0' and line[0] <= '9':
		index = int(line.split(',')[0])
		if index != seen_problem:
			opened_output_file = open(file_path_refrence.new_annotation_path + str(index)+'.txt','w')
			seen_problem = index
		opened_output_file.write(line)