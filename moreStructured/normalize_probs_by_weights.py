def normalize_probs_by_weights(weights, probs):
# 	print probs
	# print probs
	output_file = open('s_normalized.txt', 'w')
	for i in range(0, len(probs)):
		makhraj = 0
		for j in range(0, len(probs[i])):
			print probs[i][j]
			makhraj = makhraj + float(probs[i][j]) * weights[j]
		new_probs = []
		for j in range(0, len(probs[i])):
			new_probs.append((weights[j] * float(probs[i][j]) + 0.0) / (makhraj + 0.0))

		max_label = 0
		max_prob = 0
		for j in range(0, len(probs[i])):
			if new_probs[j] > max_prob:
				max_label = j
				max_prob = new_probs[j]
		if max_label ==2:
			max_label = -1
		output_file.write(str(max_label) + ' ')
		for j in range(0, len (new_probs)):
			output_file.write(str(new_probs[j]) + ' ')
		output_file.write('\n')

	
def read_probs(file_path, probs):
	input_file = open(file_path, 'r')
	for line in input_file:
		temp_prob = []
		if 'labels' in line:
			continue
		line = line[line.find(' ')+1: -2]
		parts = line.split(' ')
		for i in range(0, len(parts)):
			temp_prob.append(parts[i])
		probs.append(temp_prob)


probs = [[]]
class_weights = [1, 100 ,50]
read_probs('../s.txt', probs)
normalize_probs_by_weights(class_weights, probs)
