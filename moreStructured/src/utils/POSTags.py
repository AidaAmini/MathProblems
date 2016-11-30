#!/usr/bin/python
class POSTags:
	PosTags_list = {"unkown":1111, "nn": 0000, "nnp": 0001, "dt" : 0010, "jj": 0011, 'vbz': 0100, "cd": 0101, "nns": 0111, "nnsp": 1000, "wrb":1011 }
			
	@staticmethod
	def pos_tag_to_bin(word):
		global PosTags_list
		word = word.lower()
		word = word.replace(" ",'')
		word = word.replace(",",'')
		if word in PosTags_list:
			return str(PosTags_list[word])
		else:
			return str(PosTags_list["unkown"])