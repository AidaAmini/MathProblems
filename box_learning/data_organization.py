import json
from pprint import pprint
from file_refrence import file_refrence

file_path_refrence = file_refrence()
kushman_problem_list = []
kushman_answer_list = []
kushman_equation_list = []

with open('data/questions.json') as data_file:    
    questions_info = json.load(data_file)
index_input = open("mappings.txt", 'r')
for q_info in questions_info:
	kushman_problem_list.append(q_info[u'sQuestion'])
	kushman_equation_list.append(q_info[u'lEquations'])
	kushman_answer_list.append(q_info[u'lSolutions'])
mapping_keys = []
mapping_vals = []
for line in index_input:
	line = line[:-1]
	parts = line.split('	')
	print parts
	mapping_keys.append(int(parts[0]))
	mapping_vals.append(int(parts[1]))

for i in range(0, len(kushman_problem_list)):
	if i not in mapping_vals:
		new_data_file = open('new'+file_path_refrence.whole_question_path + str(i)+ '.txt', 'w')
		new_data_file.write(kushman_problem_list[i] + '\n')
		# index = mapping_vals.index(i)
		# prob_index = mapping_keys[index]


# my_data_start_index = 0 
# my_data_end_index = 400
# seen_problems = []
# seen_problem_indexes = []
# for i in range(my_data_start_index, my_data_end_index):
# 	if i in file_path_refrence.problematic_indexes:
# 		continue
# 	my_data_file = open(file_path_refrence.whole_question_path + str(i) + '.txt', 'r')
# 	problem = my_data_file.readline()
# 	if problem in seen_problems:
# 		# print 'repitiiiiiiiiiiiiiiiiiiiiiiition'
# 		# print problem
# 		seen_problem_indexes.append(i)
# 	else:
# 		seen_problems.append(problem)
# 	found_flg = False
# 	max_index = 50
# 	if len(problem) <= 50:
# 		max_index = len(problem) - 10
# 	for p in range (len(kushman_problem_list)):
# 		if kushman_problem_list[p].lower().startswith(problem[:max_index]):
# 			print str(i) + '	' + str(p)
# 			found_flg = True
# 	if found_flg == False:
# 		print 'noooooooooooooooottttt found'
# 		print problem
# 		print i
		
# print seen_problem_indexes

# print(data[0])