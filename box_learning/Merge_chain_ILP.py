#!/usr/bin/python

# Copyright 2016, Gurobi Optimization, Inc.
from file_refrence import file_refrence 
from gurobipy import *

class ilp_merge_chain:
	label_disjoint = 1
	label_no_rel = 0
	label_subset = 3
	label_eq = 2

	file_path_refrence = file_refrence()
	unary_list_index = []
	binary_list_index = []
	merge_prob = []
	data_start = 0
	data_end = 0
	unary_chain_size = 0
	binary_chain_size = 0

	def __init__(self, start_data_index, end_data_index):
		self.data_start = start_data_index
		self.data_end = end_data_index

	def find_mergings(self, problem_index):
		input_file = open(self.file_path_refrence.ilp_merge_results_path + str(problem_index) +'.txt', 'r')
		output_file = open(self.file_path_refrence.ilp_merge_chain_res + str(problem_index) + '.txt', 'w')
		for line in input_file:
			if '??' in line:
				if line[line.find('??') + 2] == '1':
					line_parts = line[:-1].split('   ')
					print float(line_parts[1])
					if float(line_parts[1]) == 1.0:
						unary_index = int(line[1:line.find('_')])
						binary_index = int(line[line.find('_')+1:line.find('??')])
						output_file.write(self.unary_list_index[unary_index] + '	' + self.binary_list_index[binary_index] + '\n')

	def read_data(self, problem_index):
		print 'aqaaasdasdadadadsasadsa'
		self.unary_list_index =[]
		self.binary_list_index = []
		input_file = open(self.file_path_refrence.merge_prob_path + str(problem_index) + '.txt', 'r')
		line  = input_file.readline()
		num_of_np = len(line[:-1].split(', '))
		print num_of_np
		self.unary_chain_size = num_of_np
		self.binary_chain_size = num_of_np * num_of_np
		self.merge_prob = [[0.0 for x in range(self.binary_chain_size)] for y in range(self.unary_chain_size)]
		print self.merge_prob[0]
		line = input_file.readline()
		while line != '':
			# print line
			parts = line[:-1].split('	')
			chain1_index = 0
			# print 'parts[0]'
			# print parts[1]
			# print self.unary_list_index
			if parts[1] in self.unary_list_index:
				chain1_index = self.unary_list_index.index(parts[1])
			else:
				self.unary_list_index.append(parts[1])
				chain1_index = len(self.unary_list_index) - 1

			chain2_index = 0
			if parts[0] in self.binary_list_index:
				chain2_index = self.binary_list_index.index(parts[0])
			else:
				self.binary_list_index.append(parts[0])
				chain2_index = len(self.binary_list_index) - 1
			prob = float(parts[2])
			# print "chain1_index"
			# print len(self.merge_prob[0])
			# print chain1_index
			self.merge_prob[chain1_index][chain2_index] = prob
			line = input_file.readline()
		self.binary_chain_size = len(self.binary_list_index)

	# Create a new model
	def learn_procedure(self):
		for index in range(self.data_start, self.data_end):
			if index in self.file_path_refrence.problematic_indexes:
				continue
			print 'problem :::::::' + str(index)
			self.read_data(index)
			m = Model("qcp")
			xi = []
			xijm = [[[0 for x in range(2)] for y in range(self.binary_chain_size)] for z in range(self.unary_chain_size)]
			for i in range(0, self.unary_chain_size):
				xij = [[0 for x in range(2)]for y in range(self.binary_chain_size)]
				for j in range(0, self.binary_chain_size):
					xm = []
					for k in range(0, 2):
						xm.append(m.addVar(vtype=GRB.INTEGER, name="y"+str(i) + '_' + str(j) + '??' + str(k)))
					xij[j] = xm
				xijm[i] = xij
			m.update()

			obj = 0
			for i in range(0, self.unary_chain_size):
				for j in range(0, self.binary_chain_size):
						obj = obj + xijm[i][j][1]* self.merge_prob[i][j]
			m.setObjective(obj, GRB.MAXIMIZE)

			for i in range(0, self.unary_chain_size):
				for j in range(0, self.binary_chain_size):
					m.addConstr(xijm[i][j][0] + xijm[i][j][1]  >= 1 ,"one_relation")
					m.addConstr(xijm[i][j][0] + xijm[i][j][1]  <= 1 ,"one_relation")

			for i in range(0, self.unary_chain_size):
				for j in range(0, self.binary_chain_size):
					m.addConstr(xijm[i][j][1] + xijm[k][j][1] + xijm[i][k][0] <= 2, "SDTransitive1")

			for i in range(0, self.unary_chain_size):
				index_in_bin = self.unary_list_index.index(self.unary_list_index[i])
				m.addConstr(xijm[i][index_in_bin][1] + xijm[index_in_bin][i][0] <= 1, "ref")
				m.addConstr(xijm[i][index_in_bin][1] + xijm[index_in_bin][i][0] >= 1, "ref")

			# for i in range(0, self.unary_chain_size):


			for i in range(0, self.unary_chain_size):
				for j in range(0, self.binary_chain_size):
					for k in range(0, 2):
						m.addConstr(xijm[i][j][k] >= 0)
						m.addConstr(xijm[i][j][k] <= 1)
				

			m.optimize()
			output_file_for_problem = open(self.file_path_refrence.ilp_merge_results_path + str(index) +'.txt', 'w')
			for i in range(len(self.unary_list_index) - 1):
				output_file_for_problem.write(self.unary_list_index[i] + '	')
			output_file_for_problem.write(self.unary_list_index[len(self.unary_list_index) - 1] + '\n')
			for i in range(len(self.binary_list_index) - 1):
				output_file_for_problem.write(self.binary_list_index[i] + '	')
			print len(self.binary_list_index)
			output_file_for_problem.write(self.binary_list_index[len(self.binary_list_index) - 1] + '\n')
			for v in m.getVars():
			    output_file_for_problem.write(v.varName + '   ' + str(v.x) + '\n')

			print('Obj: %g' % obj.getValue())
			output_file_for_problem.write(str(obj.getValue()) + '\n')
			self.find_mergings(index)


ilp_merge = ilp_merge_chain(201, 202)
ilp_merge.learn_procedure()