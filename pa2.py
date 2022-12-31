# Name: pa2.py
# Author(s): Alex Bae, Liam Sefton
# Date: 9/29/22
# Description: For this assignment, we will write a program that converts an NFA
#              into an equivalent DFA.

from csv import QUOTE_NONE


class NFA:
	""" Simulates an NFA """

	def __init__(self, alphabet, start_states, accept_states, transitions, num_states):
		"""
		Initializes NFA from the file whose name is
		nfa_filename.  (So you should create an internal representation
		of the nfa.)
		"""
		self.nfa_transitions = transitions #maps state to character to set of states
		self.alphabet = alphabet
		#print(self.alphabet)
		
		self.q_naught = start_states #initial state is start state, 2nd to last line
		#print(self.q_naught)
		self.F = accept_states  #last line contains accept states


	def get_E_set_iterative(self, set):
		"""This function performs the operation decribed in the textbook
		for E(R), meaning given a set, it returns the set of states reachable by 0
		or more epsilon transitions from the states in the given set."""
		stack = set.copy()
		all_e_states = []
		visited = []
		#print("INSIDE E")
		#print(stack)


		#For formatting
		for thing in set:
			if type(thing) == list:
				for thing2 in thing:
					all_e_states.append(thing2)
			else:
				all_e_states.append(thing)
		#for i in range(len(all_e_states)):
		#	all_e_states[i] = int(all_e_states[i])

		#print(all_e_states)
		#Stack approach to tree structure exploration (treat epsilon transitions as a tree)
		while len(stack) > 0:
			e_states = []
			if type(stack[-1]) != list:
				stack[-1] = [stack[-1]]
			for state in stack[-1]:
				if state in self.nfa_transitions.keys():
					if 'e' in self.nfa_transitions[state].keys():
						if len(self.nfa_transitions[state]['e']) > 0:
							for st in self.nfa_transitions[state]['e']:
								#print("here")
								e_states.append(st)
			stack = stack[:-1] #pop
			for e_state in e_states:
				if e_state not in stack and e_state not in visited:
					stack.append(e_state) #push
					visited.append(e_state) #used to prevent infinite loops from occurring
				if int(e_state) not in all_e_states:
					all_e_states.append(int(e_state))

		final_result = []
		for item in all_e_states:
			final_result.append(str(item))
		#print(final_result)
		#print("E FINISHED")
		return final_result


	def get_powerset(self, elems):
		"""Returns set of all subsets of the given set."""
		yield []
		for i in range(len(elems)):
			for x in self.get_powerset(elems[i+1:]): 
				yield [elems[i]] + x 
				
	
	def remove_items(self, list, item):
		"""Used to clear the null set from sets 
		before attempting to get E(set)."""
		c = list.count(item)
		for i in range(c):
			list.remove(item)
		return list
		

	def toDFA(self):
		"""
		Converts the "self" NFA into an equivalent DFA
		and writes it to the file whose name is dfa_filename.
		The format of the DFA file must have the same format
		as described in the first programming assignment (pa1).
		This file must be able to be opened and simulated by your
		pa1 program.

		This function should not read in the NFA file again.  It should
		create the DFA from the internal representation of the NFA that you 
		created in __init__.
		"""
		#print(self.F)
		dfa_transitions = {'1' : {}} #start with just null state self looping
		for ch in self.alphabet:
			dfa_transitions['1'][ch] = '1'

		temp_f_prime = []

		all_states = []
		all_states.append(()) #null states
		stack = []
		curr_state = tuple([*set(self.get_E_set_iterative([self.q_naught]))])
		#print(curr_state)
		q_naught_prime = curr_state
		for st in self.F:
			if st in curr_state:
				temp_f_prime.append(curr_state)
		#print(self.nfa_transitions)
		all_states.append(curr_state)
		stack.append(curr_state)
		#print(curr_state)
		while len(stack) > 0:
			curr_state = stack.pop()
			#print(curr_state)
			for ch in self.alphabet:
				#print(ch)
				new_state = []
				for st1 in curr_state:
					if st1 in self.nfa_transitions.keys() and ch in self.nfa_transitions[st1].keys():
						for st2 in self.nfa_transitions[st1][ch]:
							new_state += list(self.get_E_set_iterative([st2]))
				if str(all_states.index(curr_state) + 1) not in dfa_transitions.keys():
					dfa_transitions[str(all_states.index(curr_state) + 1)] = {}
				if len(new_state) > 1:
					new_state = [*set(new_state)] #removes duplicates and sorts list
				new_state = tuple(new_state)
				if new_state not in all_states:
					all_states.append(new_state)
					stack.append(new_state)

				for st in self.F:
					if st in new_state:
						temp_f_prime.append(new_state)
				dfa_transitions[str(all_states.index(curr_state) + 1)][ch] = str(all_states.index(new_state) + 1)
		#print(all_states)
		#print(dfa_transitions)
		F_PRIME = [*set(temp_f_prime)]
		#print(F_PRIME)

		"""
		f = open(dfa_filename, "w")
		f.write(str(len(all_states)) + "\n") #Num states
		for ch in self.alphabet:
			f.write(ch) #alphabet
		f.write("\n")

		for state in all_states:
			for ch in self.alphabet:
				emitting_state = str(all_states.index(state) + 1)
				receiving_state = dfa_transitions[str(all_states.index(state) + 1)][ch]
				f.write(emitting_state + " \'" + ch + "\' " + receiving_state + "\n")

		f.write(str(all_states.index(q_naught_prime) + 1) + "\n")
		"""
		accept_states_string = ""
		for state in F_PRIME:
			accept_states_string += str(all_states.index(state) + 1) + " "
		accept_states_string = accept_states_string[:-1]
		return (str(all_states.index(q_naught_prime) + 1), accept_states_string.split(" "), dfa_transitions)
		#f.write(accept_states_string)
		#f.close()

