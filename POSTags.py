#!/usr/bin/python
class POSTags:
	PosTags_list = {"unkown": 0, "nn": 1, "nnp": 1, "dt" : 0, "jj": 2, 'vbz': 3, "cd": 2, "nns": 1, "nnsp": 1, "wrb":2, "prp": 0 }
	max_length = 11
	
	@staticmethod
	def pos_tag_to_bin(word):
		global PosTags_list
		word = word.lower()
#		print word
		if word in POSTags.PosTags_list:
			return str(POSTags.get_bin_one_hot(POSTags.PosTags_list[word]))[2:]
		else:
			return str(POSTags.get_bin_one_hot(POSTags.PosTags_list["unkown"]))[2:]
	
	@staticmethod
	def get_bin_one_hot(index):
		result = ''
		for i in range(0, index):
			result = '0' + result
		result = '1' + result
		for i in range(index+1, POSTags.max_length):
			result = '0' + result
		return result