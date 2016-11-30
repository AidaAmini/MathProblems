#!/usr/bin/python

def make_compact_file_of_separate_problem_files(directory, start_index, end_index, output_file_name = 'data_preprocessed.txt'):
	output_file = open(output_file_name, 'w')
	for i in range(start_index, end_index):
		input_file = open(directory + str(i)+ '.txt', 'r')
		problem = input_file.readline()
		output_file.write(problem + '\n\n4\n')

def make_separte_data_file_of_compact_file(compact_file_name, start_index, end_index, directory):
	input_file = open(compact_file_name, 'r')
	line = input_file.readline()
	index = 0
	while index < start_index:
		index = index + 1
		line = input_file.readline()
		line = input_file.readline()
		line = input_file.readline()
	while line != '' and index < end_index:
		output_file = open(directory + str(index) + '.txt', 'w')
		output_file.write(line + '\n')
		index = index+1
		line = input_file.readline()
		line = input_file.readline()
		line = input_file.readline()
		
	
def make_annotation_files_form_np_marked_files(directory,  start_index, end_index):
	for index in range(start_index, end_index):
		input_file = open(np_directory + 'np/' + str(index) + '.txt.ssplit.ccg.nps' , 'r')
		output_file_entity = open(directory + 'entities/' + str(index) + '.ent', 'w')
		output_file_type = open(directory + 'ans/' + str(index) + '.ans', 'w')
		output_string_for_np_file = ''
		for line in input_file:
			line = line[:-1]
			if line.endswith('``e'):
				output_string_for_np_file = line[:-2] + '\n'
				output_file_entity.write(line[:-2] + '\n')
			elif line.endswith('``t'):
				output_string_for_np_file = line[:-2] + '\n'
				output_file_entity.write(line[:-2] + '\n')
				output_file_type.write(line[:-2] + '\n')
				
		
		output_np_file = open(np_directory + 'np/' + str(index) + '.txt.ssplit.ccg.nps' , 'w')
		output_np_file.write(output_string_for_np_file)
		
		
make_compact_file_of_separate_problem_files('data/problem_preprocessed/', 0, 140)