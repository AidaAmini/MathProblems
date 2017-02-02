from file_refrence import file_refrence
from random import randint
import copy

useful_indexes = [4,5,6,7,8,9,10]
change_group_one = [4,6,7,9]
change_group_two = [5,8,10]
file_path_refrence = file_refrence()
for i in range(0, 514):
	print i
	true_table = []
	false_tables = []
	try:
		input_file=open(file_path_refrence.new_annotation_path + str(i) + '.txt', 'r')
		count = 0
		for line in input_file:
			line_parts = line[:-2].split(',')
			merges_needed = len(line_parts) - 11
			while merges_needed > 0:
				for k in range(len(line_parts)-1):
					if line_parts[k].startswith("\"") and line_parts[k+1].endswith("\""):
						line_parts[k] = line_parts[k][1:] + ',' + line_parts[k+1][:-1]
						line_parts.remove(line_parts[k+1])
				merges_needed = merges_needed - 1
			print line_parts
			print len(line_parts)
			box_row = []
			for j in range(0, len(useful_indexes)):
				if not line_parts[useful_indexes[j]].startswith('-'):
					count = count + 1
				box_row.append(line_parts[useful_indexes[j]])
			if len(box_row) != 0:
				true_table.append(box_row)
		table_needed = count/2
		change_needed = count/2
		table_count = 0
		count_of_iters = 0
		while table_count != table_needed and count_of_iters < 100:
			count_of_iters =  count_of_iters + 1
			new_table = copy.deepcopy(true_table)
			change_count = 0
			seen_changes_list = []

			src_change_row = randint(0, len(true_table) - 1)
			src_change_column = randint(0, len(useful_indexes) -1)
			dst_change_row = randint(0, len(true_table) - 1)
			dst_change_column = randint(0, len(useful_indexes) -1)
			change_iter_count = 0
			while change_count != change_needed and change_iter_count != 100:
				change_iter_count = change_iter_count + 1
				if (src_change_row == dst_change_row) and (src_change_column == dst_change_column):
					src_change_row = randint(0, len(true_table) - 1)
					src_change_column = randint(0, len(useful_indexes) -1)
					dst_change_row = randint(0, len(true_table) - 1)
					dst_change_column = randint(0, len(useful_indexes) -1)
					continue
				if (src_change_row, src_change_column, dst_change_row, dst_change_column) not in seen_changes_list:
					seen_changes_list.append((src_change_row, src_change_column, dst_change_row, dst_change_column))
					seen_changes_list.append((dst_change_row, dst_change_column, src_change_row, src_change_column))
					if (useful_indexes[src_change_row] in change_group_one and useful_indexes[dst_change_row] in change_group_one) or (useful_indexes[src_change_row] in change_group_two and useful_indexes[dst_change_row] in change_group_two):
						temp = new_table[src_change_row][src_change_column]
						change_flag = True
						for k in range(0, len(new_table[dst_change_row])):
							if new_table[dst_change_row][k] == temp:
								change_flag = False
								break
						if change_flag == True:
							new_table[dst_change_row][dst_change_column] = new_table[src_change_row][src_change_column]
							new_table[src_change_row][src_change_column] = temp
							change_count = change_count + 1
						src_change_row = randint(0, len(true_table) - 1)
						src_change_column = randint(0, len(useful_indexes) -1)
						dst_change_row = randint(0, len(true_table) - 1)
						dst_change_column = randint(0, len(useful_indexes) -1)

					else:
						src_change_row = randint(0, len(true_table) - 1)
						src_change_column = randint(0, len(useful_indexes) -1)
						dst_change_row = randint(0, len(true_table) - 1)
						dst_change_column = randint(0, len(useful_indexes) -1)
				else:
					src_change_row = randint(0, len(true_table) - 1)
					src_change_column = randint(0, len(useful_indexes) -1)
					dst_change_row = randint(0, len(true_table) - 1)
					dst_change_column = randint(0, len(useful_indexes) -1)
			adding_flag = True
			for t in false_tables:
				if new_table == t:
					adding_flag = False
					break
			if adding_flag == True:
				false_tables.append(new_table)
				table_count = table_count + 1

		output_file = open(file_path_refrence.new_annotation_path + 'tables/' + str(i) + '.txt', 'w')
		output_file.write("1\n")
		output_file.write(str(true_table)+ '\n')
		for j in range(0, len(false_tables)):
			output_file.write("-1\n")
			output_file.write(str(false_tables[j])+ '\n')

	except:
		pass
















