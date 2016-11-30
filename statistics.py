word_list = []
word_count = []
def first_statistics():
	for i in range(0, 200):
		input_file = open('../../data/problems/' + str(i) + '_lemma.txt')
		for line in input_file:
			words = line.split(' ')
			for word in words:
				if word in word_list:
					word_count[word_list.index(word)] = word_count[word_list.index(word)] + 1
				else:
					word_list.append(word)
					word_count.append(1)
	for i in range(0, len(word_list)):
		if word_count[i] > 20 and word_count[i] < 100:
			print word_list[i]

def pair_statistics():
	pairs = []
	disjoint_pairs = []
	subset_pairs = []
	par_pairs = []
	not_found_disjoints = []
	not_found_subsets = []
	not_fount_par = []

	for i in range(0, 300):
		print i
		# if i == 17 or i == 30 or i == 33 or i == 70 or i == 104 or i == 106 or i ==132 or i == 215 or i == 246 or i == 200 or i == 281 or i == 283:
		# 		continue
		try:
			res_disjoint = read_disjoint_sub_par_noun_phrase("data/disjoints/" + str(i) + '_lemma.txt')
			res_subset = read_disjoint_sub_par_noun_phrase("data/subsets/" + str(i) + '_lemma.txt')
			res_par = read_disjoint_sub_par_noun_phrase("data/parallels/" + str(i) + '_lemma.txt')
			res_np = read_question_np('data/np_classifier/' + str(i)+ '.txt')
			total_np = read_question_np('data/ans_preprocessed/'+str(i)+'_lemma.txt')
			# print total_np
		except:
			continue
		print res_np
		# print total_np	
		problem_pairs = []
		for np1 in res_np:
			for np2 in res_np:
				if np1 == np2:
					continue
				pairs.append(np1 + '	' + np2)
				problem_pairs.append(np1 + '	' + np2)
				problem_pairs.append(np2 + '	' + np1)
		print 'dissssssssssssssssssss'
		for dis_pair in res_disjoint:
			if check_validity(dis_pair, total_np, res_np) == True:
				if dis_pair not in problem_pairs:			
					print dis_pair
					# print i
					not_found_disjoints.append(dis_pair)
				disjoint_pairs.append(dis_pair)
		print 'suuuuuuuuuuuuubbbbbbbb'
		for sub_pair in res_subset:
			if check_validity(sub_pair, total_np, res_np) == True:
				if sub_pair not in problem_pairs:
					print sub_pair
					# print i
					not_found_subsets.append(sub_pair)
				subset_pairs.append(sub_pair)
		print 'paaaaaaaaaaaaaaaaaaaaarrrrr'
		for par_pair in res_par:
			if check_validity(par_pair, total_np, res_np) == True:
				if par_pair not in problem_pairs:
					print par_pair
					# print i
					not_fount_par.append(par_pair)
				par_pairs.append(par_pair)
	print 'lkahslkahlskfhalkshflakhsflakhsflkhaflkhsflak'
	print len(pairs)
	print len(disjoint_pairs)
	print len(subset_pairs)
	print len(par_pairs)
	print len(not_found_disjoints)
	print len(not_found_subsets)
	print len(not_fount_par)

def check_validity(pair, total_np, res_np):
	pair_parts = pair.split('	')
	if pair_parts[0] in total_np and pair_parts[1] in total_np:
		if pair_parts[0] not in res_np:
			print pair_parts[0]
		if pair_parts[1] not in res_np:
			print pair_parts[1]
		return True
	return False

def read_question_np(file_name):
	input_file = open(file_name, 'r')
	res = []
	for np in input_file:
		if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
			res.append(np[:-3].lower())
		else:
			res.append(np[:-1].lower())
	return res

def read_disjoint_sub_par_noun_phrase(file_name):
	input_file = open(file_name, 'r')
	res=[]
	for line in input_file:
		line = line[:-2]
		if line == '':
			break
		parts = line.split('	')
		res.append(parts[0].lower() + '	' + parts[1].lower())
	return res


pair_statistics()
