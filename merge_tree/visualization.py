from html import HTML
import numpy as np
import matplotlib.pyplot as plt

output_file = open('visualization.html', 'w')
num_of_iters = 4
h = HTML()
feature_importances = []
feature_names = []
th_list = []
fp_samples = []
tp_samples = []
fn_samples = []
tn_samples = []
recal = []
precision = []
f1_score = []

def read_stats(num_of_iterations, recal, precision, f1_score):
	for i in range(0, num_of_iterations):
		recal_new = []
		precision_new = []
		f1_score_new = []
		input_file = open('run_log' + str(i) + '.txt', 'r')
		line = input_file.readline()
		while line != '':
			if 'recal is' in line:
				parts = line[:-1].split('\t')
				print line
				recal_new.append(parts[3])
			if 'precision is' in line:
				parts = line[:-1].split('\t')
				precision_new.append(parts[3])
			if 'f1_score is' in line:
				parts = line[:-1].split('\t')
				f1_score_new.append(parts[3])
			line = input_file.readline()
		recal.append(recal_new)
		precision.append(precision_new)
		f1_score.append(f1_score_new)
	return (recal, precision, f1_score)
			


def read_feature_importance(num_of_iterations, feature_importances):
	for i in range(0, num_of_iterations):
		temp_importances = []
		input_file = open('run_log' + str(i) + '.txt', 'r')
		line = input_file.readline()
		while line != '':
			if 'feature_importances' in line:
				while ']' not in line:
					line = input_file.readline()
					temp_line = line[:-1]
					if ']' in temp_line:
						temp_line = temp_line.replace(']', '')
					if '[' in temp_line:
						temp_line = temp_line.replace('[', '')

					parts = temp_line.split(' ')
					for part in parts:
						if len(part) > 1:
							temp_importances.append(part)

				break
			line = input_file.readline()
		feature_importances.append(temp_importances)
	return feature_importances

def read_feature_names(feature_names):
	input_file = open('run_log0.txt', 'r')
	line = input_file.readline()
	while line != '':
		if 'feature list names are :' in line:
			line = input_file.readline()
			while 'end of feature_list_name' not in line:
				line = line[line.index('	') + 1: -1]
				feature_names.append(line)
				line = input_file.readline()
			break
		line = input_file.readline()
	return feature_names

def read_th_nums(th_list):
	input_file = open('run_log0.txt', 'r')
	line = input_file.readline()
	while line != '':
		if 'new ths' in line:
			line = line[:-1].split('	')
			if line[1] not in th_list:
				th_list.append(line[1])
		line = input_file.readline()
	return th_list

def read_samples(num_of_iterations, tp_samples, fp_samples, tn_samples, fn_samples, th_list):
	for i in range(0, num_of_iterations):
		input_file = open('run_log' + str(i) + '.txt', 'r')
		tp_new = [[] for x in range(0, len(th_list))]
		fp_new = [[] for x in range(0, len(th_list))]
		tn_new = [[] for x in range(0, len(th_list))]
		fn_new = [[] for x in range(0, len(th_list))]
		line = input_file.readline()
		while line != '':
			if 'updating stats ends' in line:
				break
			if 'sampling' in line:
				line = input_file.readline()
				parts = line[:-1].split('	')
				
				th = parts[0]
				th_index = th_list.index(th)
				y_test = int(parts[1])
				y_predicted = int(parts[2])
				chain = []
				chain.append(parts[3])
				chain.append(parts[4])
				if y_test == 1:
					if y_predicted == 1:
						tp_new[th_index].append(chain)
					else:
						fn_new[th_index].append(chain)
				else:
					if y_predicted == 1:
						fp_new[th_index].append(chain)
					else:
						tn_new[th_index].append(chain)
			line = input_file.readline()
		tp_samples.append(tp_new)
		fp_samples.append(fp_new)
		tn_samples.append(tn_new)
		fn_samples.append(fn_new)

	return (tp_samples, fp_samples, tn_samples, fn_samples)




th_list = read_th_nums(th_list)
feature_importances = read_feature_importance(num_of_iters, feature_importances)
feature_names = read_feature_names(feature_names)
tp_samples, fp_samples, tn_samples, fn_samples = read_samples(num_of_iters, tp_samples, fp_samples, tn_samples, fn_samples, th_list)
recal, precision, f1_score = read_stats(num_of_iters, recal, precision, f1_score)

h.h1('While training on the problems 0-200', color = ('rgb(205, 12, 24)'))
for i in range(0, num_of_iters, 2):
	print len(feature_names)
	h.h2('considering iteration number ' + str(i))
	h.h3("Feature importances are:")
	table_data = []
	table_line = []
	table_line.append("feature_name")
	table_line.append("importance")
	table_data.append(table_line)
	h.p("feature_name \t\t\t importance")
	for j in range(0, len(feature_names)):
		table_line = []
		table_line.append(feature_names[j])
		table_line.append(feature_importances[i][j])
		table_data.append(table_line)
		h.p(feature_names[j] + '\t\t\t ' + feature_importances[i][j])

	h.h3("TP samples are")
	for k in range(0, len(th_list)):
		for j in range(0, len(tp_samples[i][k])):
			print tp_samples[i][k][j]
			h.p(str(tp_samples[i][k][j]))
	h.h3("FP samples are")
	for k in range(0, len(th_list)):
		for j in range(0, len(fp_samples[i][k])):
			h.p(str(fp_samples[i][k][j]))
	h.h3("TN samples are")
	for k in range(0, len(th_list)):
		for j in range(0, len(tn_samples[i][k])):
			h.p(str(tn_samples[i][k][j]))
	h.h3("FN samples are")
	for k in range(0, len(th_list)):
		for j in range(0, len(fn_samples[i][k])):
			h.p(str(fn_samples[i][k][j]))
	# h.p(str(table_data))

h.h1('While training on the problems 200-400')
for i in range(1, num_of_iters, 2):
	h.h3('considering iteration number ' + str(i))
	h.p("feature_name \t\t\t importance")
	for j in range(0, len(feature_names)):
		h.p(feature_names[j] + '\t\t\t ' + feature_importances[i][j])

	h.h3("TP samples are")
	for k in range(0, len(th_list)):
		for j in range(0, len(tp_samples[i][k])):
			print tp_samples[i][k][j]
			h.p(str(tp_samples[i][k][j]))
	h.h3("FP samples are")
	for k in range(0, len(th_list)):
		for j in range(0, len(fp_samples[i][k])):
			h.p(str(fp_samples[i][k][j]))
	h.h3("TN samples are")
	for k in range(0, len(th_list)):
		for j in range(0, len(tn_samples[i][k])):
			h.p(str(tn_samples[i][k][j]))
	h.h3("FN samples are")
	for k in range(0, len(th_list)):
		for j in range(0, len(fn_samples[i][k])):
			h.p(str(fn_samples[i][k][j]))
# print feature_importances
# print tp_samples
# print h
plt.plot(th_list, recal[0], '.')
plt.plot(th_list, precision[0], '*')
plt.plot(th_list, f1_score[0], '-')
plt.show()

plt.plot(th_list, recal[1], '.')
plt.plot(th_list, precision[1], '*')
plt.plot(th_list, f1_score[1], '-')
plt.show()

plt.plot(th_list, recal[2], '.')
plt.plot(th_list, precision[2], '*')
plt.plot(th_list, f1_score[2], '-')
plt.show()

plt.plot(th_list, recal[3], '.')
plt.plot(th_list, precision[3], '*')
plt.plot(th_list, f1_score[3], '-')
plt.show()

output_file.write(str(h))
output_file.close()