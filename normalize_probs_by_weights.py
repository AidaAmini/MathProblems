from file_refrence import file_refrence
import sys

def normalize_probs_by_weights(weights, probs, labels, mode):
	file_refrence_path = file_refrence()
	# print probs
	# print probs
	# print labels
	if mode == 0:
		output_file = open(file_refrence_path.score_file_name_relevant_np_type_normalized, 'w')
	elif mode == 1:
		output_file = open(file_refrence_path.score_file_name_relevant_np_entity_normalized, 'w')
	elif mode == 2:
		output_file = open(file_refrence_path.score_file_name_relevant_pair_normaized, 'w')
	elif mode == 3:
		output_file = open(file_refrence_path.score_file_name_relevant_pair_parallel_normalized,'w')
	elif mode == 4:
		output_file = open(file_refrence_path.score_file_name_join_normalized, 'w')
	elif mode == 5:
		output_file = open(file_refrence_path.score_file_name_join_normalized, 'w')
	elif mode == 6:
		output_file = open(file_refrence_path.score_file_name_join_normalized, 'w')
	for i in range(0, len(probs)):
		makhraj = 0
		if len(probs[i]) == 0:
			continue
		for j in range(0, len(probs[i])):
			# print probs[i][j]
			makhraj = makhraj + weights[j] * float(probs[i][j])
		new_probs = []
		for j in range(0, len(probs[i])):
			new_probs.append((weights[j] * float(probs[i][j]) + 0.0) / (makhraj + 0.0))

		max_label = 0
		max_prob = 0
		for j in range(0, len(probs[i])):
			if new_probs[j] > max_prob:
				max_label = j
				max_prob = new_probs[j]
		label = labels[max_label]
		# if max_prob < 0.55:
		# 	label = 1
		output_file.write(str(label) + ' ')
		for j in range(0, len (new_probs)):
			output_file.write(str(new_probs[j]) + ' ')
		output_file.write('\n')

	
def read_probs(file_path, probs):
	input_file = open(file_path, 'r')
	for line in input_file:
		temp_prob = []
		if 'label' in line or len(line) < 3:
			continue
		line = line[line.find(' ')+1: -2]
		parts = line.split(' ')
		for i in range(0, len(parts)):
			temp_prob.append(parts[i])
		probs.append(temp_prob)


file_refrence_path = file_refrence()
probs = [[]]
mode = int(sys.argv[1]) #0 : np_relevant -- 1: np_relevant_entity -- 2: pair relevant --3: noRel, eq-- 4:joint

if mode == 0:
	class_weights = [10, 1]
	labels = [1, -1]
	score_file_name = file_refrence_path.score_file_name_relevant_np_type

elif mode == 1:
	class_weights = [2, 1]
	labels = [1, -1]
	score_file_name = file_refrence_path.score_file_name_relevant_np_entity

# these are the numbers for the relevant_pair_finder
elif mode == 2 :
	class_weights = [20, 1]
	labels = [1, -1]
	score_file_name = file_refrence_path.score_file_name_relevant_pair

elif mode == 3:
	class_weights = [1, 20]
	labels = [1, -1]
	score_file_name = file_refrence_path.score_file_name_relevant_pair_parallel
# These are the numbers for joint finder
elif mode == 4:
	class_weights = [1, 20, 40, 50]
	labels = [0, 3, 2, 1]
	score_file_name = file_refrence_path.score_file_name_join[:-4]+'2.txt'

elif mode == 5:
	print '55555555'
	class_weights = [1, 20, 40, 40]
	labels = [0, 3, 2, 1]
	score_file_name = "score.txt"

elif mode == 6:
	class_weights = [20, 1]
	labels = [-1, 1]
	score_file_name = "score_bin.txt"

read_probs(score_file_name, probs)
normalize_probs_by_weights(class_weights, probs, labels, mode)
